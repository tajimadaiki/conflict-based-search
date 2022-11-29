from typing import List, Tuple, Dict, Set
import numpy as np
import heapq as hq
from neighbour_table import NeighbourTable
from state import State
from heuristic import Heuristic


class AStar:

    def __init__(self,
                 excel_map_file: str):
        self.neighbour_table = NeighbourTable(excel_map_file)
        self.grid_size_x = self.neighbour_table.grid_size_x
        self.grid_size_y = self.neighbour_table.grid_size_y
        
        self.heuristic = Heuristic(excel_map_file)

    def plan(self,
             start: Tuple[int, int],
             goal: Tuple[int, int],
             constraints_on_node: Dict[int, Set[Tuple[int, int]]] = None,
             constraints_on_edge: Dict[int, Dict[Tuple[int, int], Set[Tuple[int, int]]]] = None,
             other_agents_on_node: Dict[int, Set[Tuple[int, int]]] = None,
             other_agents_on_edge: Dict[int, Dict[Tuple[int, int], Set[Tuple[int, int]]]] = None,
             debug: bool = False) -> np.ndarray:

        def is_conflict_on_node(obstacle: Dict[int, Set[Tuple[int, int]]],
                                pos: np.ndarray,
                                time: int) -> bool:
            pos = tuple(pos)
            return pos in obstacle.setdefault(time, set())

        def is_conflict_on_edge(obstacle: Dict[int, Dict[Tuple[int, int], Set[Tuple[int, int]]]],
                                pos_f: np.ndarray,
                                pos_t: np.ndarray,
                                time: int) -> bool:
            pos_f = tuple(pos_f)
            pos_t = tuple(pos_t)
            return pos_t in obstacle.setdefault(time, dict()).setdefault(pos_f, set())

        def reconstruct_path(goal: State) -> np.ndarray:
            path = []
            current = goal
            while current.pre_state is not None:
                path.append(current.pos)
                current = current.pre_state
            path.append(current.pos)  # add start node
            path.reverse()
            return np.array(path)

        # set start and goal pos
        start = np.array(start)
        goal = np.array(goal)

        # initialize the start state
        s = State(start, 0, 0, self.heuristic.single_shortest_path(start, goal), 0)

        # create open set and heapify
        open_set = [s]
        open_closed_dict = {s: True}
        hq.heapify(open_set)

        # create closed set
        closed_set = set()

        # start a* loop
        while open_set:
            # get smallest f_value state
            current_state = open_set[0]
            pos_f = current_state.pos

            # get goal
            if current_state.is_same_position(goal):
                if debug:
                    print("Path found!")
                    print(f'conflict num: {current_state.conflict_num}')
                return reconstruct_path(current_state)

            # add closed set
            open_closed_dict[open_set[0]] = False
            closed_set.add(hq.heappop(open_set))

            # increment time step
            next_time = current_state.time + 1

            for pos_t in self.neighbour_table.neighbours(current_state.pos):
                # check conflict with other agents on node
                conflict_num = current_state.conflict_num
                if other_agents_on_node is not None and \
                        is_conflict_on_node(other_agents_on_node, pos_t, next_time):
                    conflict_num += 1

                # check conflict with other agents on edge
                if other_agents_on_edge is not None and \
                        is_conflict_on_edge(constraints_on_edge, pos_f, pos_t, next_time):
                    conflict_num += 1

                # avoid conflict on node
                if constraints_on_node is not None and \
                        is_conflict_on_node(constraints_on_node, pos_t, next_time):
                    continue

                # avoid conflict on edge
                if constraints_on_edge is not None and \
                        is_conflict_on_edge(constraints_on_edge, pos_f, pos_t, next_time):
                    continue

                # create neighbour state
                neighbour_state = State(pos_t,
                                        next_time,
                                        current_state.g_value + 1,
                                        self.heuristic.single_shortest_path(pos_t, goal),
                                        conflict_num)

                # check if visited
                if neighbour_state in closed_set:
                    continue

                # add to open set
                if open_closed_dict.setdefault(neighbour_state) is not True:
                    neighbour_state.pre_state = current_state
                    open_closed_dict[neighbour_state] = True
                    hq.heappush(open_set, neighbour_state)

        if debug:
            print("No path found!")
        return np.array([])


if __name__ == "__main__":
    planner = AStar("./map/map.xlsx")
    print(planner.plan((11, 0), (12, 4), constraints_on_node={3: {(3, 2), (2, 7)}, 4: {(3, 7)}}))
