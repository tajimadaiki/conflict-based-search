import numpy as np
import heapq as hq


class State:

    def __init__(self,
                 pos: np.ndarray,
                 time: int,
                 g_value: int,
                 h_value: int,
                 conflict_num: int):
        self.pos = pos  # [i, j]
        self.time = time
        self.g_value = g_value
        self.f_value = g_value + h_value
        self.conflict_num = conflict_num  # CAT：conflict avoidance table
        self.pre_state = None

    def is_same_position(self, pos: np.ndarray) -> bool:
        return all(self.pos == pos)

    def __hash__(self) -> int:
        concat = str(self.pos[0]) + str(self.pos[1]) + '0' + str(self.time)
        return int(concat)

    def __lt__(self, other: 'State') -> bool:
        if self.f_value != other.f_value:
            return self.f_value < other.f_value
        else:
            return self.conflict_num < other.conflict_num  # tie-breaking implementation

    def __eq__(self, other: 'State') -> bool:
        return all(self.pos == other.pos) and self.time == other.time

    def __str__(self):
        return 'State(pos=[' + str(self.pos[0]) + ', ' + str(self.pos[1]) + '], ' \
               + 'time=' + str(self.time) + ', f_value=' + str(self.f_value) + ')'


if __name__ == "__main__":
    state1 = State(np.array([3, 5]), 25, 40, 30, 2)
    state2 = State(np.array([5, 5]), 25, 45, 25, 1)
    state3 = State(np.array([1, 7]), 25, 55, 25, 3)
    state4 = State(np.array([1, 7]), 25, 55, 25, 3)

    print(state1 == state2)
    print(state1 < state2)

    state = [state1, state2, state3]
    hq.heapify(state)
    for k in range(3):
        print(hq.heappop(state))

    state_set = {state1, state2, state3, state4}  # state3 and state4 are same
    print(state_set)
