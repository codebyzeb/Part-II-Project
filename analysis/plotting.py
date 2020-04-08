"""
Analysis module used for plotting graphs of the simulation
"""

import argparse
import matplotlib.pyplot as plt
from matplotlib import style
from scipy.stats import pearsonr
import sys
import pickle
import numpy as np


class Plotter:
    """ Represents a simulation environment for a population of entities.

    Attributes:
        generations: The x-axis, the generation number
        average_entities: The y-axis, the average energy of the population over generation count
        ax: The axis plotted
    """

    generations = []
    average_fitness = []

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
        self.average_fitness.append(average_energy)
        self.ax.clear()
        self.ax.plot(self.generations, self.average_fitness)
        plt.draw()
        plt.pause(0.01)


def plot_one(foldername, num=1000):
    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.set_title("Average Fitness")
    ax.grid(linestyle='-')

    # Get data
    fitness_file = open(foldername + "/fitness.txt", "r")
    average_fitness = []
    lines = fitness_file.readlines()
    fitness_file.close()
    for j, line in enumerate(lines):
        if j >= num:
            break
        average_fitness.append(float(line))

    # Show plot
    ax.plot(list(range(len(average_fitness))),
            average_fitness,
            label="Average Fitness",
            linewidth=1.0)
    plt.show()


