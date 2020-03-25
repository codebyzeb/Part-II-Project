"""
Analysis module used for plotting graphs of the simulation
"""

import argparse
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import numpy as np


def one_generation(foldername, generation):
    # Get data
    entities = pickle.load(
        open(foldername + "/populations/generation{0}.p".format(generation), 'rb'))
    labels = list(range(100))

    flatten = 'F'
    data = [[], [], [], []]
    for entity in entities:
        b1 = entity.biases[1].flatten(flatten)
        data[0].append(b1)
        w1 = entity.weights[1].flatten(flatten)
        data[1].append(w1)
        b2 = entity.biases[2].flatten(flatten)
        data[2].append(b2)
        w2 = entity.weights[2].flatten(flatten)
        data[3].append(w2)

    return data, labels, "Entity"


def one_generation_flattened(foldername, generation):
    # Get data
    entities = pickle.load(
        open(foldername + "/populations/generation{0}.p".format(generation), 'rb'))
    labels = list(range(100))

    flatten = 'F'
    data = [[], []]
    for entity in entities:
        # Flatten the network
        b1 = entity.biases[1]
        w1 = entity.weights[1]
        b2 = entity.biases[2]
        w2 = entity.weights[2]
        weights = w2.dot(w1)
        data[1].append(weights.flatten(flatten))
        biases = w2.dot(b1) + b2
        data[0].append(biases.flatten(flatten))

    return data, labels, "Entity"


def ten_replicas_flattened(foldername, generation):
    # Get data
    flatten = 'F'
    data = [[], []]
    labels = [0, 3, 4, 5, 6, 7, 1, 2, 8, 9]
    #labels = [0, 7, 9]

    for i in labels:
        entities = pickle.load(
            open(foldername + str(i) + "/populations/generation{0}.p".format(generation), 'rb'))
        entity = entities[0]
        # Flatten the network
        b1 = entity.biases[1]
        w1 = entity.weights[1]
        b2 = entity.biases[2][:2]
        w2 = entity.weights[2][:2]
        weights = w2.dot(w1)
        print(weights.shape)
        print("here")
        data[1].append(weights.flatten(flatten))
        biases = w2.dot(b1) + b2
        print(w2.dot(b1).shape)
        data[0].append(biases.flatten(flatten))

    return data, labels, "Replica"


def many_generations(foldername, generation):
    flatten = 'F'
    data = [[], [], [], []]
    labels = [i * 50 for i in range(generation // 50 + 1)]
    labels.reverse()

    for generation in labels:
        entities = pickle.load(
            open(foldername + "/populations/generation{0}.p".format(generation), 'rb'))
        entity = entities[0]
        weights = entity.biases[1].flatten(flatten)
        data[0].append(weights)
        weights = entity.weights[1].flatten(flatten)
        data[1].append(weights)
        weights = entity.biases[2].flatten(flatten)
        data[2].append(weights)
        weights = entity.weights[2].flatten(flatten)
        data[3].append(weights)

    return data, labels, "Generation"


def display_heatmap_flattened(data, labels, ylabel):
    # Set up plot
    pc_kwargs = {
        'rasterized': True,
        'cmap': 'RdBu',
        'vmin': -2,
        'vmax': 2
    }  #, 'edgecolors':'grey', 'linewidths':[.5, 4]}

    skip = 1

    # Get axes
    fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 28]})

    # Plot first set of weights
    ax1.get_xaxis().set_ticklabels([])
    ax1.get_yaxis().set_ticks(list(range(0, len(labels), skip)))
    ax1.get_yaxis().set_ticklabels(['%d' % val for val in labels[::skip]])
    ax1.yaxis.set_label_position('left')
    ax1.set_xlabel("B'")
    ax1.set_ylabel(ylabel)
    im1 = ax1.pcolor(data[0], **pc_kwargs)

    # Plot first set of biases
    ax2.get_xaxis().set_ticklabels([])
    ax2.get_yaxis().set_ticklabels([])
    ax2.yaxis.set_label_position('left')
    ax2.set_xlabel("W'")
    im2 = ax2.pcolor(data[1], **pc_kwargs)

    fig.colorbar(im2, ax=ax2, shrink=1)

    plt.show()


def display_heatmap(data, labels, ylabel):
    # Set up plot
    pc_kwargs = {
        'rasterized': True,
        'cmap': 'RdBu',
        'vmin': -2,
        'vmax': 2
    }  #, 'edgecolors':'grey', 'linewidths':[.5, 4]}

    # Get axes
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, gridspec_kw={'width_ratios': [5, 70, 5, 25]})

    # Plot first set of weights
    ax1.get_xaxis().set_ticklabels([])
    ax1.get_yaxis().set_ticks(list(range(0, len(labels), 8)))
    ax1.get_yaxis().set_ticklabels(['%d' % val for val in labels[::8]])
    ax1.yaxis.set_label_position('left')
    ax1.set_xlabel("B1")
    ax1.set_ylabel(ylabel)
    im1 = ax1.pcolor(data[0], **pc_kwargs)

    # Plot first set of biases
    ax2.get_xaxis().set_ticklabels([])
    ax2.get_yaxis().set_ticklabels([])
    ax2.yaxis.set_label_position('left')
    ax2.set_xlabel("W1")
    im2 = ax2.pcolor(data[1], **pc_kwargs)

    # Plot second set of weights
    ax3.get_xaxis().set_ticklabels([])
    ax3.get_yaxis().set_ticklabels([])
    ax3.yaxis.set_label_position('left')
    ax3.set_xlabel("B2")
    im3 = ax3.pcolor(data[2], **pc_kwargs)

    # Plot first set of biases
    ax4.get_xaxis().set_ticklabels([])
    ax4.get_yaxis().set_ticklabels([])
    ax4.yaxis.set_label_position('left')
    ax4.set_xlabel("W2")
    im4 = ax4.pcolor(data[3], **pc_kwargs)

    fig.colorbar(im4, ax=ax4, shrink=1)

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display heatmap of entity weights')
    parser.add_argument('type',
                        type=str,
                        choices=['one_full', 'many_full', 'one_flat', 'ten_flat'],
                        help='type of graph to display')
    parser.add_argument('foldername', type=str, help="where data is stored")
    parser.add_argument('generation', type=int, default=0, help="generation to load")
    parser.add_argument('-e',
                        '--entity',
                        action='store',
                        type=int,
                        default=0,
                        help='entity in the list whose network you want to display')
    args, unknown = parser.parse_known_args()

    if args.type == "one_flat":
        data, labels, ylabel = one_generation_flattened(args.foldername, args.generation)
        display_heatmap_flattened(data, labels, ylabel)
    elif args.type == "ten_flat":
        data, labels, ylabel = ten_replicas_flattened(args.foldername, args.generation)
        display_heatmap_flattened(data, labels, ylabel)
    elif args.type == "one_full":
        data, labels, ylabel = one_generation(args.foldername, args.generation)
        display_heatmap(data, labels, ylabel)
    elif args.type == "many_full":
        data, labels, ylabel = many_generations(args.foldername, args.generation)
        display_heatmap(data, labels, ylabel)

    #style.use('fivethirtyeight')
    style.use('seaborn-bright')
