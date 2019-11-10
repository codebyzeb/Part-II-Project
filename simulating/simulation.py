"""
Simulation module deals with managing the different simulations of 
placing entities into environments, getting behaviour and having
the environments update accordingly. The simulations should run and
return the final energy of the initial entities given.

"""

from simulating.entity import Entity
from simulating.environment import Environment


class Simulation:  #pylint: disable=R0903
    """ Represents a full simulation of an entity in an environment

    Attributes:
        num_epochs: The number of epochs to run
        num_cycles: The number of time steps in each cycle
        entity: The entity whose behaviour is tested        
    """

    num_epochs = 0
    num_cycles = 0
    entity = None

    def __init__(self, epochs, cycles, ent):
        self.num_epochs = epochs
        self.num_cycles = cycles
        self.entity = ent

    def run(self, debug=True):
        """ Runs a full simulation

        Runs num_epochs epochs, each of which contains num_cycles time steps.
        At each time step, the world is updated according to the behaviour
        of the entity. The entity returns an action given inputs that depend
        on its position in the simulated world. 

        Args:
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
                    self.entity.eat(env.get_cell(mush_pos))
                    env.clear_cell(mush_pos)
                    if debug:
                        print("EATING MUSHROOM")

                # Calculate the angle and get mushroom properties if close enough
                angle = env.get_angle(entity_pos, mush_pos)
                mush = env.get_cell(mush_pos) if env.adjacent(
                    entity_pos, mush_pos) else 0

                # Get the behaviour of the entity given perceptual inputs
                action, _ = self.entity.behaviour(angle, mush, 0)

                # Print debug information
                if debug:
                    print("Epoch:", epoch, "   Cycle:", step)
                    print(env)
                    print("Entity energy:", self.entity.energy)
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
                    input()

                # Finally, do the action
                env.move_entity(action)

            # After an epoch, reset the world
            env.reset()
            env.place_entity()
