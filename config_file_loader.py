import openpyxl
from typing import List

class ConfigFileLoader:
    def __init__(self,
                 config_file: str):
        self._config_file = config_file
        self._load_map() 

    def _load_map(self):
        wb = openpyxl.load_workbook(self._config_file)
        map_sh = wb['map']
        self.map: List[List[str]] = []
        for row in range(1, map_sh.max_row + 1):
            map_row = []
            for col in range(1, map_sh.max_column + 1):
                map_row.append(map_sh.cell(row, col).value)
            self.map.append(map_row)


if __name__ == "__main__":
    map_file = "./map/map.xlsx"
    config = ConfigFileLoader(map_file)
