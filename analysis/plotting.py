"""
Analysis module used for plotting graphs of the simulation
"""

import matplotlib.pyplot as plt
from matplotlib import style


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


if __name__ == "__main__":
    style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    for language_type in ["none", "evolved", "external"]:
        energies_file = open("output/" + language_type + ".txt", "r")
        average_energies = []
        lines = energies_file.readlines()
        energies_file.close()
        for line in lines:
            average_energies.append(float(line))
        ax1.plot(list(range(len(average_energies))),
                 average_energies,
                 label=language_type,
                 linewidth=1.0)
    leg = plt.legend()
    plt.show()
