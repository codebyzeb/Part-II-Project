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


def plotOne():
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
    plt.legend()
    plt.show()


def plotTen():
    fig = plt.figure()
    for i in range(10):
        ax = fig.add_subplot(5, 2, i + 1)
        for language_type in ["none", "evolved", "external"]:
            energies_file = open(
                "output/" + language_type + str(i) + "/energies.txt", "r")
            average_energies = []
            lines = energies_file.readlines()
            energies_file.close()
            for line in lines:
                average_energies.append(float(line))
            ax.plot(list(range(len(average_energies))),
                    average_energies,
                    label=language_type,
                    linewidth=1.0)
    plt.legend()
    plt.show()


def plotAverage():
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    for language_type in ["none", "evolved", "external"]:
        average_energies = [0 for i in range(1001)]
        totalNum = 1001
        for i in range(10):
            energies_file = open(
                "output/" + language_type + str(i) + "/energies.txt", "r")
            lines = energies_file.readlines()
            if len(lines) < totalNum:
                totalNum = len(lines)
                average_energies = average_energies[:totalNum]
            energies_file.close()
            for j, line in enumerate(lines):
                if (j >= totalNum):
                    break
                average_energies[j] += (float(line) / 10)
        ax1.plot(list(range(len(average_energies))),
                 average_energies,
                 label=language_type,
                 linewidth=1.0)
    plt.legend()
    plt.show()


def plotLanguageDistributions(foldername, generations):
    fig = plt.figure()
    for j, gen in enumerate(generations):
        for i, language in enumerate(["edible", "poisonous"]):
            languages = [0, 0, 0, 0, 0, 0, 0, 0]
            with open(foldername + "/" + language + str(gen) + ".txt",
                      "r") as language_file:
                for sample in language_file.readlines():
                    languages[int(sample[0])] += 1
            ax = fig.add_subplot(len(generations), 2, i + 1 + j * 2)
            ax.plot([str(bin(i))[2:] for i in range(8)], languages)
    plt.show()


if __name__ == "__main__":
    style.use('fivethirtyeight')
    plotLanguageDistributions("testing", [i * 20 for i in range(10)])
    #plotAverage()
    #plotTen()
