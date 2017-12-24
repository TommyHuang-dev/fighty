# choose a target tile to attempt to reach,
# curposX, curposY, tarX, and tarY are the players coordinates on the 11x8 grid
def choose_tile(grid, curposX, curposY, tarX, tarY, ammo):
    dishor = curposX - tarX
    disver = curposY - tarY
    total_dist = abs(dishor) + abs(disver)
    cur_check = [curposX, curposY]
    path = []

    # get aggressive with ammo or melee weapon, which has ammo of -1:
    if ammo > 0:
        for i in range(int(total_dist)):
            # go right or left
            if abs(dishor) >= abs(disver):
                # right
                if dishor > 0:
                    dishor += -1
                    cur_check[0] += -1
                    path.append(cur_check[:])
                # left
                else:
                    dishor += 1
                    cur_check[0] += 1
                    path.append(cur_check[:])

            # go up or down
            else:
                # up
                if disver > 0:
                    disver += -1
                    cur_check[1] += -1
                    path.append(cur_check[:])
                # down
                else:
                    dishor += 1
                    cur_check[1] += 1
                    path.append(cur_check[:])

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
