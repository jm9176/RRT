'''
Finding the path from start to goal position
using Rapidly exploring Random Tree (RRT)
'''

import numpy as np
import math
from Node import Node
from retrace_path import retrace_path
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# Calculating heuristic using distance formula
def distance(point_a, point_b):
    return pow(pow(point_a.x - point_b.x, 2) + pow(point_a.y - point_b.y, 2), 0.5)

# Calculating the nearest neighbor with low cost and forming a link
def findNeigh(dict_cost, new_pt, rad):
    # temp_list storing all the neighbors to the new_pt
    # within a distance of 0.4 units as defined by rad
    temp_list = []

    for var in dict_cost:
        if distance(var, new_pt) < rad:
            temp_list.append(var)

    temp_val = dict_cost[new_pt]

    for var in temp_list:
        if dict_cost[var] < temp_val:
            temp_val = dict_cost[var]
            temp_var = var

    return temp_var


# Calculating the shortest path
def finding_path(start, goal, n_r, n_c, vertices, polygon):
    # dict_parent to store the previous (parent) node
    pt_list = [start]
    dict_parent = {}
    delta_d = 0.1
    dict_cost = {}
    rad = 0.3
    dict_cost[start] = 0
    path = []

    # generating the number of random vertices
    for i in range(vertices):

        # Generating a random point
        rand_pt = Node(round(np.random.uniform(0, n_r), 3), round(np.random.uniform(0, n_c), 3))

        # Finding the node in the open_list with minimum distance to the
        # random point
        temp_var = pt_list[0]
        temp_val = distance(temp_var, rand_pt)

        for var in pt_list:
            if distance(var, rand_pt) < temp_val:
                temp_val = distance(var, rand_pt)
                temp_var = var

        # Calculating the angle between the selected node with minimum
        # distance and the randomly generated point and expanding the selected node
        theta = math.atan2(rand_pt.y - temp_var.y, rand_pt.x - temp_var.x)
        delta_dx = round(temp_var.x + delta_d * math.cos(theta), 3)
        delta_dy = round(temp_var.y + delta_d * math.sin(theta), 3)

        new_pt = Node(delta_dx, delta_dy)

        # To check if the expanded point lies in the obstacle or not
        # if not, then add the point to the point list
        if polygon.contains(Point(new_pt.x, new_pt.y)) == False:
            pt_list.append(new_pt)

            # Storing the parent node of the new node
            dict_cost[new_pt] = dict_cost[temp_var] + distance(temp_var, new_pt)  #

            best_pt = findNeigh(dict_cost, new_pt, rad)
            plt.plot([best_pt.x, new_pt.x], [best_pt.y, new_pt.y], color='orange')
            dict_parent[new_pt] = best_pt

    # Defining a region to check if the current point is near to the
    # goal or not. If yes, then connect the current node to the goal
    max_val = max(dict_cost.values())

    for var in pt_list:
        if var == goal:
            path = retrace_path(dict_parent, goal, start)

        elif distance(var, goal) < 0.5 and dict_cost[var] <= max_val:
            pt_list.append(goal)
            plt.plot([goal.x, var.x], [goal.y, var.y], color='orange')
            dict_parent[goal] = var
            max_val = dict_cost[var]
            path = retrace_path(dict_parent, goal, start)

    # Return the path if goal is reached, else return None and
    # the navigated pt_list
    if not path:
        print("Path not found: Increase the vertices")
        return pt_list, None
    else:
        print("Path found")
        return pt_list, path


# Initialize the input grid, start and end goal
# n_r, n_c represents the no. of rows and cols in a grid
n_r, n_c = 6, 6
start = Node(1, 1)
goal = Node(5, 5)
vertices = 500

plt.figure()
plt.axis([0, n_r, 0, n_c])

# Defining the polygon obstacle
points = [[2, 2], [2, 4], [4, 4], [4, 2]]
polygon = Polygon(points)
plt.gca().add_patch(plt.Polygon(points, fill=True, color='lightgrey'))

# Finding the final path and the navigated points
final_list, path = finding_path(start, goal, n_r, n_c, vertices, polygon)

# Plotting the overall search nodes
for var in final_list:
    plt.plot(var.x, var.y, color='orange', marker='o', markersize=3)

# Plotting the final path and the nodes from start to goal
if path is not None:
    for i in range(1, len(path)):
        plt.plot(path[i].x, path[i].y, color='red', marker='o', markersize=1)
        plt.plot([path[i].x, path[i - 1].x], [path[i].y, path[i - 1].y], color='red')

plt.plot(start.x, start.y, color='blue', marker='o')
plt.plot(goal.x, goal.y, color='green', marker='o')

plt.show()
