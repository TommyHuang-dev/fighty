# choose a target tile to attempt to reach,
# curposX, curposY, tarX, and tarY are the players coordinates on the 11x8 grid


# check to see if there is a valid path to the player

# search algorithm from a shady site
# https://github.com/brean/python-pathfinding

from pathfinder.pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinder.pathfinding.core.grid import Grid
from pathfinder.pathfinding.finder.a_star import AStarFinder

matrix = [
  [0, 0, 0],
  [0, 1, 0],
  [0, 0, 0]
]
grid = Grid(matrix=matrix)

start = grid.node(0, 0)
end = grid.node(2, 2)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print(grid.grid_str(path=path, start=start, end=end))


'''
EXAMPLE GRID (x and y are flipped, look at it with ur head tilted 90 degrees CCW:
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, True, ----, ----, ----, True, ----], 
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, ----, ----, True, ----, ----, ----], 
[----, ----, ----, ----, True, ----, ----, ----], 
[----, ----, ----, True, ----, ----, ----, ----], 
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, ----, True, ----, ----, ----, ----]]

first and last are always empty

'''
