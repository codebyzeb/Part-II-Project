import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')


class Plotter:

    generations = []
    average_energies = []

    ax = None

    def __init__(self):
        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(1, 1, 1)
        #a = animation.FuncAnimation(fig, self.update, frames=1000)
        plt.show()
        plt.pause(0.1)

    def add_point(self, generation, average_energy):
        self.generations.append(generation)
        self.average_energies.append(average_energy)
        self.update(0)

    def update(self, i):
        self.ax.clear()
        self.ax.plot(self.generations, self.average_energies)
        plt.draw()
        plt.pause(0.01)
