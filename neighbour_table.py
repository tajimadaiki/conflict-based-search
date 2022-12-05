from typing import List, Tuple, Dict
import numpy as np
from typing import Dict

class NeighbourTable:

    def __init__(self,
                 map_data: List[List[str]]):
        # load map file
        self.map = map_data
        grid_size_x = len(map_data)
        grid_size_y = len(map_data[0])
        # create neighbours table
        self.neighbours_table: Dict[Tuple[int,int]: str] = dict()
        for x in range(grid_size_x):
            for y in range(grid_size_y):
                directions = []
                neighbours = []
                value = self.map[x][y]
                if len(value) == 1:
                    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
                else:
                    directions.append((0, 0))
                    for c in value[1:]:
                        if c == 'r': directions.append((0, -1))
                        if c == 'u': directions.append((-1, 0))
                        if c == 'l': directions.append((0, 1))
                        if c == 'd': directions.append((1, 0))
                
                for dx, dy in directions:
                    nx = x+ dx
                    ny = y + dy
                    if 0 <= nx < grid_size_x and 0 <= ny < grid_size_y:
                        if not (self.map[nx][ny] == '@'):
                            neighbours.append(np.array([nx, ny]))
                self.neighbours_table[(x, y)] = np.array(neighbours)             

    def neighbours(self, pos: np.ndarray) -> np.ndarray:
        return self.neighbours_table[tuple(pos)]
    
    def is_obstacle(self, pos: np.ndarray) -> bool:
        x = pos[0]
        y = pos[1]
        return self.map[x][y] == '@'


if __name__ == "__main__":
    # import config file loader
    from config_file_loader import Config
    config_file = "./config/config.xlsx"
    config = Config(config_file)
    neighbour_table = NeighbourTable(config.map)
    print(neighbour_table.map[12][4])
    pos1 = np.array([24, 35])
    pos2 = np.array([4, 3])
    print(neighbour_table.neighbours(pos1))
    print(neighbour_table.is_obstacle(pos2))
