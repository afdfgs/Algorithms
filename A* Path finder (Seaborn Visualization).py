import random as rand
import seaborn as sns
import matplotlib.pyplot as plt

plt.ion()

def get_neighbors(point, grid):
    x, y = point
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))
    return neighbors

def heuristic(current, end):
    return abs(current[0]-end[0]) + abs(current[1]-end[1])

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

def visualization(grid, path=None, closed=None, start=None, end=None):
    visual = []
    path_set = set(path) if path else set()
    closed_set = set(closed) if closed else set()

    for i in range(len(grid)):
        row = []
        for j in range(len(grid[0])):
            if (i,j) == start:
                row.append(5)
            elif (i,j) == end:
                row.append(6)
            elif (i,j) in path_set:
                row.append(4)
            elif (i,j) in closed_set:
                row.append(3)
            elif grid[i][j] == 1:
                row.append(2)
            else:
                row.append(1)
        visual.append(row)
    return visual

def plot_seaborn(grid, path=None, closed=None, start=None, end=None):
    visual = visualization(grid, path, closed, start, end)

    cmap = sns.color_palette([
        "lightgrey",
        "black",
        "yellow",
        "blue",
        "green",
        "red"
    ])

    plt.clf()
    sns.heatmap(visual, cmap=cmap, cbar=False, square=True, linewidths=0.5)
    plt.title("A* Pathfinding (Live)")
    plt.pause(0.05)

def astar(grid, start, end):
    open_list = [start]
    came_from = {}
    g = {start: 0}
    closed = []

    while open_list:
        current = get_lowest_f(open_list, g, end)

        # 动态显示
        plot_seaborn(grid, closed=closed, start=start, end=end)

        if current == end:
            path = reconstruct_path(came_from, start, end)
            return path

        open_list.remove(current)
        closed.append(current)

        for neighbor in get_neighbors(current, grid):
            new_g = g[current] + 1
            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                came_from[neighbor] = current
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None

def create_grid():
    rows = rand.randint(10, 20)
    cols = rand.randint(10, 20)
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if rand.randint(0,100) < 25:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)

    start = (0,0)
    end = (rows-1, cols-1)
    grid[0][0] = 0
    grid[rows-1][cols-1] = 0
    return grid, start, end

grid, start, end = create_grid()
print("Start:", start)
print("End:", end)

plot_seaborn(grid, start=start, end=end)
path = astar(grid, start, end)

if path:
    print("Path found:")
    print(path)
    plot_seaborn(grid, path=path, start=start, end=end)
else:
    print("No Path Found")
    plot_seaborn(grid, start=start, end=end)

plt.ioff()
plt.show()
