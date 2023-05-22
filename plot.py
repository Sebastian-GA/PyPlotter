from tkinter import Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib import animation
import collections

from constants import *


class Plot(Frame):
    def __init__(self, master, device, *args):
        super().__init__(master, *args)

        self.configure(bg=BG2)
        self.max_data = PLOT_X_LIM
        self.device = device
        self.data = device.signals[0]  # TODO: Plot multiple signals

        # Styling plot
        self.fig, ax = plt.subplots(facecolor=BG2, dpi=70, figsize=(1, 1))
        plt.title(PLOT_TITLE, color=FG, size=FONT[1], family=FONT[0])
        plt.xlim(0, PLOT_X_LIM)
        plt.ylim(PLOT_Y_LIMS)
        plt.xlabel("Samples", color=FG, size=FONT[1], family=FONT[0])
        plt.ylabel("Temperature (°C)", color=FG, size=FONT[1], family=FONT[0])

        ax.tick_params(
            direction="out", length=5, width=2, colors=FG, grid_color=FG, grid_alpha=0.5
        )
        ax.set_facecolor(BG1)
        ax.spines["bottom"].set_color(BG1)
        ax.spines["top"].set_color(BG1)
        ax.spines["left"].set_color(BG1)
        ax.spines["right"].set_color(BG1)

        # Styling plot line
        (self.line,) = ax.plot(
            [],
            [],
            color=PLOT_LINE_COLOR,
            marker="o",
            linewidth=2,
            markersize=5,
            markeredgecolor=PLOT_LINE_COLOR,
            markerfacecolor=PLOT_LINE_COLOR,
        )

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.start()

    def animate(self, i):
        # self.data.append(self.device.receive_data)
        self.line.set_data(range(self.max_data), self.data)

    def start(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100)
        self.canvas.draw()

    def pause(self):
        self.ani.event_source.stop()

    def clear(self):
        self.device.clear_data()
        self.line.set_data(range(self.max_data), self.data)
