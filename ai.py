# choose a target tile to attempt to reach,
# curposX, curposY, tarX, and tarY are the players coordinates on the 11x8 grid


# check to see if there is a valid path to the player


# EMERGENCY PATHING
# returns an array
def wall_path(cur_tile, walls, direction):
    pass


# find a path
def choose_tile(walls, curposX, curposY, tarX, tarY, ammo):
    dishor = curposX - tarX
    disver = curposY - tarY
    total_dist = abs(dishor) + abs(disver)
    cur_check = [curposX, curposY]
    path = []
    path_found = False

    # get aggressive with ammo or melee weapon, which has ammo of -1:
    # this works but doesnt go around walls
    if ammo > 0:
        while not path_found:
            pass
            # do stuff

    # otherwise get to safety while reloading
    elif ammo == 0:
        pass


    #print("dist:", total_dist)
    return path



# uses some algorithm and the tile it wants to move to in order to return which direction to move in the 8
# main compass directions
def find_next_tile(grid, tile_choice):
    pass


'''
EXAMPLE GRID:
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
