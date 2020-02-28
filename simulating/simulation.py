"""
Simulation module deals with managing the different simulations of 
placing entities into environments, getting behaviour and having
the environments update accordingly. The simulations should run and
return the final fitness of the initial entities given.

"""

import argparse
import math
import os
import random
import pickle
import copy

from enum import Enum

from multiprocessing import Pool

from analysis.plotting import Plotter
from simulating.action import Action
from simulating.entity import NeuralEntity
from simulating.environment import Environment
from simulating import environment
from simulating.entity import array_to_bits


class Language(Enum):
    """ Represent possible types of languages """

    NONE = "None"
    EXTERNAL = "External"
    EVOLVED = "Evolved"

    def from_string(self, language_type):
        """ Returns language from a string """
        if language_type == "Evolved":
            return self.EVOLVED
        if language_type == "External":
            return self.EXTERNAL
        return self.NONE


class Simulation:  #pylint: disable=R0903
    """ Represents a simulation environment for a population of entities.

    Attributes:
        num_epochs: The number of epochs to run
        num_cycles: The number of time steps in each cycle
        num_entities: The number of entities in the population
        num_generations: The number of generations to run the simulation for
    """

    # Simulation loop parameters
    num_epochs = 0
    num_cycles = 0
    num_entities = 0
    num_generations = 0
    language_type = Language.NONE

    # Genetic algorithm parameters
    percentage_mutate = 0.1
    percentage_keep = 0.2

    # I/O parameters
    interactive = False
    threading = True

    record_language = True
    record_language_period = 1

    record_entities = True
    record_entities_period = 1

    record_fitness = True

    foldername = "folder"

    def __init__(self, epochs, cycles, population_size, generations, language_type):
        self.num_epochs = epochs
        self.num_cycles = cycles
        self.num_entities = population_size
        self.num_generations = generations
        self.language_type = self.language_type.from_string(language_type)

    def set_io_options(self,
                       interactive=False,
                       record_language=True,
                       record_language_period=1,
                       record_entities=True,
                       record_entities_period=1,
                       record_fitness=True,
                       foldername="folder"):
        """ Set options that determine I/O """

        self.interactive = interactive
        self.record_language = record_language
        self.record_language_period = record_language_period
        self.record_entities = record_entities
        self.record_entities_period = record_entities_period
        self.record_fitness = record_fitness
        self.foldername = foldername

    def run_single(self, entity, population=[], viewer=False):
        """ Runs a single simulation for one entity

        Runs num_epochs epochs, each of which contains num_cycles time steps.
        At each time step, the world is updated according to the behaviour
        of the entity. The entity returns an action given inputs that depend
        on its position in the simulated world. 

        Args:
            entity: The entity whose behaviour is tested        
            at each step.
            population: The remaining entities in the population
            viewer (bool): If true, prints debugging information and pauses
        """

        env = Environment()
        env.place_entity()

        # Run num_epochs epochs of num_cycles cycles each
        for epoch in range(self.num_epochs):

            for step in range(self.num_cycles):

                # Get entity position and closest mushroom
                entity_pos = env.get_entity_position()
                try:
                    mush_pos = env.closest_mushroom(entity_pos)
                except (environment.MushroomNotFound):
                    # Skip cycle if all mushrooms have been eaten
                    break

                # Calculate the angle and get mushroom properties if close enough
                angle = env.get_entity_angle_to_position(mush_pos)
                mush = env.get_cell(mush_pos) if env.adjacent(entity_pos, mush_pos) else 0

                # Get audio signal according to language type
                signal = self.get_signal(angle, env.get_cell(mush_pos), population, viewer)

                # Get the behaviour of the entity given perceptual inputs
                action, out_signal = entity.behaviour(angle, mush, signal)

                # Print debug information
                if viewer:
                    to_print = "\n".join([
                        "Epoch: {0}    Cycle: {1}".format(epoch, step),
                        str(env), "Entity fitness: {0}".format(entity.fitness),
                        "Entity position: ({0},{1})".format(entity_pos[0], entity_pos[1]),
                        "Closest mushroom position: ({0},{1})".format(mush_pos[0], mush_pos[1]),
                        "Direction: {0}".format(env.entity_direction), "Angle: {0}".format(angle),
                        "Mushroom input: {0}".format(mush), "Signal input: {0}".format(signal),
                        "Action chosen: {0}".format(action), "Signal output: {0}".format(out_signal)
                    ])
                    print(to_print)
                    ##time.sleep(0.1)
                    usr_input = input()
                    if usr_input == chr(27):
                        return entity

                # If the action is NOTHING, it will stay that way,
                # so we can make some optimisations
                if action == Action.NOTHING:
                    break

                # We can also break if the entity tries to move forward but can't
                if action == Action.FORWARDS and env.entity_facing_out():
                    break

                # Do the action
                env.move_entity(action)

                # Finally, eat a mushroom if currently on one
                new_pos = env.get_entity_position()
                if env.is_mushroom(new_pos):
                    entity.eat(env.get_cell(new_pos))
                    env.clear_cell(new_pos)
                    if viewer:
                        print("EATING MUSHROOM")

            # After an epoch, reset the world and replace the entity
            env.reset()
            env.place_entity()

        return entity

    def get_signal(self, angle, mush, population, viewer):
        """
        Generate the appropriate audio signal according to language type

        Args:
            angle: The angle to the closest mushroom
            mush: The perceptual properties of the closest mushroom
            population: The remaining entities in the population
            viewer (bool): If true, prints debugging information and pauses        
        """

        if self.language_type == Language.NONE:
            signal = [0.5, 0.5, 0.5]

        elif self.language_type == Language.EXTERNAL:
            # Externally imposed language
            signal = [1, 0, 0] if environment.is_edible(mush) else [0, 1, 0]
            if viewer:
                print("getting signal for mushroom ", bin(mush))

        elif self.language_type == Language.EVOLVED:
            # A partner entity (which can see the mushroom properties)
            # names the mushroom for this entity
            partner_entity = random.choice(population)
            _, signal = partner_entity.behaviour(angle, mush, [0.5, 0.5, 0.5])
            if viewer:
                print("Partner vocal:", signal)
                print("Partner weights:", partner_entity.weights)
                print("Partner weights:", partner_entity.baises)

        return signal

    def start(self):
        """ Run a population of neural entities from generation 0
        """

        # Generate an initial population of neural entities
        entities = [NeuralEntity() for _ in range(self.num_entities)]
        self.run_population(entities)

    def start_from_generation(self, generation):
        """ Run a previously-saved population of neural entities

        Args:
            generation: The generation to load from
        """

        entities = self.load_entities(generation)
        self.run_population(entities, generation)

    def run_population(self, entities, start_generation=0):
        """ Run a population of entities

        Loop for num_generations evolutionary steps. At each step,
        run a single simulation for each entity, choose the best 20
        in terms of fitness and let them asexually reproduce for the
        next generation.
        """

        # Initialise files and plotter for simulation I/O
        plotter = self.initialise_io()

        # Run evolution loop
        for generation in range(start_generation, self.num_generations + 1):

            # For each entity, create a list of the other entities for the Evolved language
            cloned_population = [ent.copy() for ent in entities]
            populations = [[] for i in range(len(cloned_population))]
            if self.language_type == Language.EVOLVED:
                for i in range(len(cloned_population)):
                    populations[i] = (cloned_population[0:i] +
                                      cloned_population[i + 1:len(cloned_population)])

            # Run a simulation for each entity
            if self.threading:
                with Pool() as pool:
                    entities = pool.starmap(self.run_single, zip(entities, populations))
            else:
                for i, entity in enumerate(entities):
                    self.run_single(entity, populations[i])

            # Sort the entities by final fitness value
            entities.sort(key=lambda entity: entity.fitness, reverse=True)

            # Do I/O including writing to files and displaying interactive information
            self.io(entities, generation, populations, plotter)

            # Finally, select the best entities to reproduce for the next generation
            entities = self.reproduce_population(entities)

    def reproduce_population(self, entities):
        """
        Use percentage_keep and percentage_mutate to create
        a new population of entities using asexual reproduction
        """
        best_entities = entities[:math.ceil(self.num_entities * self.percentage_keep)]
        new_population = [
            child for entity in best_entities
            for child in entity.reproduce(int(1 / self.percentage_keep), self.percentage_mutate)
        ]
        return new_population

    skip_interactive_count = 0

    def initialise_io(self):
        """ Create the neccessary plotter and folders for I/O
        """
        plotter = Plotter() if self.interactive else None
        if not os.path.exists(self.foldername):
            os.makedirs(self.foldername)
        if not os.path.exists(self.foldername + "/populations"):
            os.makedirs(self.foldername + "/populations")
        if not os.path.exists(self.foldername + "/language"):
            os.makedirs(self.foldername + "/language")
        if self.record_fitness:
            fitness_file = self.foldername + "/fitness.txt"
            open(fitness_file, "w").close()

        info_file = open(self.foldername + "/info.txt", "w")
        info_file.writelines("\n".join([
            "Num Epochs: " + str(self.num_epochs), "Num Cycles: " + str(self.num_cycles),
            "Num Entities: " + str(self.num_entities),
            "Num Generations:" + str(self.num_generations),
            "Language Type: " + str(self.language_type),
            "Percentage Mutate" + str(self.percentage_mutate),
            "Percentage Keep" + str(self.percentage_keep)
        ]))
        info_file.close()

        return plotter

    def io(self, entities, generation, populations, plotter):
        """ Write to files and display the plotter and interactive information
        for the simulation
        """
        # Get average fitness
        average_fitness = sum([entity.fitness for entity in entities]) / len(entities)

        # Save the average fitness values
        if self.record_fitness:
            with open(self.foldername + "/fitness.txt", "a") as out:
                out.write(str(average_fitness) + "\n")

        # If generation is a multiple of the record_language_period
        # option, record the language
        if self.record_language and generation % self.record_language_period == 0:
            self.save_language(entities, generation)

        # If generation is a multiple of the save_entities_period
        # option, save the population
        if self.record_entities and generation % self.record_entities_period == 0:
            self.save_entities(entities, generation)

        # Run interactive menu and plot the average fitness over time
        if self.interactive:
            plotter.add_point_and_update(generation, average_fitness)
            self.interactive_viewer(generation, entities, populations, average_fitness)

    def interactive_viewer(self, generation, entities, populations, average_fitness):
        """ At each generation, display information about the simulation

        Loops to allow for viewing individual entities' behaviour, 

        Args:
            generation: The current generation
            entities: The list of entities at this generation
        """

        loop_interactive = True
        while loop_interactive:
            print("----- GENERATION ", generation, " -----", sep="")
            print("Sorted fitness values: ")
            print([entity.fitness for entity in entities])
            print("Average fitness:", average_fitness)
            if self.skip_interactive_count > 0:
                self.skip_interactive_count -= 1
                usr_input = ""
            else:
                usr_input = input("\n")
            if usr_input.split(" ")[0] == "watch":
                if len(usr_input.split(" ")) < 2:
                    print("INVALID NUMBER\n")
                    continue
                try:
                    i = int(usr_input.split(" ")[1])
                except ValueError:
                    print("INVALID NUMBER\n")
                    continue
                if not 0 <= i < len(entities):
                    print("INVALID NUMBER\n")
                    continue
                if_yes = input(
                    str("Watching behaviour of entity " + str(i) + " - enter yes to continue: "))
                if if_yes == "yes":
                    fitness = entities[i].fitness
                    entities[i].fitness = 0
                    self.run_single(entities[i], populations[i], viewer=True)
                    entities[i].fitness = fitness
            elif len(usr_input) == 0:
                loop_interactive = False
            elif usr_input.isdecimal():
                self.skip_interactive_count = int(usr_input) - 1
                loop_interactive = False
            else:
                print("INVALID INPUT\n")

    def save_language(self, entities, generation):
        """
        Given a group of entities at a certain generation, performs a naming task
        for each entity to get a sample of the language used by the entities
        for edible and poisonous mushrooms
        """

        edible_samples = []
        poisonous_samples = []
        for entity in entities:
            edible, poisonous = self.naming_task(entity)
            edible_samples.extend(edible)
            poisonous_samples.extend(poisonous)
        with open(self.foldername + "/language/edible" + str(generation) + ".txt", "w") as out:
            out.write("\n".join([str(s) for s in edible_samples]))
        with open(self.foldername + "/language/poisonous" + str(generation) + ".txt", "w") as out:
            out.write("\n".join([str(s) for s in poisonous_samples]))

    def save_entities(self, entities, generation):
        """
        Saves the current group of entities to a binary file
        """
        filename = self.foldername + "/populations/generation" + str(generation) + ".p"

        pickle.dump([entity.copy() for entity in entities], open(filename, 'wb'))

    def load_entities(self, generation):
        """
        Load a group of entities from a file
        """

        filename = self.foldername + "/populations/generation" + str(generation) + ".p"

        entities = pickle.load(open(filename, "rb"))
        return entities

    def naming_task(self, entity):
        """
        Return 80 samples of the language produced by this entity
        for poisonous and edible mushrooms
        """

        edible_samples = []
        poisonous_samples = []

        # Get all possible mushrooms
        edible_mushrooms = [environment.make_edible(i) for i in range(10)]
        poisonous_mushrooms = [environment.make_poisonous(i) for i in range(10)]

        # Get a sample of the language for each mushroom for each of four directions
        for angle in [0, 0.25, 0.5, 0.75]:
            for mushroom in edible_mushrooms:
                _, signal = entity.behaviour(angle, mushroom, [0.5, 0.5, 0.5])
                edible_samples.append(array_to_bits(signal))
            for mushroom in poisonous_mushrooms:
                _, signal = entity.behaviour(angle, mushroom, [0.5, 0.5, 0.5])
                poisonous_samples.append(array_to_bits(signal))

        # Return samples
        return edible_samples, poisonous_samples


