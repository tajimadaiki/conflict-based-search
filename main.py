import time
from agent import Agent
from conflict_based_search import ConflictBasedSearch
from visualizer import Visualizer
from config import Config


def main():
    start_time = time.time()

    config = Config()
    config_file = "./config/config.xlsx"
    config.load_from_xlsx(config_file)

    planner = ConflictBasedSearch(config)
    intermediate_time = time.time()
    print(f"create planner: {intermediate_time - start_time}")

    starts = {config.agents[0]: (11, 0), config.agents[1]: (17, 4)}
    goals = {config.agents[0]: (16, 4), config.agents[1]: (17, 6)}
    print(f'starts: {starts}')
    print(f'goals: {goals}')

    solution = planner.plan(starts, goals)

    end_time = time.time()
    print(f"calculate solution: {end_time - intermediate_time}")

    visualizer = Visualizer(config, solution)
    visualizer.plot()


if __name__ == "__main__":
    main()
