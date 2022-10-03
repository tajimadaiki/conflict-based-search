from typing import Dict, List, Tuple
from agent import Agent
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches


class Visualizer:

    def __init__(self,
                 grid_size_x: int,
                 grid_size_y: int,
                 static_obstacles: List[Tuple[int, int]],
                 solution: Dict[Agent, np.ndarray],
                 step_div=10):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.static_obstacles = static_obstacles
        self.solution = solution
        self.traject: Dict[Agent, np.ndarray] = dict()
        self.step_div = step_div
        self.path_steps = 0
        self.traj_steps = 0
        self._make_traject()
        self._set_steps()

    def _set_steps(self):
        for path in self.solution.values():
            self.path_steps = max(self.path_steps, len(path))
        self.traj_steps = int(self.path_steps * self.step_div + 1)

    def _make_traject(self):
        for agent, path in self.solution.items():
            traj_x = np.array([])
            traj_y = np.array([])
            for step in range(len(path) - 1):
                traj_steps = self.step_div + 1
                traj_this_step_x = np.linspace(path[step][0], path[step + 1][0], traj_steps)
                traj_this_step_y = np.linspace(path[step][1], path[step + 1][1], traj_steps)
                traj_x = np.append(traj_x, traj_this_step_x)
                traj_y = np.append(traj_y, traj_this_step_y)
                if step + 2 is not len(path):
                    traj_x = np.delete(traj_x, len(traj_x) - 1)
                    traj_y = np.delete(traj_y, len(traj_y) - 1)
            self.traject[agent] = np.stack([traj_x, traj_y], 1)

    def plot(self, save=False):
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect=1)

        def plot_one_step(f):
            # clear pre step artists
            ax.cla()
            # set lim
            ax.set_xlim(-1, self.grid_size_x)
            ax.set_ylim(-1, self.grid_size_y)
            # set grid
            for x in range(self.grid_size_x + 1):
                ax.plot([x - 0.5, x - 0.5], [0 - 0.5, self.grid_size_y - 0.5], color="black")
            for y in range(self.grid_size_y + 1):
                ax.plot([0 - 0.5, self.grid_size_x - 0.5], [y - 0.5, y - 0.5], color="black")

            # plot agents
            for agent, pos in self.traject.items():
                # plot agents
                if f < len(pos):
                    c = patches.Circle(xy=(pos[f][0], pos[f][1]), radius=0.3, color="blue")
                else:
                    c = patches.Circle(xy=(pos[-1][0], pos[-1][1]), radius=0.3, color="red")
                ax.add_patch(c)
        interval_time = 1000/self.step_div
        anim = FuncAnimation(fig, plot_one_step, frames=self.traj_steps, interval=interval_time)
        if save:
            anim.save('anim.mp4', writer="ffmpeg")
        plt.show()


if __name__ == '__main__':
    agent_1 = Agent(1)
    agent_2 = Agent(2)
    grid_size_x = 15
    grid_size_y = 10
    static_obstacles = [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)]
    path_1 = np.array([[1, 2], [2, 2], [3, 2], [3, 3]])
    path_2 = np.array([[2, 2], [2, 3], [3, 3], [4, 3], [5, 3]])
    solution = {agent_1: path_1, agent_2: path_2}

    visualizer = Visualizer(grid_size_x, grid_size_y, static_obstacles, solution)
    visualizer.plot()
