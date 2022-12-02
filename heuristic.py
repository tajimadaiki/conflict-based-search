from typing import List, Tuple
import numpy as np
from neighbour_table import NeighbourTable


class Heuristic:

    def __init__(self,
                 map_data:  List[List[str]]):
        self.neighbour_table = NeighbourTable(map_data)
        self.grid_size_x = len(map_data)
        self.grid_size_y = len(map_data[0])
        self._warshall_floyd()

    @staticmethod
    def manhattan(current: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(current - goal, 1))

    @staticmethod
    def euclidean(current: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(current - goal, 2))

    def single_shortest_path(self, current: np.ndarray, goal: np.ndarray) -> int:
        return self.shortest_distance[self.converter(current)][self.converter(goal)]
    
    # reshape [grid_size_x, grid_size_y] -> [grid_size_x * grid_size_y, 1]
    def converter(self, pos: np.ndarray) -> int:
        return pos[0] * self.grid_size_y + pos[1]

    # reshape [[grid_size_x * grid_size_y, 1] -> [grid_size_x, grid_size_y]
    def inverter(self, id_: int) -> np.ndarray:
        i = id_ // self.grid_size_y
        j = id_ % self.grid_size_y
        return np.array([i, j])

    def _warshall_floyd(self) -> np.ndarray:
        
        def is_obstacle(id_: int) -> bool:
            pos = self.inverter(id_)
            return self.neighbour_table.is_obstacle(pos)

        inf = 1001001001
        node_num = self.grid_size_x * self.grid_size_y
        distance = np.full((node_num, node_num), inf)
        # set 0
        for i in range(node_num):
            if is_obstacle(i): continue
            distance[i][i] = 0
        # set neighbour
        for i in range(self.grid_size_x):
            for j in range(self.grid_size_y):
                pos = np.array([i, j])
                node_id = self.converter(pos)
                for n_pos in self.neighbour_table.neighbours(pos):
                    n_node_id = self.converter(n_pos)
                    distance[node_id][n_node_id] = 1
        # calculate warshall_floyd
        for k in range(node_num):
            if is_obstacle(k): continue
            for i in range(node_num):
                if is_obstacle(i): continue
                for j in range(node_num):
                    if is_obstacle(j): continue
                    distance[i][j] = min([distance[i][j], distance[i][k] + distance[k][j]])

        self.shortest_distance  = distance


if __name__ == "__main__":
    from config_file_loader import ConfigFileLoader
    config_file = "./config/config.xlsx"
    config = ConfigFileLoader(config_file)
    h = Heuristic(config.map)
    print(h.neighbour_table.map[11][0], h.neighbour_table.map[12][4])
    print(h.single_shortest_path(np.array([11, 0]), np.array([12, 4])))
    print(h.single_shortest_path(np.array([24, 35]), np.array([24, 35])))
