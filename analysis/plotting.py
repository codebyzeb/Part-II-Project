"""
Analysis module used for plotting graphs of the simulation
"""

import matplotlib.pyplot as plt
from matplotlib import style
from scipy.stats import pearsonr
import sys
import numpy as np


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


def plot_one(foldername):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    energies_file = open(foldername + "/energies.txt", "r")
    average_energies = []
    lines = energies_file.readlines()
    energies_file.close()
    for line in lines:
        average_energies.append(float(line))
    ax1.plot(list(range(len(average_energies))),
             average_energies,
             label="Average Fitness",
             linewidth=1.0)
    plt.legend()
    plt.show()


def plot_ten(foldername):
    fig = plt.figure()
    for i in range(10):
        ax = fig.add_subplot(5, 2, i + 1)
        for language_type in ["none", "evolved", "external"]:
            energies_file = open(foldername + "/" + language_type + str(i) + "/energies.txt", "r")
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


def plot_ten_evolved(foldername, language):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    for i in range(10):
        energies_file = open(foldername + "/" + language + str(i) + "/energies.txt", "r")
        lines = energies_file.readlines()
        average_energies = [0 for i in range(1001)]
        totalNum = 1001
        if len(lines) < totalNum:
            totalNum = len(lines)
            average_energies = average_energies[:totalNum]
        energies_file.close()
        for j, line in enumerate(lines):
            if (j >= totalNum):
                break
            average_energies[j] += float(line)
        ax1.plot(list(range(len(average_energies))), average_energies, linewidth=0.6)
    plt.legend()
    plt.show()


def plot_average(foldername):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    for language_type in ["None", "Evolved", "External"]:
        average_energies = [0 for i in range(1001)]
        totalNum = 1001
        for i in range(10):
            energies_file = open(foldername + "/" + language_type + str(i) + "/energies.txt", "r")
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


def plot_language_distributions(foldername, generations):
    fig = plt.figure()
    for j, gen in enumerate(generations):
        for i, language in enumerate(["edible", "poisonous"]):
            languages = [0, 0, 0, 0, 0, 0, 0, 0]
            with open(foldername + "/" + language + str(gen) + ".txt", "r") as language_file:
                num_samples = 0
                for sample in language_file.readlines():
                    languages[int(sample[0])] += 1
                    num_samples += 1
                for t in range(len(languages)):
                    languages[t] /= num_samples
            ax = fig.add_subplot(len(generations), 2, i + 1 + j * 2)
            plt.setp(ax.get_yticklabels(), visible=False)
            if i == 0:
                ax.set_ylabel(str(gen),
                              rotation="horizontal",
                              verticalalignment="center",
                              horizontalalignment="right",
                              size="small")
            if j < len(generations) - 1:
                plt.setp(ax.get_xticklabels(), visible=False)
            ax.plot([str(bin(i))[2:] for i in range(8)], languages)
            ax.tick_params(axis='x', labelsize="small")
    plt.gcf().subplots_adjust(left=0.15)
    plt.show()


def plot_language_distributions_bar(foldername, generations):

    width = 0.35
    labels = [str(bin(i))[2:] for i in range(8)]
    x = np.arange(len(labels))

    fig = plt.figure()
    for j, gen in enumerate(generations):

        ax = fig.add_subplot(len(generations), 1, j + 1)

        for i, language in enumerate(["edible", "poisonous"]):
            languages = [0, 0, 0, 0, 0, 0, 0, 0]
            with open(foldername + "/" + language + str(gen) + ".txt", "r") as language_file:
                num_samples = 0
                for sample in language_file.readlines():
                    languages[int(sample[0])] += 1
                    num_samples += 1
                for t in range(len(languages)):
                    languages[t] /= num_samples

                rects = ax.bar(x + pow(-1, i) * width / 2, languages, width, label=language)

        ax.set_ylabel(str(gen),
                      rotation="horizontal",
                      verticalalignment="center",
                      horizontalalignment="right",
                      size="small")
        if j == 0:
            ax.set_title('Language Frequency Distribution')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, size="small")
        plt.setp(ax.get_yticklabels(), visible=False)
        if j < len(generations) - 1:
            plt.setp(ax.get_xticklabels(), visible=False)

    plt.legend()
    plt.gcf().subplots_adjust(left=0.15)
    plt.show()


def get_QI(foldername, generations, k=1):
    """ Calculates the quality index for each generation where k is a constant
    to weigh the effect of the internal dispersion value of poisonous or edible mushrooms.
    """

    qis = []
    for gen in generations:
        production_table = {
            "edible": [0, 0, 0, 0, 0, 0, 0, 0],
            "poisonous": [0, 0, 0, 0, 0, 0, 0, 0]
        }
        # Create production table, storing the frequencies of each signal
        for language in production_table:
            with open(foldername + "/language/" + language + str(gen) + ".txt", "r") as sample_file:
                samples = [int(sample) for sample in sample_file.readlines()]
                for sample in samples:
                    production_table[language][sample] += 1
                for i in range(8):
                    production_table[language][i] /= len(samples)

        # Calculate the dispersion values
        d_edible = sum([abs(frequency - 0.125) for frequency in production_table["edible"]])
        d_poisonous = sum([abs(frequency - 0.125) for frequency in production_table["poisonous"]])

        # Calculate quality index
        qi = sum([
            abs(production_table["edible"][i] - production_table["poisonous"][i]) for i in range(8)
        ]) - k * min(d_edible, d_poisonous)
        qis.append(qi * 100 / 3.75)

    return qis


def frequency_and_qi(foldername, generations):

    # Get QI scores for each generation
    qis = get_QI(foldername, generations)

    # Get fitness scores
    energies_file = open(foldername + "/energies.txt", "r")
    average_energies = []
    lines = energies_file.readlines()
    energies_file.close()
    for line in lines:
        average_energies.append(float(line))

    # Calculate correlation
    print("Correlation:", pearsonr(average_energies, qis))

    # Create figure
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(list(range(len(average_energies))),
             average_energies,
             label="average energy",
             linewidth=1.0)
    ax1.plot(generations, qis, label="Quality Index", linewidth=1.0)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    style.use('fivethirtyeight')
    #plotTen(str(sys.argv[1]))
    #plotOne(str(sys.argv[1]))
    plot_average(str(sys.argv[1]))
    #plotTenEvolved(str(sys.argv[1]), sys.argv[2])
    #for j in range(10):
    #    plotLanguageDistributionsBar(str(sys.argv[1]) + "/Evolved" + str(j) + "/language/", [i * 100 for i in range(11)])
    #frequency_and_qi(str(sys.argv[1]), [i for i in range(1001)])
