import pygame

# parses the file for weapons and shield stats in "open_file"
def parse_file(open_file):
    cur_line = open_file.readline()
    cur_wpn = 0
    cur_type = ""

    # initial parse for the save
    if cur_line == "save\n":
        # monies
        cur_line = open_file.readline().split()
        money = cur_line[1]

    else:
        print("something is wrong with the save file! 'save' is not at the top")
        print(cur_line)
        return

    for line in open_file:
        cur_line = line.split()
        if len(line.strip()) != 0:
            if cur_line[0] == "weapon":
                cur_type = "weapon"
                # name of weapon
                cur_line = open_file.readline().split()
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wName.append("")  # stop yelling at me pls
                wName[cur_wpn] = (cur_line[0:])

            elif cur_line[0] == "damage":
                wDmg.append("")
                wDmg[cur_wpn] = (int(cur_line[1]))
            elif cur_line[0] == "fire_rate":
                wRate.append("")
                wRate[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "proj_speed":
                wProj.append("")
                wProj[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "ammo":
                wAmmo.append("")
                wAmmo[cur_wpn] = (int(cur_line[1]))
            elif cur_line[0] == "reload":
                wRel.append("")
                wRel[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "inaccuracy":
                wAcc.append("")
                wAcc[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "recoil":
                wCoil.append("")
                wCoil[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "image":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wImg.append("")
                wImg[cur_wpn] = cur_line[6:]
            elif cur_line[0] == "bullet":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wBul.append("")
                wBul[cur_wpn] = cur_line[7:]
            elif cur_line[0] == "effect":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wEff.append("")
                wEff[cur_wpn] = cur_line[7:]
            elif cur_line[0] == "cost":
                wCost.append("")
                wCost[cur_wpn] = (int(cur_line[1]))
            elif cur_line[0] == "owned":
                wOwned.append("")
                wOwned[cur_wpn] = (int(cur_line[1]))

            if cur_line[0] == "end":
                if cur_type == "weapon":
                    cur_wpn += 1
                    #default thing later

wName = []
wDmg = []
wRate = []
wProj = []
wAmmo = []
wRel = []
wAcc = []
wCoil = []
wImg = []
wBul = []
wEff = []
wCost = []
wOwned = []

money = 0

# get the entire file and read it
saveFile = open("stats", "r")
parse_file(saveFile)

