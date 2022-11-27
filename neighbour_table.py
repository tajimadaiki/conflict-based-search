from typing import List, Tuple
import numpy as np


class NeighbourTable:

    directions_k2 = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    directions_k3 = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self,
                 grid_size_x: int,
                 grid_size_y: int,
                 static_obstacles: List[Tuple[int, int]],
                 k: int = 2):
        # set 2^k neighborhood movement
        directions = []
        if k == 2: directions = self.directions_k2
        if k == 3: directions = self.directions_k3
        # create neighbours table
        table = dict()
        for i in range(grid_size_x):
            for j in range(grid_size_y):
                neighbours = []
                for dx, dy in directions:
                    x = i + dx
                    y = j + dy
                    if 0 <= x < grid_size_x and \
                            0 <= y < grid_size_y and \
                            not ((x, y) in static_obstacles):
                        neighbours.append(np.array([x, y]))
                table[(i, j)] = np.array(neighbours)
        self.table = table

    def neighbours(self, pos: np.ndarray) -> np.ndarray:
        return self.table[tuple(pos)]


if __name__ == "__main__":
    obstacles = [(3, 4), (5, 5), (9, 2)]
    neighbour = NeighbourTable(10, 15, obstacles)
    pos44 = np.array([4, 4])
    print(neighbour.neighbours(pos44))
