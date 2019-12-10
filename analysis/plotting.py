"""
Analysis module used for plotting graphs of the simulation
"""

import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')


class Plotter:
    """ Represents a simulation environment for a population of entities.

    Attributes:
        generations: The x-axis, the generation number
        average_entities: The y-axis, the average energy of the population over generation count
        ax: The axis plotted
    """

    generations = []
    average_energies = []

    ax = None

    def __init__(self):
        """
        Initialise the plot

        """

        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(1, 1, 1)
        plt.show()

    def add_point_and_update(self, generation, average_energy):
        """
        Add a point and update the graph

        Args:
            generation: The generation number        
            average_energy: The average energy of the population
        """

        self.generations.append(generation)
        self.average_energies.append(average_energy)
        self.ax.clear()
        self.ax.plot(self.generations, self.average_energies)
        plt.draw()
        plt.pause(0.01)