def run_single(args):
    """ Run a basic simulation for debugging.
    """

    sim = Simulation(args.num_epo, args.num_cyc, args.num_ent, args.num_gen, args.language)
    sim.set_io_options(interactive=args.interactive,
                       record_language=args.rec_lang,
                       record_language_period=args.rec_lang_per,
                       record_entities=args.rec_ent,
                       record_entities_period=args.rec_ent_per,
                       record_fitness=args.rec_fit,
                       foldername=args.foldername)
    ent = NeuralEntity()
    print(ent.weights)
    print(ent.biases)
    sim.run_single(ent, viewer=True)


def run_full(args):
    """ Run a neural simulation for debugging
    """

    sim = Simulation(args.num_epo, args.num_cyc, args.num_ent, args.num_gen, args.language)
    sim.set_io_options(interactive=args.interactive,
                       record_language=args.no_rec_lang,
                       record_language_period=args.rec_lang_per,
                       record_entities=args.no_rec_ent,
                       record_entities_period=args.rec_ent_per,
                       record_fitness=args.no_rec_fit,
                       foldername=args.foldername)
    sim.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the full genetic algorithm')
    parser.add_argument('language',
                        type=str,
                        choices=['None', 'Evolved', 'External'],
                        help='language type used in the simulation')
    parser.add_argument('foldername', type=str, help='where results are stored')
    parser.add_argument('-s',
                        '--single',
                        action='store_true',
                        help='run a single simulation for one entity')
    parser.add_argument('-i', '--interactive', action='store_true', help='run with interactivity')
    parser.add_argument('--num_epo',
                        action='store',
                        type=int,
                        default=15,
                        help='number of epochs per single simulation run')
    parser.add_argument('--num_cyc',
                        action='store',
                        type=int,
                        default=50,
                        help='number of cycles per epoch')
    parser.add_argument('--num_ent',
                        action='store',
                        type=int,
                        default=100,
                        help='number of entities in the population')
    parser.add_argument('--num_gen',
                        action='store',
                        type=int,
                        default=1000,
                        help='number of generations to run for')
    parser.add_argument('--per_mut',
                        action='store',
                        type=float,
                        default=0.1,
                        help='percentage of weights to mutate in reproduction')
    parser.add_argument('--per_keep',
                        action='store',
                        type=float,
                        default=0.2,
                        help='percentage of population that reproduces')
    parser.add_argument('--no_rec_lang', action='store_false', help='don\'t store the language')
    parser.add_argument('--rec_lang_per',
                        action='store',
                        type=float,
                        default=1,
                        help='how frequently to store the language')
    parser.add_argument('--no_rec_ent', action='store_false', help='don\'t store the population')
    parser.add_argument('--rec_ent_per',
                        action='store',
                        type=float,
                        default=25,
                        help='how frequently to store the population')
    parser.add_argument('--no_rec_fit', action='store_false', help='don\'t store the fitness')

    args, unknown = parser.parse_known_args()

    if args.single:
        run_single(args)
    else:
        run_full(args)
