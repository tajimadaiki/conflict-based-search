from typing import List, Tuple, Dict
import numpy as np
import heapq as hq
from agent import Agent
from constraints import Constraints
from constraint_tree_node import CTNode
from a_star import AStar


class Planner:

    def __init__(self,
                 agents: List[Agent],
                 grid_size_x: int,
                 grid_size_y: int,
                 static_obstacles: List[Tuple[int, int]]):
        self.agents = agents
        self.low_level_planner = AStar(grid_size_x, grid_size_y, static_obstacles)

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

        # start iteration
        while open_nodes:
            current_node = hq.heappop(open_nodes)
            if debug:
                print(f'conflict:{current_node.conflict}, num:{current_node.conflicts_num}')
            # get goal
            if current_node.conflicts_num == 0:
                return current_node.solution

            child_node_r, child_node_l = current_node.create_child_nodes()
            hq.heappush(open_nodes, child_node_r)
            hq.heappush(open_nodes, child_node_l)


if __name__ == "__main__":
    agent_num = 3
    agents = [Agent(i) for i in range(agent_num)]
    grid_size_x = 10
    grid_size_y = 10
    static_obstacles = [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)]

    planner = Planner(agents, grid_size_x, grid_size_y, static_obstacles)
    print("create planner!")

    starts = {agents[0]: (0, 1), agents[1]: (3, 1), agents[2]: (2, 4)}
    goals = {agents[0]: (3, 1), agents[1]: (0, 1), agents[2]: (2, 0)}

    solution = planner.plan(starts, goals, True)

    print(solution)
