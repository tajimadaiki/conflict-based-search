import openpyxl
from typing import List
from agent import Agent

class Config:
    def __init__(self):
        self.agents: List[Agent] = []
        self.agents_ags = dict()
        self.map: List[List[str]] = []
        self.static_obstacles = []
        self.endpoints = dict()
        self.chargers = dict()
        self.grid_size_x = int()
        self.grid_size_y = int()
        
    def load_from_xlsx(self, config_file: str):
        self._wb = openpyxl.load_workbook(config_file)
        self._load_agent()
        self._load_map() 
    
    # load work sheet 'agents'
    def _load_agent(self):
        agents_ws = self._wb['agents']
        keys = dict()
        for row in range(1, agents_ws.max_row + 1):
            for col in range(1, agents_ws.max_column + 1):
                if row == 1:
                    key = str(agents_ws.cell(row, col).value)
                    self.agents_ags[key] = []
                    keys[col] = key
                else:
                    value = str(agents_ws.cell(row, col).value)
                    self.agents_ags[keys[col]].append(value)
                    if keys[col] == 'id': 
                        agent = Agent(value)
                        self.agents.append(agent)

    # load work sheet 'map' and 'name'
    def _load_map(self):
        map_ws = self._wb['map']
        name_ws = self._wb['name']
        self.grid_size_x = map_ws.max_row
        self.grid_size_y = map_ws.max_column
        for row in range(1, map_ws.max_row + 1):
            map_row = []
            for col in range(1, map_ws.max_column + 1):
                x = row - 1
                y = col - 1
                # record map
                map_row.append(map_ws.cell(row, col).value)
                name = name_ws.cell(row, col).value
                # record static obstacles
                if map_ws.cell(row, col).value == '@':
                    self.static_obstacles.append([x, y])
                # record endpoints
                if map_ws.cell(row, col).value[0] == 'e':
                    self.endpoints[name] = [x, y]
                # record chargers
                if map_ws.cell(row, col).value[0] == 'c':
                    self.chargers[name] = [x, y]
            self.map.append(map_row)


if __name__ == "__main__":
    config = Config()
    config_file = "./config/config.xlsx"
    config.load_from_xlsx(config_file)
    print(config.agents)
    print(config.agents_ags)

