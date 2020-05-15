from algorithm import *
import time

"""
IMPORTANT VARIABLES: change maximum steepness and distance cost depending on data resolution
"""

def main():

    #Load Data into np array
    print("Loading Data...")
    data = open_data('Elliot_data')
    print("Done Loading Data")

    #Find highest point in map and set as goal
    result = np.where(data == np.amax(data))
    goal = list(zip(result[0], result[1]))[0]  # (y, x) (rows, columns)
    start = (0, 0)
    print("Start: ", start)
    print("Goal: ", goal)
    print("Total Elevation Difference: ", abs(data[start[0]][start[1]] - data[goal[0]][goal[1]]))

    #Time and run algorithm
    total_time = 0
    for i in range(1):
        start_time = time.time()

        path = A_star(data, start, goal, 'm')

        end_time = time.time()
        total_time += (end_time - start_time)

    print(f"Total Time: {total_time}")
    print(f"Average: {total_time/10}")

    #Display Path found
    if path:
        draw_path(data, start, path)

if __name__ == "__main__":
    main()