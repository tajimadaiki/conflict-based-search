def load_file(map_file_path):
    col = 0
    row = 0
    static_obstacles = []
    end_points = []
    file = open(map_file_path, "r")
    if not file.mode == 'r':
        print("Could not open " + map_file_path)
    else:
        print("Loading map file")
        world_data = file.readlines()
        for line in world_data:
            col = 0
            for char in line:
                if char == '.':
                    pass
                if char == 'e':
                    end_points.append((col, row))
                if char == '@':
                    static_obstacles.append((col, row))
                if char is not "\n":
                    col += 1
            row += 1
    file.close()
    return col, row, static_obstacles, end_points


if __name__ == "__main__":
    grid_size_x, grid_size_y, static_obstacles, end_points = load_file('./map/kvc.map')
    print(grid_size_x, grid_size_y)
    print(static_obstacles)
