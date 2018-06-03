import pygame

# parses the file for weapons and shield weapons in "open_file"
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
            elif cur_line[0] == "volley":
                wVol.append("")
                wVol[cur_wpn] = (int(cur_line[1]))
            elif cur_line[0] == "fire_rate":
                wRate.append("")
                wRate[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "proj_speed":
                wProj.append("")
                wProj[cur_wpn] = (float(cur_line[1]))
            elif cur_line[0] == "ammo":
                wAmmo.append("")
                wAmmo[cur_wpn] = (int(cur_line[1]))
            elif cur_line[0] == "speed":
                wSpeed.append("")
                wSpeed[cur_wpn] = (float(cur_line[1]))
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
            elif cur_line[0] == "special":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wSpecial.append("")
                wSpecial[cur_wpn] = cur_line[8:]
            elif cur_line[0] == "effect":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wEff.append("")
                wEff[cur_wpn] = cur_line[7:]
            elif cur_line[0] == "sound":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wSound.append("")
                wSound[cur_wpn] = "sounds/" + cur_line[6:] + ".wav"
            elif cur_line[0] == "sound_death":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wExpSound.append("")
                wExpSound[cur_wpn] = "sounds/" + cur_line[12:] + ".wav"
            elif cur_line[0] == "sound_hit":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                wHitSound.append("")
                wHitSound[cur_wpn] = "sounds/" + cur_line[10:] + ".wav"
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


def parse_enemy(open_file):
    cur_line = open_file.readline()
    cur_enemy = 0
    cur_type = ""

    # initial parse for the save
    if cur_line == "save\n":
        pass
    else:
        print("something is wrong with the save file! 'save' is not at the top")
        print(cur_line)
        return

    for line in open_file:
        cur_line = line.split()
        if len(line.strip()) != 0:
            if cur_line[0] == "enemy":
                cur_type = "enemy"
                # name of enemy
                cur_line = open_file.readline().split()
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                eName.append("")  # stop yelling at me pls
                eName[cur_enemy] = (cur_line[0:])
            elif cur_line[0] == "health":
                eHP.append("")
                eHP[cur_enemy] = (int(cur_line[1]))
            elif cur_line[0] == "weapon":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                eWpn.append("")
                eWpn[cur_enemy] = cur_line[7:]
            elif cur_line[0] == "img":
                cur_line = ' '.join(map(str, cur_line))  # joins all words together
                eImg.append("")
                eImg[cur_enemy] = cur_line[4:]
            elif cur_line[0] == "hitbox":
                eBox.append("")
                eBox[cur_enemy] = (int(cur_line[1]))
            elif cur_line[0] == "frequency":
                eFreq.append("")
                eFreq[cur_enemy] = (int(cur_line[1]))
            elif cur_line[0] == "movespeed":
                eSpeed.append("")
                eSpeed[cur_enemy] = (float(cur_line[1]))
            elif cur_line[0] == "boss":
                eBoss.append("")
                eBoss[cur_enemy] = (bool(int(cur_line[1])))

            if cur_line[0] == "end":
                if cur_type == "enemy":
                    cur_enemy += 1


'''
type enemy (enemies must be in the enemies file)
name asdf (names must be unique maybe idk)
health # (integer)
weapon (name of a weapon)
img (name of the image in the enemy_pic/ folder. All pictures should be asdf)
hitbox # (integer, the length/height of the square for the hitbox, more complicated hitboxes later[tm])
rarity # (how common enemies are, uncommon enemies become more common later on, and should be stronger)
mov_speed # (float, pixels per frame, player has 5.0 mov_speed)
boss # (1 = true, 0 = false. Bosses have their own spawning conditions and music)
end
'''

wName = []
wDmg = []
wVol = []
wRate = []
wProj = []
wAmmo = []
wRel = []
wAcc = []
wCoil = []
wImg = []
wBul = []
wSpeed = []
wSpecial = []
wEff = []
wEff2 = []
wSound = []
wExpSound = []
wHitSound = []
wCost = []
wOwned = []

money = 0


eName = []
eHP = []
eWpn = []
eImg = []
eBox = []
eFreq = []
eSpeed = []
eBoss = []


# get the entire file and read it
saveFile = open("datafiles/weapons", "r")
enemyFile = open("datafiles/enemies", "r")
parse_file(saveFile)
parse_enemy(enemyFile)


# default weapons
numWeapons = len(wName)
