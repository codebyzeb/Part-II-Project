"""
Simulation module deals with managing the different simulations of 
placing entities into environments, getting behaviour and having
the environments update accordingly. The simulations should run and
return the final energy of the initial entities given.

"""

import math
import random

from multiprocessing import Pool
from itertools import product

from analysis.plotting import Plotter
from simulating.action import Action
from simulating.entity import NeuralEntity
from simulating.environment import Environment
from simulating import environment
from simulating.entity import bits_to_array


class Simulation:  #pylint: disable=R0903
    """ Represents a simulation environment for a population of entities.

    Attributes:
        num_epochs: The number of epochs to run
        num_cycles: The number of time steps in each cycle
        num_entities: The number of entities in the population
    """

    num_epochs = 0
    num_cycles = 0
    num_entities = 0
    num_generations = 0

    def __init__(self, epochs, cycles, population_size, generations):
        self.num_epochs = epochs
        self.num_cycles = cycles
        self.num_entities = population_size
        self.num_generations = generations

    def run_single(self,
                   entity,
                   language_type="None",
                   partner_entity=None,
                   interactive=False):
        """ Runs a single simulation for one entity

        Runs num_epochs epochs, each of which contains num_cycles time steps.
        At each time step, the world is updated according to the behaviour
        of the entity. The entity returns an action given inputs that depend
        on its position in the simulated world. 

        Args:
            entity: The entity whose behaviour is tested        
            debug (bool): If true, prints debugging information and pauses
            at each step.
        """

        env = Environment()
        env.place_entity()

        # Do whole simulation
        for epoch in range(self.num_epochs):

            # Do an epoch
            for step in range(self.num_cycles):
                # Get entity position and closest mushroom
                entity_pos = env.get_entity_position()
                _, mush_pos = env.closest_mushroom(entity_pos)

                # Eat a mushroom if currently on one
                if env.entity_position == mush_pos:
                    entity.eat(env.get_cell(mush_pos))
                    env.clear_cell(mush_pos)
                    if interactive:
                        print("EATING MUSHROOM")

                # Calculate the angle and get mushroom properties if close enough
                angle = env.get_angle(entity_pos, mush_pos)
                mush = env.get_cell(mush_pos) if env.adjacent(
                    entity_pos, mush_pos) else 0

                # Get audio signal
                signal = (0.5, 0.5, 0.5)
                if language_type == "External":
                    signal = (1, 0, 0) if (environment.is_edible(
                        env.get_cell(mush_pos))) else (0, 1, 0)
                elif language_type == "Evolved":
                    _, partner_vocal = partner_entity.behaviour(
                        angle, env.get_cell(mush_pos), (0.5, 0.5, 0.5))
                    signal = bits_to_array(partner_vocal, 3)

                # Get the behaviour of the entity given perceptual inputs
                action, _ = entity.behaviour(angle, mush, signal)

                # Print debug information
                if interactive:
                    print("Epoch:", epoch, "   Cycle:", step)
                    print(env)
                    print("Entity energy:", entity.energy)
                    print("Entity position: (",
                          entity_pos[0],
                          ",",
                          entity_pos[1],
                          ")",
                          sep="")
                    print("Closest mushroom position: (",
                          mush_pos[0],
                          ",",
                          mush_pos[1],
                          ")",
                          sep="")
                    print("Direction: ", env.entity_direction)
                    print("Angle: ", angle)
                    print("Mushroom input: ", mush)
                    print("Action chosen: ", action)
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

                # Finally, do the action
                env.move_entity(action)

            # After an epoch, reset the world
            env.reset()
            env.place_entity()
        return entity

    def run_population(self, filename, language_type="None",
                       interactive=False):
        """ Run a population of entities without any energies

        Loop for num_generations evolutionary steps. At each step,
        run a single simulation for each entity, choose the best 20
        in terms of fitness and let them asexually reproduce for the
        next generation.

        Args:
            debug (bool): If true, prints debugging information and pauses
            at each step.
        """

        # Plotter and file to plot and save energy values
        plotter = Plotter()
        out = open(filename, "w")
        out.close()

        # First, generate the initial population of neural entities
        entities = [NeuralEntity(0, [5]) for _ in range(self.num_entities)]

        # Run evolution loop
        for generation in range(self.num_generations):

            # Get a partner for each entity
            partners = []
            for i in range(len(entities)):
                r = list(range(0, i)) + list(range(i + 1, len(entities)))
                partners.append(entities[random.choice(r)])

            # Run a simulation for each entity
            with Pool() as pool:
                entities = pool.starmap(
                    self.run_single,
                    zip(entities, [language_type] * len(entities), partners))

            #for i, entity in enumerate(entities):
            #    self.run_single(entity, language_type, partners[i])

            # Sort the entities by final energy value
            entities.sort(key=lambda entity: entity.energy, reverse=True)

            # Get average energy and add to the live graph
            average_energy = sum([entity.energy
                                  for entity in entities]) / len(entities)
            plotter.add_point(generation, average_energy)

            # Run interactive menu
            if interactive:
                self.interactive_viewer(generation, entities, average_energy)

            # Save the average energy values
            with open(filename, "a") as out:
                out.write(str(average_energy) + "\n")

            # Select the best 20% to reproduce for the next generation
            best_entities = entities[:math.ceil(self.num_entities / 5)]
            entities = [
                child for entity in best_entities
                for child in entity.reproduce(5, 0.1)
            ]

    skip_interactive_count = 0

    def interactive_viewer(self, generation, entities, average_energy):
        """ At each generation, display information about the simulation

        Loops to allow for viewing individual entities' behaviour, 

        Args:
            generation: The current generation
            entities: The list of entities at this generation
        """

        loop_interactive = True
        while loop_interactive:
            print("----- GENERATION ", generation, " -----", sep="")
            print("Sorted energy values: ")
            print([entity.energy for entity in entities])
            print("Average energy:", average_energy)
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
                    str("Watching behaviour of entity " + str(i) +
                        " - enter yes to continue: "))
                if if_yes == "yes":
                    energy = entities[i].energy
                    entities[i].energy = 0
                    self.run_single(entities[i], interactive=True)
                    entities[i].energy = energy
            elif len(usr_input) == 0:
                loop_interactive = False
            elif usr_input.isdecimal():
                self.skip_interactive_count = int(usr_input)
                loop_interactive = False
            else:
                print("INVALID INPUT\n")
