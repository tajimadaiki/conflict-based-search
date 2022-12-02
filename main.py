import time
from agent import Agent
from conflict_based_search import ConflictBasedSearch
from visualizer import Visualizer
import random


def main():
    start_time = time.time()

    agent_num = 3
    agents = [Agent(str(i)) for i in range(agent_num)]
    excel_map_file = "./config/config.xlsx"
    planner = ConflictBasedSearch(agents, excel_map_file)
    intermediate_time = time.time()
    print(f"create planner: {intermediate_time - start_time}")

    starts = {agents[0]: (11, 0), agents[1]: (17, 4), agents[2]: (17, 5)}
    goals = {agents[0]: (16, 4), agents[1]: (17, 6), agents[2]: (11, 1)}
    print(starts, goals)

    solution = planner.plan(starts, goals)

    end_time = time.time()
    print(f"calculate solution: {end_time - intermediate_time}")

    visualizer = Visualizer(excel_map_file, solution)
    visualizer.plot()


if __name__ == "__main__":
    main()
