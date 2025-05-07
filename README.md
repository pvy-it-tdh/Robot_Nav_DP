# Robot_Nav_DP
This repository contains a Python implementation of a robot navigation algorithm using Dynamic Programming (DP), Dijkstra, Hybrid Dynamic Programming Dijkstra to find the shortest path in a grid environment. The robot can move in four directions: up, down, left, and right. The algorithm takes into account obstacles in the grid and computes the optimal path from a start position to a goal position.
## Table of Contents
- [Robot_Nav_DP](#robot_nav_dp)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Algorithm Explanation](#algorithm-explanation)
  - [Example](#example)
  - [License](#license)
  - [Contributing](#contributing)
  - [Contact](#contact)
  - [References](#references)
  - [Future Work](#future-work)
  - [Limitations](#limitations)
    - [Acknowledgements](#acknowledgements)
    - [Disclaimer](#disclaimer)
    - [Author](#author)
    - [Version](#version)

```
## Usage
To use the robot navigation algorithm, you can run the `robot_nav.py` script. The script takes the following command-line arguments:
```bash
python Dijkstra.py --start_x <start_x> --start_y <start_y> --goal_x <goal_x> --goal_y <goal_y> --obstacles <obstacles>
```
- `start_x`: The x-coordinate of the starting position.
- `start_y`: The y-coordinate of the starting position.
- `goal_x`: The x-coordinate of the goal position.
- `goal_y`: The y-coordinate of the goal position.
- `obstacles`: A list of tuples representing the coordinates of obstacles in the grid. For example, `[(1, 2), (3, 4)]` represents obstacles at (1, 2) and (3, 4).
- `--algorithm`: The algorithm to use for pathfinding. Options are `dijkstra`, `dynamic_programming`, or `hybrid_dijkstra`. Default is `dijkstra`.
- `--grid_size`: The size of the grid. Default is `10`.
- `--show_path`: Whether to visualize the path. Default is `False`.
- `--show_grid`: Whether to visualize the grid. Default is `False`.
- `--show_obstacles`: Whether to visualize the obstacles. Default is `False`.
- `--show_start_goal`: Whether to visualize the start and goal positions. Default is `False`.
- `--show_grid_with_path`: Whether to visualize the grid with the path. Default is `False`.
- `--show_grid_with_obstacles`: Whether to visualize the grid with obstacles. Default is `False`.
- `--show_grid_with_start_goal`: Whether to visualize the grid with start and goal positions. Default is `False`.
- `--show_grid_with_start_goal_path`: Whether to visualize the grid with start, goal, and path. Default is `False`.
- `--show_grid_with_start_goal_obstacles`: Whether to visualize the grid with start, goal, and obstacles. Default is `False`.
- `--show_grid_with_start_goal_obstacles_path`: Whether to visualize the grid with start, goal, obstacles, and path. Default is `False`.
- `--show_grid_with_start_goal_obstacles_path_grid`: Whether to visualize the grid with start, goal, obstacles, and path in a grid format. Default is `False`.
