from typing import List, Tuple
import numpy as np
from neighbour_table import NeighbourTable


class Heuristic:

    def __init__(self,
                 map_file: str):
        self.neighbour_table = NeighbourTable(map_file)
        self.grid_size_x = self.neighbour_table.grid_size_x
        self.grid_size_y = self.neighbour_table.grid_size_y
        self.shortest_distance = self._warshall_floyd()

    @staticmethod
    def manhattan(current: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(current - goal, 1))

    @staticmethod
    def euclidean(current: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(current - goal, 2))

    def single_shortest_path(self, current: np.ndarray, goal: np.ndarray) -> int:
        return self.shortest_distance[current[0]][current[1]][goal[0]][goal[1]]

    def _warshall_floyd(self) -> np.ndarray:

        # reshape [grid_size_x, grid_size_y] -> [grid_size_x * grid_size_y, 1]
        def converter(pos: np.ndarray) -> int:
            return pos[0] * self.grid_size_y + pos[1]

        # reshape [[grid_size_x * grid_size_y, 1] -> [grid_size_x, grid_size_y]
        def inverter(id_: int) -> np.ndarray:
            i = id_ // self.grid_size_y
            j = id_ % self.grid_size_y
            return np.array([i, j])
        
        def is_obstacle(id_: int) -> bool:
            pos = inverter(id_)
            return self.neighbour_table.is_obstacle(pos)

        inf = 1001001001
        node_num = self.grid_size_x * self.grid_size_y
        distance = np.full((node_num, node_num), inf)
        # set 0
        for i in range(node_num):
            distance[i][i] = 0
        # set neighbour
        for i in range(self.grid_size_x):
            for j in range(self.grid_size_y):
                pos = np.array([i, j])
                node_id = converter(pos)
                for n_pos in self.neighbour_table.neighbours(pos):
                    n_node_id = converter(n_pos)
                    distance[node_id][n_node_id] = 1
        # calculate warshall_floyd
        for k in range(node_num):
            if is_obstacle(k): continue
            for i in range(node_num):
                if is_obstacle(i): continue
                for j in range(node_num):
                    if is_obstacle(j): continue
                    distance[i][j] = min([distance[i][j], distance[i][k] + distance[k][j]])

        shortest_distance = np.full((self.grid_size_x, self.grid_size_y, self.grid_size_x, self.grid_size_y), inf)
        print(distance)

        for i in range(node_num):
            for j in range(node_num):
                i_pos = inverter(i)
                j_pos = inverter(j)
                shortest_distance[i_pos[0]][i_pos[1]][j_pos[0]][j_pos[1]] = distance[i][j]

        return shortest_distance


if __name__ == "__main__":
    h = Heuristic("./map/map.xlsx")
    print(h.neighbour_table.map[11][0], h.neighbour_table.map[12][4])
    print(h.single_shortest_path(np.array([11, 0]), np.array([12, 4])))

