import numpy as np
from typing import Dict, Tuple
from constraints import Constraints
from a_star import AStar
from agent import Agent
from itertools import combinations
from copy import deepcopy


class CTNode:

    def __init__(self,
                 constraints: Constraints,
                 solution: Dict[Agent, np.ndarray],
                 low_level_planner: AStar,
                 starts: Dict[Agent, Tuple[int, int]],
                 goals: Dict[Agent, Tuple[int, int]], ):
        self.constraints = constraints
        self.solution = solution
        self.cost = self.sic(solution)  # sum of individual costs
        self.low_level_planner = low_level_planner
        self.starts = starts
        self.goals = goals
        self.conflict = tuple()
        self.conflicts_num = int()
        self.search_conflicts()

    @staticmethod
    def sic(solution: Dict[Agent, np.ndarray]):  # sum of individual costs
        cost = 0
        for path in solution.values():
            cost += len(path)
        return cost

    def __lt__(self, other):
        if self.cost is not other.cost:
            return self.cost < other.cost
        else:
            return self.conflicts_num < other.conflicts_num  # tie-breaking implementation

    def create_child_nodes(self) -> Tuple['CTNode', 'CTNode']:

        # node conflict (agent_i, agent_j, pos, time)
        if len(self.conflict) == 4:
            # set params
            agent_i, agent_j, pos, time = self.conflict

            def node_conflict_child(agent_x, time_x, pos_x) -> 'CTNode':
                constraints_x = self.constraints.fork_node_conflict(agent_x, time_x, tuple(pos_x))

                # TODO 他のロボットの動き(dynamic_obstacle)を入力してa_starの中でタイブレークできるようにする
                path_x = self.low_level_planner.plan(self.starts[agent_x],
                                                     self.goals[agent_x],
                                                     constraints_on_node
                                                     =constraints_x.constraints_on_node.setdefault(agent_x, dict()),
                                                     constraints_on_edge
                                                     =constraints_x.constraints_on_edge.setdefault(agent_x, dict()))
                solution_x = deepcopy(self.solution)
                solution_x[agent_x] = path_x
                node_x = CTNode(constraints_x,
                                solution_x,
                                self.low_level_planner,
                                self.starts,
                                self.goals)
                return node_x

            return node_conflict_child(agent_i, time, pos), node_conflict_child(agent_j, time, pos)

        # edge conflict (agent_i, agent_j, pos_i, pos_j, time)
        if len(self.conflict) == 5:
            # set params
            agent_i, agent_j, pos_i, pos_j, time = self.conflict

            def edge_conflict_child(agent_x, time_x, pos_x_f, pos_x_t):
                constraints_x = self.constraints.fork_edge_conflict(agent_x, time_x, tuple(pos_x_f), tuple(pos_x_t))

                # TODO 他のロボットの動き(dynamic_obstacle)を入力してa_starの中でタイブレークできるようにする
                path_x = self.low_level_planner.plan(self.starts[agent_x],
                                                     self.goals[agent_x],
                                                     constraints_on_node
                                                     =constraints_x.constraints_on_node.setdefault(agent_x, dict()),
                                                     constraints_on_edge
                                                     =constraints_x.constraints_on_edge.setdefault(agent_x, dict()))
                solution_x = deepcopy(self.solution)
                solution_x[agent_x] = path_x
                node_x = CTNode(constraints_x,
                                solution_x,
                                self.low_level_planner,
                                self.starts,
                                self.goals)
                return node_x

            return edge_conflict_child(agent_i, time, pos_j, pos_i), edge_conflict_child(agent_j, time, pos_i, pos_j)

    # TODO 経路を入れ替えたエージェントだけ計算し直せるようにする
    def search_conflicts(self):
        # set agents
        agents = list(self.solution.keys())
        # set has_arrived flag
        has_arrived: Dict[Agent, bool] = dict()
        just_arrived: Dict[Agent, bool] = dict()
        for agent in agents:
            has_arrived[agent] = False
            just_arrived[agent] = False
        # set find conflict flag
        found_conflict = False
        # set max iter number
        max_iter = 500
        # start iteration
        time = 0
        while not all(has_arrived.values()) and time < max_iter:
            time += 1
            for agent_i, agent_j in combinations(agents, 2):
                # change arrived flag
                if len(self.solution[agent_i]) == time:
                    has_arrived[agent_i] = True
                    just_arrived[agent_i] = True
                else:
                    just_arrived[agent_i] = False

                if len(self.solution[agent_j]) == time:
                    has_arrived[agent_j] = True
                    just_arrived[agent_j] = True
                else:
                    just_arrived[agent_j] = False

                # find conflict
                pos_i = self.solution[agent_i][time] if not has_arrived[agent_i] else self.solution[agent_i][-1]
                pos_j = self.solution[agent_j][time] if not has_arrived[agent_j] else self.solution[agent_j][-1]
                pre_pos_i = self.solution[agent_i][time - 1] \
                    if not has_arrived[agent_i] or just_arrived[agent_i] \
                    else self.solution[agent_i][-1]
                pre_pos_j = self.solution[agent_j][time - 1] \
                    if not has_arrived[agent_j] or just_arrived[agent_j] \
                    else self.solution[agent_j][-1]
                # node conflict
                if all(pos_i == pos_j):
                    self.conflicts_num += 1
                    if not found_conflict:
                        found_conflict = True
                        self.conflict = (agent_i, agent_j, pos_i, time)
                # edge conflict
                if all(pos_i == pre_pos_j) and all(pos_j == pre_pos_i):
                    self.conflicts_num += 1
                    if not found_conflict:
                        found_conflict = True
                        # agent_i: pos_j -> pos_i (time-1 ~ time)
                        self.conflict = (agent_i, agent_j, pos_i, pos_j, time)


if __name__ == "__main__":
    # make planner
    agent_num = 3
    agents = [Agent(i) for i in range(agent_num)]
    grid_size_x = 10
    grid_size_y = 10
    static_obstacles = [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)]

    planner = AStar(grid_size_x, grid_size_y, static_obstacles)

    starts = {agents[0]: (0, 1), agents[1]: (1, 0), agents[2]: (2, 4)}
    goals = {agents[0]: (4, 1), agents[1]: (1, 4), agents[2]: (2, 0)}

    constraints_0 = Constraints()
    agent_1 = Agent(1)
    agent_2 = Agent(2)
    agent_3 = Agent(3)
    constraints_1 = constraints_0.fork_node_conflict(agent_1, 35, (5, 8))
    constraints_2 = constraints_1.fork_node_conflict(agent_1, 35, (3, 4))

    solution = {agent_1: np.array([[1, 2], [2, 2], [2, 3], [2, 3], [4, 4], [3, 4]]),
                agent_2: np.array([[1, 2], [1, 2], [2, 3], [3, 5], [3, 4], [4, 4]]),
                agent_3: np.array([[4, 3], [5, 4], [3, 5]])}

    node = CTNode(constraints_2, solution, planner, starts, goals)
    print(node.conflicts_num)
    print(node.conflict)
    print(node.cost)
