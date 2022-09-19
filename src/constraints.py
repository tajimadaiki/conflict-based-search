from typing import Dict, Tuple, Set
from copy import deepcopy
from agent import Agent


class Constraints:

    def __init__(self):
        self.constraints: Dict[Agent, Dict[int, Set[Tuple[int, int]]]] = dict()
        self.constraints_on_edge: Dict[Agent, Dict[int, Dict[Tuple[int, int], Set[Tuple[int, int]]]]] = dict()

    def fork(self, agent: Agent, time: int, obstacle: Tuple[int, int]) -> 'Constraints':
        # copy constrains and insert constrain
        constraints_copy = deepcopy(self.constraints)
        constraints_on_edge_copy = deepcopy(self.constraints_on_edge)
        constraints_copy.setdefault(agent, dict()).setdefault(time, set()).add(obstacle)
        # create new constrain instance
        new_constraints = Constraints()
        new_constraints.constraints = constraints_copy
        new_constraints.constraints_on_edge = constraints_on_edge_copy
        return new_constraints

    def fork_edge_conflict(self,
                           agent: Agent,
                           time: int,
                           obstacle_f: Tuple[int, int],
                           obstacle_t: Tuple[int, int]) -> 'Constraints':
        # copy constrains and insert constrain
        constraints_copy = deepcopy(self.constraints)
        constraints_on_edge_copy = deepcopy(self.constraints_on_edge)
        constraints_on_edge_copy\
            .setdefault(agent, dict())\
            .setdefault(time, dict())\
            .setdefault(obstacle_f, set()).add(obstacle_t)
        # create new constrain instance
        new_constraints = Constraints()
        new_constraints.constraints = constraints_copy
        new_constraints.constraints_on_edge = constraints_on_edge_copy
        return new_constraints

    def __str__(self):
        return "node_conf:" + str(self.constraints) + \
               "edge_conf:" + str(self.constraints_on_edge)


if __name__ == "__main__":
    constraints_0 = Constraints()
    agent_1 = Agent(1)
    agent_2 = Agent(2)
    constraints_1 = constraints_0.fork(agent_1, 35, (5, 8))
    constraints_2 = constraints_1.fork(agent_1, 35, (3, 4))
    constraints_3 = constraints_2.fork(agent_2, 20, (6, 4))
    constraints_4 = constraints_3.fork_edge_conflict(agent_1, 30, (3, 4), (4, 4))

    print(constraints_4.constraints[agent_1], constraints_4.constraints_on_edge[agent_1])