def plot_ten(foldername, num=1000):
    fig = plt.figure()
    ax = fig.add_subplot(1111)
    # ax.set_title("Average fitness for ten replicas")
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")

    # Plot ten subgraphs
    for i in range(10):
        # Set up axis
        ax = fig.add_subplot(5, 2, i + 1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(linestyle='-')

        # Get data
        for language_type in ["none", "evolved", "external"]:
            fitness_file = open(foldername + "/" + language_type + str(i) + "/fitness.txt", "r")
            average_fitness = []
            lines = fitness_file.readlines()
            fitness_file.close()
            for j, line in enumerate(lines):
                if (j >= num):
                    break
                average_fitness.append(float(line))

            # Plot data
            ax.plot(list(range(len(average_fitness))),
                    average_fitness,
                    label=language_type,
                    linewidth=1.0)

    # Show graph
    plt.legend()
    plt.show()


def plot_ten_language(foldername, language, num):
    # Set up figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")
    # ax.set_title("Average fitness for ten replicas of {0} language".format(language))
    ax.grid(linestyle='-')
    # ax.set_ylim([0, 450])

    # Get data
    for i in range(10):
        fitness_file = open(foldername + "/" + language + str(i) + "/fitness.txt", "r")
        lines = fitness_file.readlines()
        average_fitness = [0 for i in range(num)]
        totalNum = num
        if len(lines) <= totalNum:
            totalNum = len(lines)
            average_fitness = average_fitness[:totalNum]
        fitness_file.close()
        for j, line in enumerate(lines):
            if (j >= totalNum):
                break
            average_fitness[j] += float(line)

        # Plot graph
        ax.plot(list(range(len(average_fitness))), average_fitness, linewidth=0.6, label=i)
    plt.legend()
    plt.show()


def plot_average(foldername, num=1000):
    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.set_title("Average fitness")
    ax.set_xlabel("Generations")
    ax.set_ylabel("Fitness")
    ax.grid(linestyle='-')
    # ax.set_ylim([0, 450])

    # Get data
    for language_type in ["None", "Evolved", "External"]:
        average_fitness = [0 for i in range(num)]
        totalNum = num
        for i in range(10):
            fitness_file = open(foldername + "/" + language_type + str(i) + "/fitness.txt", "r")
            lines = fitness_file.readlines()
            if len(lines) < totalNum:
                totalNum = len(lines)
                average_fitness = average_fitness[:totalNum]
            fitness_file.close()
            for j, line in enumerate(lines):
                if (j >= totalNum):
                    break
                average_fitness[j] += (float(line) / 10)

        # Plot line
        ax.plot(list(range(len(average_fitness))),
                average_fitness,
                label=language_type,
                linewidth=1.0)
    plt.legend()
    plt.show()


def plot_language_distributions_bar(foldername, increment, num):

    generations = [i * increment for i in range(int(num / increment) + 1)]

    width = 0.35
    labels = [str(bin(i))[2:].zfill(3) for i in range(8)]
    x = np.arange(len(labels))

    fig = plt.figure()

    # Set up main axis for title and labels
    axmain = fig.add_subplot(111)
    axmain.spines['top'].set_color('none')
    axmain.spines['bottom'].set_color('none')
    axmain.spines['left'].set_color('none')
    axmain.spines['right'].set_color('none')
    axmain.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    # axmain.set_title('Language Frequency Distribution')

    # Get data
    language = pickle.load(open(foldername + "/language.p", 'rb'))

    # Plot a frequency distribution for each generation in the list
    for j, gen in enumerate(generations):

        # Create subplot and remove ticks
        ax = fig.add_subplot(len(generations), 1, j + 1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        axmain.set_ylabel('generation')
        axmain.set_xlabel('signal')

        # Set label and ticks
        ax.set_ylabel(str(gen),
                      rotation="horizontal",
                      verticalalignment="center",
                      horizontalalignment="right",
                      size="small")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, size="small")
        plt.setp(ax.get_yticklabels(), visible=False)
        ax.get_yaxis().set_ticks([])
        if j < len(generations) - 1:
            plt.setp(ax.get_xticklabels(), visible=False)

        # Set axis height
        ax.set_ylim([0, 1])

        # Plot data
        rects = ax.bar(x + pow(-1, 1) * width / 2,
                       language[gen]["edible"],
                       width,
                       label="edible",
                       color='red')
        rects = ax.bar(x + pow(-1, 2) * width / 2,
                       language[gen]["poisonous"],
                       width,
                       label="poisonous",
                       color='blue')

        # Plot legend half way up
        if gen == generations[len(generations) // 2]:
            ax.legend()

    plt.gcf().subplots_adjust(left=0.15)
    plt.show()


def get_QI(foldername, generations, k=1):
    """ Calculates the quality index for each generation where k is a constant
    to weigh the effect of the internal dispersion value of poisonous or edible mushrooms.
    """

    qis = []

    # Get data
    language = pickle.load(open(foldername + "/language.p", 'rb'))

    for gen in generations:

        # Calculate the dispersion values
        d_edible = sum([abs(frequency - 0.125) for frequency in language[gen]["edible"]])
        d_poisonous = sum([abs(frequency - 0.125) for frequency in language[gen]["poisonous"]])

        # Calculate quality index
        qi = sum(
            [abs(language[gen]["edible"][i] - language[gen]["poisonous"][i])
             for i in range(8)]) + k * min(d_edible, d_poisonous)
        qis.append(qi * 100 / 3.75)

    return qis


def frequency_and_qi(foldername, increment, num):

    generations = [i * increment for i in range(int(num / increment) + 1)]

    # Get QI scores for each generation
    qis = get_QI(foldername, generations)

    # Get fitness scores
    fitness_file = open(foldername + "/fitness.txt", "r")
    average_fitness = []
    lines = fitness_file.readlines()
    fitness_file.close()
    for i, line in enumerate(lines):
        if i in generations:
            average_fitness.append(float(line))

    # Calculate correlation
    print("Correlation:", pearsonr(average_fitness, qis))

    # Plot average fitness
    fig, ax1 = plt.subplots()
    l1, = ax1.plot(generations, average_fitness, label="Average fitness", linewidth=1.0, color='r')
    ax1.set_ylabel("Fitness")

    # Plot QI score
    ax2 = ax1.twinx()
    ax2.set_ylim([0, 100])
    l2, = ax2.plot(generations, qis, label="Quality Index", linewidth=1.0, color='b')
    ax2.set_ylabel("Quality")
    plt.legend([l1, l2], ["Average fitness", "Quality Index"])
    plt.show()


def qi_all(foldername, increment, num):

    generations = [i * increment for i in range(int(num / increment) + 1)]

    # Get QI scores for each generation for each repeat
    qis_all = []
    fitness_all = []
    for i in range(10):
        qis = get_QI(foldername + str(i), generations)
        qis_all.extend(qis)

        # Get fitness scores
        fitness_file = open(foldername + str(i) + "/fitness.txt", "r")
        average_fitness = []
        lines = fitness_file.readlines()
        fitness_file.close()
        for i, line in enumerate(lines):
            if i in generations:
                average_fitness.append(float(line))
        fitness_all.extend(average_fitness)

        # Calculate correlation
        print("Correlation:", pearsonr(average_fitness, qis))
    # Calculate correlation
    print("Full Correlation:", pearsonr(fitness_all, qis_all))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Conduct Analysis of Simulation')
    parser.add_argument(
        'type',
        type=str,
        choices=['average', 'ten', 'ten-language', 'single', 'language', 'qi', 'qi-all'],
        help='type of graph to display')
    parser.add_argument('foldername', type=str, help="where data is stored")
    parser.add_argument('-n',
                        '--num_gen',
                        action='store',
                        type=int,
                        default=2000,
                        help='number of generations to display')
    parser.add_argument('-l',
                        '--language',
                        action='store',
                        type=str,
                        default="Evolved",
                        help='language type to display')
    parser.add_argument('-i',
                        '--increment',
                        action='store',
                        type=int,
                        default=100,
                        help='language increment')

    args, unknown = parser.parse_known_args()

    #style.use('fivethirtyeight')
    style.use('seaborn-bright')

    if args.type == "average":
        plot_average(args.foldername, args.num_gen)
    elif args.type == "ten":
        plot_ten(args.foldername, args.num_gen)
    elif args.type == "single":
        plot_one(args.foldername, args.num_gen)
    elif args.type == "ten-language":
        plot_ten_language(args.foldername, args.language, args.num_gen)
    elif args.type == "language":
        plot_language_distributions_bar(args.foldername, args.increment, args.num_gen)
    elif args.type == "qi":
        frequency_and_qi(args.foldername, args.increment, args.num_gen)
    elif args.type == "qi-all":
        qi_all(args.foldername, args.increment, args.num_gen)
