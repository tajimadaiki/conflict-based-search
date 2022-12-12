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

    planner = ConflictBasedSearch(config.agents, config.map)
    intermediate_time = time.time()
    print(f"create planner: {intermediate_time - start_time}")

    starts = {config.agents[0]: (5, 5), config.agents[1]: config.chargers['charger_2']}
    goals = {config.agents[0]: config.endpoints['con_6_6'], config.agents[1]: config.endpoints['con_6_2']}
    print(f'starts: {starts}')
    print(f'goals: {goals}')

    solution = planner.plan(starts, goals)

    end_time = time.time()
    print(f"calculate solution: {end_time - intermediate_time}")

    visualizer = Visualizer(config, solution)
    visualizer.plot(True, 'kamigo_1')


if __name__ == "__main__":
    main()
