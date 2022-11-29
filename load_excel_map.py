import openpyxl

def load_excel_map(map_file):
    wb = openpyxl.load_workbook(map_file)
    map_sh = wb['map']
    for row in range(1, map_sh.max_row + 1):
        for col in range(1, map_sh.max_column + 1):
            print(map_sh.cell(row, col).value, end=' ')
        print('')

if __name__ == "__main__":
    map_file = "./map/map.xlsx"
    load_excel_map(map_file)
