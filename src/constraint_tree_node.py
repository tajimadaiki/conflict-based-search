import numpy as np
from typing import Dict
from constraints import Constraints
from agent import Agent
from itertools import combinations


class CTNode:

    def __init__(self,
                 constraints: Constraints,
                 solution: Dict[Agent, np.ndarray]):
        self.constraints = constraints
        self.solution = solution
        self.cost = self.sic(solution)  # sum of individual costs
        self.parent_node = None
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
        step = 0
        while not all(has_arrived.values()) and step < max_iter:
            step += 1
            for agent_i, agent_j in combinations(agents, 2):
                # change arrived flag
                if len(self.solution[agent_i]) == step:
                    has_arrived[agent_i] = True
                    just_arrived[agent_i] = True
                else:
                    just_arrived[agent_i] = False

                if len(self.solution[agent_j]) == step:
                    has_arrived[agent_j] = True
                    just_arrived[agent_j] = True
                else:
                    just_arrived[agent_j] = False

                # find conflict
                pos_i = self.solution[agent_i][step] if not has_arrived[agent_i] else self.solution[agent_i][-1]
                pos_j = self.solution[agent_j][step] if not has_arrived[agent_j] else self.solution[agent_j][-1]
                pre_pos_i = self.solution[agent_i][step - 1] \
                    if not has_arrived[agent_i] or just_arrived[agent_i] \
                    else self.solution[agent_i][-1]
                pre_pos_j = self.solution[agent_j][step - 1] \
                    if not has_arrived[agent_j] or just_arrived[agent_j] \
                    else self.solution[agent_j][-1]
                # node conflict
                if all(pos_i == pos_j):
                    self.conflicts_num += 1
                    if not found_conflict:
                        found_conflict = True
                        self.conflict = (agent_i, agent_j, pos_i, step)
                # edge conflict
                if all(pos_i == pre_pos_j) and all(pos_j == pre_pos_i):
                    self.conflicts_num += 1
                    if not found_conflict:
                        found_conflict = True
                        # agent_i: pos_j -> pos_i (step-1 ~ step)
                        self.conflict = (agent_i, agent_j, pos_i, pos_j, step)


if __name__ == "__main__":
    constraints_0 = Constraints()
    agent_1 = Agent(1)
    agent_2 = Agent(2)
    agent_3 = Agent(3)
    constraints_1 = constraints_0.fork(agent_1, 35, (5, 8))
    constraints_2 = constraints_1.fork(agent_1, 35, (3, 4))

    solution = {agent_1: np.array([[1, 2], [2, 2], [2, 3], [2, 3], [4, 4], [3, 4]]),
                agent_2: np.array([[1, 2], [1, 2], [2, 3], [3, 5], [3, 4], [4, 4]]),
                agent_3: np.array([[4, 3], [5, 4], [3, 5]])}

    node = CTNode(constraints_2, solution)
    print(node.conflicts_num)
    print(node.conflict)
    print(node.cost)
