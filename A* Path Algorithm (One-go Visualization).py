import random as rand

def get_neighbors(point, grid):
    x,y = point
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbor = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == 0:
                neighbor.append((nx, ny))

    return neighbor

def heuristic(current, end):
    return abs(current[0] - end[0]) + abs(current[1] - end[1])

def reconstruct_path(came_from, start, end):
    current = end
    path = []

    while current in came_from:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path

def get_lowest_f(open_list, g, end):
    best_point = open_list[0]
    best_f = g[best_point] + heuristic(best_point, end)

    for point in open_list:
        f = g[point] + heuristic(point, end)
        if f < best_f:
            best_point = point
            best_f = f

    return best_point

def astar(grid, start, end):
    open_list = [start]
    came_from = {}
    g = {start: 0}

    while open_list:

        current = get_lowest_f(open_list, g, end)

        if current == end:
            path = reconstruct_path(came_from, start, end)
            return path

        open_list.remove(current)

        for neighbor in get_neighbors(current, grid):
            new_g = g[current] + 1

            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                came_from[neighbor] = current

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None

def create_grid():
    length = rand.randint(5, 30)
    width = rand.randint(5,30)
    grid = []

    for i in range(length):
        row = []
        for j in range(width):
            component = rand.randint(0,100)
            if component < 10:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)

    end_x = rand.randint(0,width-1)
    end_y = rand.randint(0,length-1)

    start_coord = (0,0)
    end_coord = (end_x, end_y)

    grid[0][0] = 0
    grid[end_x][end_y] = 0

    return grid, start_coord, end_coord

def visualization(grid, path = None, start = None, end = None):
    for i in range(len(grid)):
        row_str = ""
        for j in range(len(grid[0])):
            if path and (i,j) in path:
                row_str += "P "
            elif start == (i,j):
                row_str += "S "
            elif end == (i,j):
                row_str += "E "
            elif grid[i][j] == 1:
                row_str += "# "
            else:
                row_str += "* "
        print(row_str)
    print("\n")

grid, start, end = create_grid()
print("Grid: ")
visualization(grid, start = start, end = end)

path = astar(grid, start, end)

if path:
    print("Path found:")
    print(path)
    visualization(grid, path = path, start = start, end = end)
else:
    print("No Path Found")