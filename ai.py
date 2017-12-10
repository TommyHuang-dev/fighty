

# choose a target tile to attempt to reach, tarX and tarY are the players coordinates on the 11x8 grid
def choose_tile(grid, curposX, curposY, tarX, tarY, ammo):
    curposX = (curposX - 100) // 75
    curposY = (curposY) // 75
    # get aggressive with ammo:
    if ammo > 0:
        pass

    # otherwise get to safety while reloading
    elif ammo <= 0:
        pass


# uses some algorithm and the tile it wants to move to in order to return which direction to move in the 8
# main compass directions
def find_next_tile(grid, tile_choice):
    pass


'''
EXAMPLE GRID:
[----, ----, ----, ----, ----, ----, ----, ----], 
[----, ----, ----, ----, True, ----, ----, ----], 
[----, ----, ----, ----, ----, ----, True, ----], 
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

