import time
from typing import Dict, List, Tuple
from agent import Agent
from planner import Planner
from visualizer import Visualizer
import random


agent_num = 5
agents = [Agent(i) for i in range(agent_num)]
grid_size_x = 21
grid_size_y = 6
static_obstacles = []
possible_zone = []
for x in range(grid_size_x):
    for y in range(grid_size_y):
        if x%2==1 and 1<=y<=4:
            static_obstacles.append((x, y))
        else:
            possible_zone.append((x, y))

# print(random.sample(possible_zone, 1))

start_time = time.time()
planner = Planner(agents, grid_size_x, grid_size_y, static_obstacles)
intermediate_time = time.time()
print(f"create planner: {intermediate_time-start_time}")


starts = {}
goals = {}
for agent in agents:
    start_pos = random.choice(possible_zone)
    starts[agent] = start_pos
    possible_zone.remove(start_pos)
    #
    goal_pos = random.choice(possible_zone)
    goals[agent] = goal_pos
    possible_zone.remove(goal_pos)
    #
print(starts, goals)

solution = planner.plan(starts, goals, True)

end_time = time.time()
print(f"calculate solution: {end_time-intermediate_time}")

visualizer = Visualizer(grid_size_x, grid_size_y, static_obstacles, solution)
visualizer.plot()

