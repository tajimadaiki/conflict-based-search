import time
from typing import Dict, List, Tuple
from agent import Agent
from planner import Planner
import numpy as np
import random
import map_reader
import copy
import matplotlib.pyplot as plt


def main():

    grid_size_x, grid_size_y, static_obstacles, end_points = map_reader.load_file('./map/11x11.map')
    agent_num = 8
    print(f"x:{grid_size_x}, y:{grid_size_y}, agent:{agent_num}")
    agents = [Agent(i) for i in range(agent_num)]
    planner = Planner(agents, grid_size_x, grid_size_y, static_obstacles)

    trials_num = 50
    successes_num = 0
    sum_of_exe_time = 0
    exe_times = []
    for _ in range(trials_num):
        start_time = time.time()
        starts = {}
        goals = {}
        end_points_copy = copy.copy(end_points)
        goal_pos_flag = [2 for _ in range(grid_size_x)]
        for agent in agents:
            start_pos = random.choice(end_points_copy)
            starts[agent] = start_pos
            end_points_copy.remove(start_pos)
            while True:
                goal_pos = random.choice(end_points_copy)
                goal_x = goal_pos[0]
                if goal_pos_flag[goal_x] > 0:
                    goal_pos_flag[goal_x] -= 1
                    break
            goals[agent] = goal_pos
            end_points_copy.remove(goal_pos)

        solution = planner.plan(starts, goals)

        end_time = time.time()
        if solution is not None:
            successes_num += 1
            exe_time = end_time - start_time
            sum_of_exe_time += exe_time
            exe_times.append(exe_time)
            print(f"{exe_time}")

    exe_time_average = sum_of_exe_time/successes_num
    print(f"{exe_time_average} sec")
    successes_ratio = successes_num/trials_num*100
    print(f"{successes_ratio}%")
    plot_hist(exe_times)


def plot_hist(data: List, save_fig: bool = False, agent_num: int = 0, trials_num: int = 0, map_name: str = ""):
    np_data = np.array(data)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.hist(np_data, bins=50, range=(0, 10), color='blue', ec='black')
    ax.set_title(f'Execution time (agent:{agent_num})')
    ax.set_xlabel('time')
    if save_fig:
        plt.savefig(f"./fig/exe_time_{agent_num}agents_{trials_num}trials_{map_name}.png")
    plt.show()


if __name__ == "__main__":
    main()
