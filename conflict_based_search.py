from typing import List, Tuple, Dict
import numpy as np
import heapq as hq
from agent import Agent
from constraints import Constraints
from constraint_tree_node import CTNode
from a_star import AStar
from config import Config
import time


class ConflictBasedSearch:

    def __init__(self,
                 config: Config):
        self.agents = config.agents
        self.low_level_planner = AStar(config.map)

    def plan(self,
             starts: Dict[Agent, Tuple[int, int]],
             goals: Dict[Agent, Tuple[int, int]],
             debug: bool = False) -> Dict[Agent, np.ndarray]:

        # create initial CT node
        solution: Dict[Agent, np.ndarray] = dict()
        for agent in self.agents:
            path = self.low_level_planner.plan(starts[agent], goals[agent])
            solution[agent] = path
        constraints = Constraints()
        node = CTNode(constraints,
                      solution,
                      self.low_level_planner,
                      starts,
                      goals)

        open_nodes = [node]
        hq.heapify(open_nodes)

        start_time = time.time()
        # start iteration
        while open_nodes:
            current_time = time.time()
            if current_time - start_time > 10:
                print("Not found!")
                return None
            current_node = hq.heappop(open_nodes)
            if debug:
                print(f'conflict:{current_node.conflict}, num:{current_node.conflicts_num}')
                if current_node.conflicts_num != 0:
                    agent_r = current_node.conflict[0]
                    agent_l = current_node.conflict[1]
                    print(f'agent_r: {len(current_node.solution[agent_r])}, agent_l: {len(current_node.solution[agent_l])}')

            # get goal
            if current_node.conflicts_num == 0:
                return current_node.solution

            child_node_r, child_node_l = current_node.create_child_nodes()
            if child_node_r is not None:
                hq.heappush(open_nodes, child_node_r)
            if child_node_l is not None:
                hq.heappush(open_nodes, child_node_l)


if __name__ == "__main__":
    from config import Config
    config_file = "./config/config.xlsx"
    config = Config(config_file)

    planner = ConflictBasedSearch(config)
    print("create planner!")

    starts = {config.agents[0]: (11, 0), config.agents[1]: (17, 4)}
    goals = {config.agents[0]: (16, 4), config.agents[1]: (17, 6)}

    solution = planner.plan(starts, goals, True)

    print(solution)
