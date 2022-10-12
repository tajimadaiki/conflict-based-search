import time
from typing import Dict, List, Tuple
from agent import Agent
from planner import Planner
from visualizer import Visualizer
import random
import map_reader
import copy


def main():

    grid_size_x, grid_size_y, static_obstacles, end_points = map_reader.load_file('./map/kvc.map')
    agent_num = 5
    print(f"x:{grid_size_x}, y:{grid_size_y}, agent:{agent_num}")
    agents = [Agent(i) for i in range(agent_num)]
    planner = Planner(agents, grid_size_x, grid_size_y, static_obstacles)

    trials_num = 50
    successes_num = 0
    sum_of_exe_time = 0
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
            print(f"calculate solution: {exe_time}")

    exe_time_average = sum_of_exe_time/successes_num
    print(f"{exe_time_average} sec")
    successes_ratio = successes_num/trials_num*100
    print(f"{successes_ratio}%")


if __name__ == "__main__":
    main()
