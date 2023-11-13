# QS-test-task
This is a test task.

## Done
Currently the requirements from 1 to 5 are met.

Grid Representation:
- created class `CityGrid`;
- initialized class with N x M matrix using enum `TileType` as predefined values;
- implemented random obstacle coverage according to percents given.

Tower Coverage:
- visualized tower coverage with changing surrounding squares within its area to the type `TileType.Conected`;
- added method `print_pseudo` to show the grid as matrix of numbers.

Optimization Problem:
- implemented tower position evaluation based on the maximum connection area and if the tower is inside of other tower connection area (if there are no disconnected areas in the grid or the next tower can not be placed in any connection area).

Path Reliability:
- added method to get all connections between towers within tower radius;
- described all connections as graph;
- implemented dijkstra with potentials euristic to find the shortest paths between two nodes of connections graph.

Visualization:
- visualized the grid with a 2D heatmap with `seaborn` library;
- visualized reliable paths between all nodes with `matplotlib.animation`.

Animation example.

![Animation example](https://github.com/Tulenien/QS-test-task/blob/develop/pics/workExample.gif)

Examples with various parameters:

* M x N = 10 x 10
* R = 1
* Obstruction % = 30

![](https://github.com/Tulenien/QS-test-task/blob/develop/pics/10_10_30_1.png)

* M x N = 20 x 20
* R = 2
* Obstruction % = 40

![](https://github.com/Tulenien/QS-test-task/blob/develop/pics/20_20_40_2.png)

* M x N = 30 x 40
* R = 4
* Obstruction % = 60

![](https://github.com/Tulenien/QS-test-task/blob/develop/pics/30_40_60_4.png)

## Todo
Improve upon tower placement with new restrictions:
- budget;
- towers cost.

## Task
Imagine that a telecommunications company is working on designing an efficient 7G-network layout for a new city. The city can be represented as a grid, where some blocks are obstructed and cannot have towers, while others can. The goal is to provide the maximum coverage with the minimum number of towers.

1. Grid Representation
Create a class CityGrid that can represent the city as an N x M grid. During the initialization of the class, obstructed blocks are randomly placed with coverage >30% (we can change this parameter).

2. Tower Coverage
Each tower has a fixed range R (in blocks) within which it provides coverage. This coverage is a square, with the tower in the center.
Implement a method in the CityGrid class to place a tower and visualize its coverage.

3. Optimization Problem
Design an algorithm to place the minimum number of towers such that all of non-obstructed blocks are within the coverage of at least one tower. The algorithm cannot place towers on obstructed blocks.
Implement a method in the CityGrid class to display the placement of towers.

4. Path Reliability
Imagine that data is transmitted between towers. For simplicity, assume that each tower can directly communicate with any other tower within its range.
Design an algorithm to find the most reliable path between two towers. The reliability of a path decreases with the number of hops (tower-to-tower links). So, a path with fewer hops is more reliable.

5. Visualization
Implement functions to visualize the CityGrid, including obstructed blocks, towers, coverage areas, and data paths.
Use any Python plotting library of your choice, such as matplotlib or seaborn.

Bonus tasks (optional):
Extend the optimization problem: Now towers have a cost, and you have a limited budget. Modify your algorithm to maximize coverage while staying within the budget. Consider different types of towers with different ranges and costs. How would this change your optimization approach?
