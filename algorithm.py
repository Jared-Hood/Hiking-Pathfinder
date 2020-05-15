import numpy as np
import matplotlib.pylab as plt
import util
import math

"""
Display only the map images
"""
def display_image(data):
    plt.imshow(data)
    plt.show()

"""
Display AI path overlain on the map images
"""
def draw_path(data, start, path):
    coord_list = path_coordinates(start, path)
    plt.imshow(data)
    x = [item[0] for item in coord_list]
    y = [item[1] for item in coord_list]
    plt.plot(y,x, 'r-')
    plt.show()

"""
Convert the actions taken to a list of coordinate pairs
"""
def path_coordinates(start, path):
    path_coordinates = [start]
    new_start = list(start)
    for p in path:
        coord = (new_start[0] + p[0], new_start[1] + p[1])
        path_coordinates.append(coord)
        new_start = list(coord)
    print(path_coordinates)
    return path_coordinates

"""
Open csv file containing the mountain elevation data
"""
def open_data(file):
    data = np.loadtxt(open(str(file), "rb"), delimiter=",")
    return data

"""
A* search function
g = total distance traveled to that node from start
 - Total distance traveled so far = previous distance + elevation change + 1 --> add 1 because each node is 1 meter
h = heuristic estimating distance to goal
"""
def A_star(data, position, goal, h='Euclidean'):
    queue = util.PriorityQueue()
    visited = set()
    queue.push((position, [], 0), 0)
    while (not queue.isEmpty()):
        state, moves, cost= queue.pop()
        if state not in visited:
            if state == goal:
                return moves

            visited.add(state)
            for neighbor in neighbors(data, state):
                c_cost = cost + neighbor[2] * .3048     #current_cost = previous_cost + elevation change (meters) + block size (for distance)
                queue.push( (neighbor[0], moves + [neighbor[1]], c_cost), c_cost + heuristic(h, neighbor[0], goal, data))

    print("No path to goal exists")

"""
Manhattan: inadmissible
Euclidean: admissible
Diagonal: inadmissible
"""
def heuristic(h, position, goal, data):
    if h == 'Manhattan' or h == 'm':
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1]) + abs(get_steepness(data, position, goal))
    if h == 'Diagonal' or h == 'd':
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        return (dx + dy) -1 * min(dx, dy) + get_steepness(data, position, goal)
    else:
        return math.sqrt((position[0] - goal[0])**2 + (position[1] - goal[1])**2 + get_steepness(data, position, goal)**2)

"""
Check if index into array is valid
"""
def in_bounds(matrix, row, col):
    if row < 0 or col < 0:
        return False
    if row > len(matrix)-1 or col > len(matrix[0])-1:
        return False
    return True

"""
Check if it is possible to go from p1 to p2 given the elevation difference
 - maximum_grade = max steepness before impossible to go to p2
"""
def check_steepness(elevation):
    maximum_grade = 30
    return elevation <= maximum_grade

"""
Cost function relating steepness
"""
def get_steepness(data, p1, p2):
    e1 = data[p1[0]][p1[1]]  # Starting elevation
    e2 = data[p2[0]][p2[1]]  # Neighbor elevation
    return abs(e1-e2)

"""
Get the neighboring nodes of the current position
"""
def neighbors(data, position):
    rowNumber = position[1]
    colNumber = position[0]
    neighbors = []
    for row in range(-1,2):
        for col in range(-1,2):
            if in_bounds(data, colNumber+col, rowNumber+row ):
                point = (colNumber+col, rowNumber+row )
                if point != position:
                    elevation_change = get_steepness(data, position, point)
                    if check_steepness(elevation_change):
                        n = (point, (col, row), elevation_change)  #position, action, real cost
                        neighbors.append(n)

    return neighbors