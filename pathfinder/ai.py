# choose a target tile to attempt to reach,
# curposX, curposY, tarX, and tarY are the players coordinates on the 11x8 grid


# check to see if there is a valid path to the player

# search algorithm from a shady site
# https://github.com/brean/python-pathfinding

from pathfinder.pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinder.pathfinding.core.grid import Grid
from pathfinder.pathfinding.finder.a_star import AStarFinder

def find_path(wall_grid, enemy_loc, player_loc):
    matrix = wall_grid
    grid = Grid(matrix=matrix)

    end = grid.node(enemy_loc[0], enemy_loc[1])
    start = grid.node(player_loc[0], player_loc[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    print(grid.grid_str(path=path, start=start, end=end))
    return path
