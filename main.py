import parse
import pygame
import math
import sys
import random
from pathfinder import ai
import time

# TODO: Add powerups (hp, mana, speed boost, maybe one for inf. ammo?)
# TODO: Add functionality for special weapon effects (explosion, pierce)
# TODO: Add levels and stronger enemies (enemies are done, but not the levels)
# TODO: Add Monies and shop


class Enemy:
    def __init__(self):
        # 3 lazy 5 this
        pass


# appends the folder/name.png thingy to the file, instead of 1just name
def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


# more stackoverflow stuff
def slow_music():
    pass

# finds grid location from coordinates
# GRID SPECIFICATIONS: center of walls start 100 + 37 from the left (100 is taken up by the ui)
#                      and 0 from the top. It is 12x8, first one and last two never have walls
#                      Each wall is 75x75, and is in total a
#                      900x600 grid
def grid_location(x, y):
    loc = [0, 0]
    # x
    loc[0] = int((x - 100)//75)
    loc[1] = int(y//75)

    if loc[0] > 11:
        loc[0] = 11
    elif loc[0] < 0:
        loc[0] = 0
    if loc[1] > 7:
        loc[1] = 7
    elif loc[1] < 0:
        loc[1] = 0

    return loc

# move to the next path tile thing
def move_next_path(curEnemy, egridloc, epath, espeed, xpos):
    if len(epath) > 1:
        # check all 4 directions
        # epath is (y, x) but egridloc is (x, y) cuz reasons
        if egridloc[0] < epath[1][1]:  # move right
            enemyX[curEnemy] += espeed * timeSlow[1]
        elif egridloc[0] > epath[1][1] or xpos > disLength - 30:  # move left
            enemyX[curEnemy] -= espeed * timeSlow[1]
        elif egridloc[1] > epath[1][0]:  # move up
            enemyY[curEnemy] -= espeed * timeSlow[1]
        elif egridloc[1] < epath[1][0]:  # move down
            enemyY[curEnemy] += espeed * timeSlow[1]


# some stackoverflow bs ¯\_(ツ)_/¯
def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


def draw_crosshair(cX, cY, dis, inAcc, curwpn):
    # more spacing = more inaccurate
    spacing = dis / 55 * inAcc + 3
    # right, left, up, down
    if relCD[curWpn] <= 0:
        if curwpn == 2:
            pygame.draw.circle(screen, crossCol, (cX, cY), 8, 3)
        else:
            pygame.draw.circle(screen, crossCol, (cX, cY), 3)
            pygame.draw.line(screen, crossCol, (cX + spacing - 1, cY), (cX + spacing + 3, cY))
            pygame.draw.line(screen, crossCol, (cX - spacing, cY), (cX - spacing - 3, cY))
            pygame.draw.line(screen, crossCol, (cX, cY - spacing), (cX, cY - spacing - 3))
            pygame.draw.line(screen, crossCol, (cX, cY + spacing - 1), (cX, cY + spacing + 3))

    else:  # draw an X during reload
        pygame.draw.line(screen, crossCol, (cX - 10, cY - 10), (cX + 10, cY + 10))
        pygame.draw.line(screen, crossCol, (cX + 10, cY - 10), (cX - 10, cY + 10))


# this calculates angles and shit for the bullets
def calc_bullet(bX, bY, acc):
    global curBul, bulTarX, bulTarY, bulProj, bulAng
    bulAng[curBul] = (math.atan2(-(bulTarY[curBul] - bY), bulTarX[curBul] - bX))
    if acc > 0:
        randomAng = math.radians(random.uniform(-acc, acc))  # add some randomness to the bullets
        bulAng[curBul] = bulAng[curBul] + randomAng

    bulTarY[curBul] = - math.sin(bulAng[curBul]) * bulProj[curBul]
    bulTarX[curBul] = math.cos(bulAng[curBul]) * bulProj[curBul]


# this calculates angles and shit for the bullets
def calc_enemy_bullet(bX, bY, acc):
    global enemyCurBul, enemyBulTarX, enemyBulTarY, enemyBulProj, enemyBulAng
    enemyBulAng[enemyCurBul] = (math.atan2(-(enemyBulTarY[enemyCurBul] - bY), enemyBulTarX[enemyCurBul] - bX))
    if acc > 0:
        randomAng = math.radians(random.uniform(-acc, acc))  # add some randomness to the bullets
        enemyBulAng[enemyCurBul] = enemyBulAng[enemyCurBul] + randomAng

    enemyBulTarY[enemyCurBul] = - math.sin(enemyBulAng[enemyCurBul]) * enemyBulProj[enemyCurBul]
    enemyBulTarX[enemyCurBul] = math.cos(enemyBulAng[enemyCurBul]) * enemyBulProj[enemyCurBul]


# this creates the health bar and mana bar
def create_UI(hp, mp, boss):
    global alertPic
    # draw hp
    screen.fill(UIHp, (20, 30, 20, hp * 20))
    pygame.draw.rect(screen, [0, 0, 0], [20, 30, 20, 200], 2)
    # hp bars, 2 hp ticks
    for i in range(hp // 2 + 1):
        pygame.draw.line(screen, [0, 0, 0], [20, 30 + 40 * i], [40, 30 + 40 * i])
    # draw 1 mark ticks
    #for i in range((hp + 1) // 2):
       # pygame.draw.line(screen, [0, 0, 0], [35, 50 + 40 * i], [40, 50 + 40 * i])

    if boss > 0:
        screen.blit(alertPic, (425, 25))

    # draw mana
    screen.fill(UIMana, (60, 30, 20, int(mp * 2)))
    pygame.draw.rect(screen, [0, 0, 0], [60, 30, 20, 200], 2)
    # for i in range(int(mp) // 20 + 1):
    # pygame.draw.line(screen, [0, 0, 0], (60, 30 + i * 40), (80, 30 + i * 40))


# This function creates the little weapon sprites for switching weapons / displaying ammo
def weapon_UI(img, ammo, max_ammo, num, selected):  # num = weapon from 0 - 2 (top to bottom)
    global relCD, meleeDashCD
    screen.blit(img, (12, 250 + num * 120))
    if selected == num:
        pygame.draw.rect(screen, (0, 0, 0), (8, 250 + num * 120, 84, 70), 1)

    # ammo display
    ammo_words = str(ammo) + " / " + str(max_ammo)
    if relCD[num] > 0:
        ammo_words = "REL " + str(round(relCD[num] / 60, 1))
    elif ammo <= -1:
        ammo_words = "INF"
    ammo_text = ammoFont.render(ammo_words, False, (0, 0, 0))
    screen.blit(ammo_text, (50 - len(ammo_words) * 4.5, 330 + num * 120))
    # draw the dash cd
    if num == 2 and meleeDashCD[0] > 0:
        screen.fill((200, 140, 140), rect=(8, 322 + num * 120, (meleeDashCD[1] - meleeDashCD[0]) * (84 / meleeDashCD[1]), 4))
    elif num == 2 and meleeDashCD[0] <= 0:
        screen.fill((100, 220, 100), rect=(8, 322 + num * 120, (meleeDashCD[1] - meleeDashCD[0]) * (84 / meleeDashCD[1]), 4))


# This moves the player in the 4 cardinal directions + diagonally
def move_player(buttons, pSpd):
    global posX, posY
    num = [0, 0]

    # redoing dis shit, num[0] = x movement, num[1] = y movement
    if buttons[pygame.K_w]:
        if not wall_collision(posX, posY - pSpd, 16):
            num[0] = - pSpd
    elif buttons[pygame.K_s]:
        if not wall_collision(posX, posY + pSpd, 16):
            num[0] = pSpd
    if buttons[pygame.K_d]:
        if not wall_collision(posX + pSpd, posY, 16):
            num[1] = pSpd
    elif buttons[pygame.K_a]:
        if not wall_collision(posX - pSpd, posY, 16):
            num[1] = - pSpd

    # move da player
    if num[0] and num[1] != 0:
        posX += num[1] * 0.7
        posY += num[0] * 0.7
    else:
        posX += num[1]
        posY += num[0]

    # boundaries
    if posX < 120:
        posX = 120
    elif posX > disLength - 20:
        posX = disLength - 20
    if posY < 20:
        posY = 20
    elif posY > disHeight - 20:
        posY = disHeight - 20


# checks for a wall collision given x and y coordinates
def wall_collision(x, y, hitbox):
    global wallRandom, wallRandomY
    for i in range(len(wallRandom)):
        if wallRandom[i] + hitbox + 37 > x > wallRandom[i] - hitbox - 37 and \
                        wallRandomY[i] + hitbox + 37 > y > wallRandomY[i] - hitbox - 37:
            return True
    return False


# check if a fired bullet hits an enemy. x and y are the bullet coords, enemy_x and enemy_y are an array of enemy locations
# returns -1 if no hit, otherwise returns the list location of the hit enemy
def enemy_collision(x, y, enemy_x, enemy_y, enemy_active, box_e, box_bul):
    global numEnemy
    for i in range(numEnemy):
        if enemy_x[i] - box_e[i] / 2 - box_bul < x < enemy_x[i] + box_e[i] / 2 + box_bul and \
                        enemy_y[i] - box_e[i] / 2 - box_bul < y < enemy_y[i] + box_e[i] / 2 + box_bul and enemy_active:
            return i
    return -1


# returns 0 if no hit, otherwise returns 1
def player_collision(x, y, p_x, p_y, box_bul, box_p):
    distance = math.sqrt((abs(p_x - x)**2) + (abs(p_y - y)**2))
    if distance <= box_bul + box_p:
        return 1

    return 0


def draw_map(wall_col, rand, randY):
    pygame.draw.rect(screen, wall_col, (102, 2, 896, 596), 5)
    screen.fill((45, 45, 45), rect=(disLength - 7, 75, 7, 75))
    screen.fill((45, 45, 45), rect=(disLength - 7, disHeight - 150, 7, 75))
    for i in range(len(rand)):
        screen.fill(wall_col, rect=(rand[i] - 38, randY[i] - 38, 76, 76))


def main_menu():
    pass


# calculates if the enemy is in a circle in front of the player
# enemy x, enemy y, and enemy box are arrays of enemy weapons
# returns which enemies were hit
def calc_melee_hit(x, y, enemy_x, enemy_y, enemy_box, melee_box, angle):
    # draw two circles. If the enemy is in the front circle but not in the behind circle, return true
    x_tar = x
    y_tar = y
    x_tar2 = x + (math.sin(angle + math.pi / 2) * - melee_box)
    y_tar2 = y + (math.cos(angle + math.pi / 2) * - melee_box)
    hit_list = []
    for i in range(len(enemy_x)):
        distance = math.sqrt((enemy_x[i] - x_tar) ** 2 + (enemy_y[i] - y_tar) ** 2)
        distance_2 = math.sqrt((enemy_x[i] - x_tar2) ** 2 + (enemy_y[i] - y_tar2) ** 2)
        if distance < melee_box + enemy_box[i] / 2 and distance_2 > melee_box:
            hit_list.append(i)

    return hit_list


# display a standard message at bottom of screen
def msg_display():
    pass


# draw a sp00ky aura
def draw_aura(colour, radius, width):
    pygame.draw.circle(screen, colour, (int(posX), int(posY)), radius, width)


# initiate pygame and cursors
pygame.mixer.pre_init(22050, -16, 6, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
time.sleep(1)

cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
pygame.mouse.set_cursor(*pygame.cursors.diamond)
pygame.mouse.set_visible(False)


# setup the screen and main clock
disLength = 1000
disHeight = 600
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("shooty")
clock = pygame.time.Clock()

ammoFont = pygame.font.SysFont('Courier New', 15)
msgFont = pygame.font.SysFont('Courier New', 20, True)

# background and objects like walls
backCol = [240, 240, 240]
UIBod = [125, 125, 225]
UICol = [210, 230, 240]
UISlow = [180, 200, 210]
UIHp = [250, 70, 70]
UIMana = [100, 100, 240]
wallCol = [120, 120, 120]
crossCol = [0, 40, 10]
UIHeal = [70, 250, 70]
UIDmg = [252, 252, 252]

# GRID SPECIFICATIONS: center of walls start 125 + 37 from the left (100 is taken up by the ui)
#                      and 0 from the top. It is 11x8, first one and last two never have walls
#                      Ends at last 50 units from the right. Each wall is 75x75, and is in total a
#                      825x600 grid
wallRandom = []
wallRandomY = []
wallCoords = []  # walls on the 12x8 array
wallCount = 0  # number of walls in total, should not exceed 8
wallCountC = 0  # number of walls in a single column, should not exceed 3
ran = 0
wallGrid = []

for i in range(12):  # x axis
    wallGrid.append([])
    wallCountC = 0
    for k in range(8):  # y axis
        # better walls[tm]
        if random.randint(0, 60) + ran >= 56 and 1 <= i <= 10 and wallCountC < 3 and wallCount < 9:
            wallGrid[i].append(1)
            wallCountC += 1
            wallCount += 1
            ran = 5
            wallRandom.append(100 + i * 75 + 37)  # center of the wall X and Y
            wallRandomY.append(k * 75 + 37)
            wallCoords.append([i, k])
        else:
            wallGrid[i].append(0)
            ran = 0

# global game variables
level = 0
levelTimer = 1200  # increase level every 20 or 30sec
timeBuffer = [0, 20]  # used so that pressing space doesn't accidentally do it 2 times
timeSlow = [1.0, 1.0]  # self slow, enemy slow
score = 0

bossMode = False
bossSpawnDelay = -6
bossRarity = 10  # usually 10
bossMinSeparation = 10  # kill 10 enemies at least before another boss can spawn

# alert sound and picture
alertPic = pygame.image.load("effects/alert.png")
alertSound = pygame.mixer.Sound("sounds/alert.wav")

# player variables
playerImg = pygame.image.load("player.png").convert_alpha()
posX = 150.0  # start in the top left corner
posY = 50.0
baseSpeed = 4.5
health = [10, 10]  # cur/max hp
mana = [100, 100]  # cur/max mana
manaChargeDelay = [0, 30]  # number of ticks of delay before mana starts to recharge
manaUseSpeed = [20, 10]  # usage rate / recharge rate per second
fireCD = 0.0  # used when shooting
wpnAmmo = [parse.wAmmo[0], parse.wAmmo[1], parse.wAmmo[2]]
wpnInAcc = [parse.wAcc[0], parse.wAcc[1], parse.wAcc[2]]
relCD = [0, 0, 0]  # used by weapon 1, 2, and 3 when reloading.
curWpn = 0
speed = baseSpeed * parse.wSpeed[curWpn]  # this changes based on the weapon
atkSound = pygame.mixer.Sound(parse.wSound[curWpn])

# for ai
gridLoc = [0, 0]

# death red screen
deathTimer = -2
deathImg = load_pics("ui/", "redscreen")

# effect pictures and stuff
expSmall = pygame.image.load("effects/exp_small.png").convert_alpha()

# player bullet variables
bulImg = [parse.wBul] * 30  # should probably add different pictures
effImg = [expSmall] * 30
effImg2 = [""] * 30
bulX = [-50.0] * 30
bulY = [-50.0] * 30
active = [0] * 30
bulDmg = [0] * 30
bulProj = [0.0] * 30
bulTarX = [-50.0] * 30
bulTarY = [-50.0] * 30
bulAng = [0.0] * 30
bulSpec = ["none"] * 30
bulExpSound = [parse.wExpSound[curWpn]] * 30
bulHitSound = [parse.wHitSound[curWpn]] * 30
curBul = 0

outOfAmmoSound = pygame.mixer.Sound('sounds/noammo.wav')

# 2nd frame of effects (optional)
for i in range(len(parse.wEff)):
    try:
        parse.wEff2.append(load_pics("effects/", "1" + parse.wEff[i]))
    except pygame.error:
        parse.wEff2.append("")
# weapon sprites and effects
for i in range(len(parse.wImg)):
    parse.wImg[i] = load_pics("weapons/", parse.wImg[i])
for i in range(len(parse.wBul)):
    parse.wBul[i] = load_pics("projectiles/", parse.wBul[i])
for i in range(len(parse.wEff)):
    parse.wEff[i] = load_pics("effects/", parse.wEff[i])

# ENEMY STUFF
# global weapons
numEnemy = 6  # add more if needed!

# individual weapons
for i in range(len(parse.eImg)):
    parse.eImg[i] = load_pics("enemy_pic/", parse.eImg[i])

enemyReEvaluate = [0, 5]  # every 5 ticks re evaluate the path chosen

# enemy weapons
enemyHP = [parse.eHP[0]] * numEnemy
enemyMaxHP = enemyHP * numEnemy  # used for the HP bar
enemyImg = [parse.eImg[0]] * numEnemy
enemyBox = [parse.eBox[0]] * numEnemy
enemySpeed = [parse.eSpeed[0]] * numEnemy
enemyIsBoss = [False] * numEnemy
enemyX = [disLength + 40] * numEnemy
enemyY = [75 + 37] * numEnemy
enemyGridLoc = grid_location(75 + 37, disLength - 10) * numEnemy
enemyTar = [[0, 0]] * numEnemy  # an array of tile positions, where the enemy wants to move
enemyNextTar = [[0, 0]] * numEnemy  # which x, y direction enemy should move to (e.g. [-1,0] is West)
enemyPath = [[]] * numEnemy
enemyActive = [False] * numEnemy
enemyShootDelay = [30] * numEnemy  # ticks down, enemy shoots when it hits 0
enemyScore = [0] * numEnemy

# weapons for the enemy weapons
enemyBulImg = [parse.wBul] * 30  # should probably add different pictures
enemyEffImg = [expSmall] * 30
enemyEffImg2 = [""] * 30
enemyBulX = [-50.0] * 30
enemyBulY = [-50.0] * 30
enemyBulActive = [0] * 30
enemyBulDmg = [0] * 30
enemyBulProj = [0.0] * 30
enemyBulTarX = [-50.0] * 30
enemyBulTarY = [-50.0] * 30
enemyBulAng = [0.0] * 30
enemyBulSpec = ["none"] * 30
enemyBulExpSound = [parse.wExpSound[curWpn]] * 30
enemyBulHitSound = [parse.wHitSound[curWpn]] * 30
enemyCurBul = 0

enemyWpnIndex = [0] * numEnemy  # index location of its weapon in the main list

enemySpawn = 0

# load sounds, channel 0 is reserved for music, all others used for sound effects
ingameMusic = pygame.mixer.music.load('sounds/ftl soundtrack.ogg')
pygame.mixer.set_num_channels(10)
pygame.mixer.music.set_volume(1.0)  # volume value between 0 and 1
pygame.mixer.music.play(-1)
# slow motion music

# power ups
healthPack = pygame.image.load("powerup/health_pack.png").convert_alpha()
attackspeedPack = pygame.image.load("powerup/attackspeed_pack.png").convert_alpha()

powerupCD = random.randint(450, 900)  # spawn a powerup when this reaches
powerupCoords = [0, 0]
activePowerup = 0  # delay before powerupCD counts down, usually depends on duration of powerup
powerupType = "none"

# powerup sounds
spawnSound = pygame.mixer.Sound("sounds/spawn.wav")
pickupHealth = pygame.mixer.Sound("sounds/pickupHealth.wav")
pickupAtkSpd = pygame.mixer.Sound("sounds/pickupAtkSpd.wav")

# health change animations
changeAnimation = 0

# ========= GAME LOGIC ========= #
# LIST OF ALL WEAPONS (not including WIP)
# Shotgun, Sub Machine Gun, Pistol, Katana. A melee weapon should always be the 3rd weapon
EqWpnName = ["Shotgun", "Pistol", "Katana"]  # the 2 weapons used

for i in range(2, -1, -1):
    if EqWpnName[i] in parse.wName:
        ArrayLoc = parse.wName.index(EqWpnName[i])
        # theres DEFINITELY a better way of doing dis
        parse.wName = [parse.wName[ArrayLoc]] + parse.wName
        parse.wDmg = [parse.wDmg[ArrayLoc]] + parse.wDmg
        parse.wVol = [parse.wVol[ArrayLoc]] + parse.wVol
        parse.wRate = [parse.wRate[ArrayLoc]] + parse.wRate
        parse.wProj = [parse.wProj[ArrayLoc]] + parse.wProj
        parse.wAmmo = [parse.wAmmo[ArrayLoc]] + parse.wAmmo
        parse.wRel = [parse.wRel[ArrayLoc]] + parse.wRel
        parse.wAcc = [parse.wAcc[ArrayLoc]] + parse.wAcc
        parse.wCoil = [parse.wCoil[ArrayLoc]] + parse.wCoil
        parse.wImg = [parse.wImg[ArrayLoc]] + parse.wImg
        parse.wBul = [parse.wBul[ArrayLoc]] + parse.wBul
        parse.wSpeed = [parse.wSpeed[ArrayLoc]] + parse.wSpeed
        parse.wEff = [parse.wEff[ArrayLoc]] + parse.wEff
        parse.wEff2 = [parse.wEff2[ArrayLoc]] + parse.wEff2
        parse.wSpecial = [parse.wSpecial[ArrayLoc]] + parse.wSpecial
        parse.wSound = [parse.wSound[ArrayLoc]] + parse.wSound
        parse.wExpSound = [parse.wExpSound[ArrayLoc]] + parse.wExpSound
        parse.wHitSound = [parse.wHitSound[ArrayLoc]] + parse.wHitSound
        parse.wCost = [parse.wCost[ArrayLoc]] + parse.wCost
        parse.wOwned = [parse.wOwned[ArrayLoc]] + parse.wOwned
    else:
        print("A weapon was not found in the data!!! F")

wpnName = [parse.wName[0], parse.wName[1], parse.wName[2]]  # the 2 weapons used
wpnAmmo = [parse.wAmmo[0], parse.wAmmo[1], parse.wAmmo[2]]
wpnInAcc = [parse.wAcc[0], parse.wAcc[1], parse.wAcc[2]]
relCD = [0, 0, 0]  # used by weapon 1 and weapon 2 when reloading.
curWpn = 0
speed = baseSpeed * parse.wSpeed[curWpn]  # this changes based on the weapon
atkSound = pygame.mixer.Sound(parse.wSound[curWpn])


# melee stuff
# animations, coords, etc.
meleeAnimation = 0
meleeAngle = 0
meleeImg = parse.wBul[2]
meleeDashCD = [0, 120]  # base, dash max cd
dashAlreadyHit = []  # list of enemies already hit
dashAngle = 0
dashSpeed = 20  # constant
dashImg = load_pics("projectiles/", parse.wName[2] + "_dash")
# the change in x and y when dashing
meleeX = 0
meleeY = 0
dashTarget = [-50, -50]
dummyBullets = load_pics("projectiles/", "dummy")

# ========= MAIN LOOP =========
while deathTimer != 0:
    screen.fill(backCol)

    # increase level, which increases difficulty by spawning higher level enemies
    levelTimer -= 1 * timeSlow[1]
    if levelTimer <= 0:
        levelTimer = 1800  # 30sec per level
        level += 1
        print("level increased! Level: ", level)

    activePowerup -= 1 * timeSlow[0]
    if activePowerup <= 0:
        powerupCD -= 1 * timeSlow[1]

    enemySpawn -= 1 * timeSlow[1]
    if bossSpawnDelay >= 0:
        bossSpawnDelay -= 1 * timeSlow[1]

    # tick down timers, recharge mana
    for i in range(numEnemy):
        enemyShootDelay[i] += -1 * timeSlow[1]
    if meleeDashCD[0] > 0:
        meleeDashCD[0] -= 1 * timeSlow[0]

    if deathTimer > 0:
        deathTimer -= 1

    enemyReEvaluate[0] += -1

    timeBuffer[0] += -1
    fireCD += -1 * timeSlow[0]

    # handle reloading
    for i in range(2):
        if relCD[i] > 0 and curWpn == i:
            relCD[i] += -1 * timeSlow[0]
        elif relCD[i] > 0 and curWpn != i:
            relCD[i] = parse.wRel[i] * 60
        if -2 <= relCD[i] <= 0:
            wpnAmmo[i] = parse.wAmmo[i]
            relCD[i] += -3

    # use mana if ability is active
    if (timeSlow[0] != 1 or timeSlow[1] != 1) and deathTimer < 0:
        mana[0] -= manaUseSpeed[0] / 60
    else:  # recharge mana after the delay
        manaChargeDelay[0] += -1
        if manaChargeDelay[0] <= 0 and mana[0] < mana[1]:
            mana[0] += manaUseSpeed[1] / 60
    # stop powerup if run out of mana
    if mana[0] <= 0:
        timeSlow[0] = 1.0
        timeSlow[1] = 1.0
        # pygame.mixer.music.set_volume(1.0)

    # ------------ POWERUP STUFF ---------- #
    # spawn powerup
    if -2 <= powerupCD <= 0:
        powerupCD -= 5
        # set random location
        powerupCoords[0] = random.randint(140, 940)
        powerupCoords[1] = random.randint(40, 540)
        # make sure it doesnt spawn on top of wall or player, re-randomize if it does
        while wall_collision(powerupCoords[0], powerupCoords[1], 25) or \
                player_collision(powerupCoords[0], powerupCoords[1], posX, posY, 40, 25):
                powerupCoords[0] = random.randint(150, 950)
                powerupCoords[1] = random.randint(50, 550)

        powerupSpawnRNG = random.randint(1, 2)
        if powerupSpawnRNG == 1:
            powerupType = "health"
        elif powerupSpawnRNG == 2:
            powerupType = "ammoPack"
        spawnSound.play()

    # collect a powerup
    if player_collision(powerupCoords[0], powerupCoords[1], posX, posY, 20, 10):
        # heal 2 points, maybe play animation?
        if powerupType == "health":
            activePowerup = 100
            # this is for the green flash in the hp bar
            changeAnimation = (health[1] - health[0]) * 20
            if changeAnimation > 80:
                changeAnimation = 80
            # play sound
            pickupHealth.play()
            # make sure hp doesnt go above 10
            health[0] += 4
            if health[0] > health[1]:
                health[0] = health[1]

        # increase attack speed for 8 sec and makes guns have inf. ammo
        elif powerupType == "ammoPack":
            activePowerup = 480
            for i in range(3):
                relCD[i] = -4
                wpnAmmo[i] = -1
            # play sound [soon tm]
            pickupAtkSpd.play()

        # this is derpy, move the powerup so that the player cant repeatedly get it
        powerupCoords[0] = -200
        powerupCoords[1] = -200
        powerupCD = random.randint(900, 1800)

    # draw powerup
    if powerupCD <= 0:
        if powerupType == "health":
            screen.blit(healthPack, (powerupCoords[0] - healthPack.get_rect()[3] / 2, powerupCoords[1] - healthPack.get_rect()[3] / 2))
        elif powerupType == "ammoPack":
            screen.blit(attackspeedPack, (powerupCoords[0] - attackspeedPack.get_rect()[3] / 2,
                                          powerupCoords[1] - attackspeedPack.get_rect()[3] / 2))

    # do the effects of powerups
    if activePowerup > 0 and powerupType == "ammoPack":
        fireCD -= 1 * timeSlow[0] / 2  # tick it down AGAIN!! by half
        # draw a yellow aura around the player
        draw_aura((200, 200, 90), 24, 8)
    if -2 <= activePowerup <= 0 and powerupType == "ammoPack":
        for i in range(3):
            wpnAmmo[i] = parse.wAmmo[i]

    # ------------ ENEMY STUFF ------------ #

    # enemy spawning
    # TODO: add sounds when enemy shoots
    if enemySpawn <= 0 and bossSpawnDelay < -5:
        # lower spawn rates if lots of enemies already there
        numEnemyAlive = enemyActive.count(True)
        enemySpawn = random.randint(90, 180) + (numEnemyAlive * random.randint(10, 20))
        if numEnemyAlive < numEnemy:
            # this spawns a random enemy by first rolling random number from 1 to 10
            # NOTE: REQUIRES AT LEAST ONE ENEMY TO HAVE 10 FREQUENCY
            spawnNum = random.randint(1, 10)
            tempSpawnList = []
            for i in range(len(parse.eFreq)):
                # if frequency is greater than the rolled number, add to pool, then
                # choose a random enemy in the pool to spawn. Rarer enemies also increase the next spawn time.
                if parse.eFreq[i] >= spawnNum - level and parse.eBoss[i] == 0:
                    tempSpawnList.append(i)
            spawnNum = random.randint(0, len(tempSpawnList) - 1)
            selection = tempSpawnList[spawnNum]

            # gets the next dead enemy in list
            nextEnemy = enemyActive.index(False)

            # reset weapons
            enemyHP[nextEnemy] = parse.eHP[selection]
            enemyMaxHP[nextEnemy] = enemyHP[nextEnemy] # used for the HP bar
            enemyImg[nextEnemy] = parse.eImg[selection]
            enemyBox[nextEnemy] = parse.eBox[selection]
            enemySpeed[nextEnemy] = parse.eSpeed[selection]
            enemyIsBoss[nextEnemy] = False
            enemyScore[nextEnemy] = parse.eScore[selection]
            # equip gun
            enemyWpnIndex[nextEnemy] = parse.wName.index(parse.eWpn[selection])
            enemyShootDelay[nextEnemy] = 60 / parse.wRate[enemyWpnIndex[nextEnemy]] * random.uniform(1, 1.5)  # add a bit of unpredictability

            # spawn enemy, randomize location
            spawnLoc = random.randint(0, 1)
            if spawnLoc == 0:
                enemyX[nextEnemy] = disLength + 40
                enemyY[nextEnemy] = 75 + 37
            elif spawnLoc == 1:
                enemyX[nextEnemy] = disLength + 40
                enemyY[nextEnemy] = disHeight - 75 - 37

            enemyActive[nextEnemy] = True
            # increase spawn delay if there is a boss
            if bossMode:
                enemySpawn *= 1.5
                enemySpawn += 100

            # roll for a boss every x enemies
            if random.randint(1, bossRarity) == 1 and bossMinSeparation <= 0 and not bossMode:
                bossMode = True
                bossSpawnDelay = 300
                enemySpawn += 450
                alertSound.play()


    elif bossMode and -2 <= bossSpawnDelay <= 0:
        bossSpawnDelay -= 6
        # spawn boss, basically same as normal enemy
        numEnemyAlive = enemyActive.count(True)
        if numEnemyAlive < numEnemy:
            # this spawns a random enemy by first rolling random number from 1 to 10
            # NOTE: REQUIRES AT LEAST ONE ENEMY TO HAVE 10 FREQUENCY
            spawnNum = random.randint(1, 10)
            tempSpawnList = []
            for i in range(len(parse.eFreq)):
                # if frequency is greater than the rolled number AND its a boss, add to pool
                if parse.eFreq[i] >= spawnNum - level and parse.eBoss[i] == 1:
                    tempSpawnList.append(i)
            spawnNum = random.randint(0, len(tempSpawnList) - 1)
            selection = tempSpawnList[spawnNum]

            # gets the next dead enemy in list
            nextEnemy = enemyActive.index(False)

            # reset weapons
            enemyHP[nextEnemy] = parse.eHP[selection] * (1 + level * 0.05)  # bosses gain 5% more hp every level
            enemyMaxHP[nextEnemy] = enemyHP[nextEnemy]
            enemyImg[nextEnemy] = parse.eImg[selection]
            enemyBox[nextEnemy] = parse.eBox[selection]
            enemySpeed[nextEnemy] = parse.eSpeed[selection]
            enemyScore[nextEnemy] = parse.eScore[selection]
            enemyIsBoss[nextEnemy] = True
            # equip gun
            enemyWpnIndex[nextEnemy] = parse.wName.index(parse.eWpn[selection])
            enemyShootDelay[nextEnemy] = 60 / parse.wRate[enemyWpnIndex[nextEnemy]] * random.uniform(1, 1.5)  # add a bit of unpredictability

            # spawn enemy, randomize location
            spawnLoc = random.randint(0, 1)
            if spawnLoc == 0:
                enemyX[nextEnemy] = disLength + 40
                enemyY[nextEnemy] = 75 + 37
            elif spawnLoc == 1:
                enemyX[nextEnemy] = disLength + 40
                enemyY[nextEnemy] = disHeight - 75 - 37

            enemyActive[nextEnemy] = True

    # Every 0.5sec, evaluate a path for every enemy to the player
    # path finding for the enemies, using some shady algorithm from online
    if enemyReEvaluate[0] <= 0:
        gridLoc = grid_location(posX, posY)

        enemyReEvaluate[0] = int(enemyReEvaluate[1] * random.uniform(0.5, 1.0))
        # loop through all of the enemies and get da paths
        for i in range(numEnemy):
            if 40 < (enemyX[i] + 50) % 75 < 60 and 0 < (enemyY[i] + 50) % 75 < 20 or enemyX[i] > disLength:
                if enemyActive[i]:
                    enemyGridLoc[i] = grid_location(enemyX[i], enemyY[i])
                    # print("loc:", enemyGridLoc)
                    enemyPath[i] = ai.find_path(wallGrid, enemyGridLoc[i], gridLoc)
                    # print("path:", enemyPath)

    # enemy movement
    for i in range(numEnemy):
        if enemyActive[i]:
            # do everything
            move_next_path(i, enemyGridLoc[i], enemyPath[i], enemySpeed[i], enemyX[i])
            # draw!
            screen.blit(enemyImg[i], (enemyX[i] - enemyBox[i] / 2, enemyY[i] - enemyBox[i] / 2))

    # enemy shooting
    for i in range(numEnemy):
        if enemyActive[i]:
            if enemyShootDelay[i] <= 0:
                # randomness, up to 1.5x the rated time delay
                enemyShootDelay[i] = (60 * random.uniform(1, 1.5)) / parse.wRate[enemyWpnIndex[i]]
                for k in range(parse.wVol[enemyWpnIndex[i]]):
                    enemyCurBul += 1
                    if enemyCurBul >= 30:
                        enemyCurBul = 0
                    # set some bullet variables
                    #
                    enemyBulX[enemyCurBul] = enemyX[i]
                    enemyBulY[enemyCurBul] = enemyY[i]
                    enemyBulActive[enemyCurBul] = 1
                    enemyBulTarX[enemyCurBul] = posX
                    enemyBulTarY[enemyCurBul] = posY
                    enemyBulDmg[enemyCurBul] = parse.wDmg[enemyWpnIndex[i]]
                    enemyBulProj[enemyCurBul] = parse.wProj[enemyWpnIndex[i]]
                    enemyBulSpec[enemyCurBul] = parse.wSpecial[enemyWpnIndex[i]]
                    # do the same thing for player bullets but with enemy bullets
                    calc_enemy_bullet(enemyBulX[enemyCurBul], enemyBulY[enemyCurBul], parse.wAcc[enemyWpnIndex[i]])
                    enemyBulImg[enemyCurBul] = rot_center(parse.wBul[enemyWpnIndex[i]], math.degrees(enemyBulAng[enemyCurBul]))
                    enemyEffImg[enemyCurBul] = parse.wEff[enemyWpnIndex[i]]
                    enemyEffImg2[enemyCurBul] = parse.wEff2[enemyWpnIndex[i]]
                    enemyBulExpSound[enemyCurBul] = pygame.mixer.Sound(parse.wExpSound[enemyWpnIndex[i]])
                    enemyBulHitSound[enemyCurBul] = pygame.mixer.Sound(parse.wHitSound[enemyWpnIndex[i]])

    # draw enemy bullets and make them hit things
    # yes this code is copied from the player bullet section
    # also yes i should have made it a class so i wouldnt have to copy it from the player bullet section
    # displaying and resetting bullets
    for i in range(30):
        if enemyBulActive[i] > 0:
            # check if the bullet hits a wall or enemy, else display it
            # number of times to check for collision
            gap = int(math.sqrt(enemyBulTarX[i] ** 2 + enemyBulTarY[i] ** 2)) // 8 + 1
            for j in range(gap):
                # check if the bullet hits a wall or player
                # returns 1 if hit player, 0 if it did not
                eCenter = enemyBulImg[i].get_rect()
                playerHitCheck = player_collision(enemyBulX[i], enemyBulY[i], posX, posY, 2, 16)
                if (wall_collision(enemyBulX[i], enemyBulY[i], 2) or enemyBulX[i] + 10 > disLength or enemyBulX[i] < 110 \
                        or enemyBulY[i] + 10 > disHeight or enemyBulY[i] < 10) and enemyBulSpec[i] != "phase":

                    # draw the bullet for one frame before death
                    screen.blit(enemyBulImg[i], (enemyBulX[i] - (eCenter[2] / 2), enemyBulY[i] - (eCenter[3] / 2)))
                    enemyBulActive[i] = -1
                    # change picture to explosion!!!
                    enemyBulImg[i] = enemyEffImg[i]
                    enemyBulExpSound[i].play()
                    break

                # check if the bullet hits the player
                elif playerHitCheck == 1:
                    # draw the bullet for one frame before removal
                    screen.blit(enemyBulImg[i], (enemyBulX[i] - (eCenter[2] / 2), enemyBulY[i] - (eCenter[3] / 2)))
                    enemyBulActive[i] = -1
                    # change picture to explosion!!!
                    enemyBulImg[i] = enemyEffImg[i]
                    # invincibility frames if there was a recent dash
                    if meleeDashCD[0] > meleeDashCD[1] - 11:
                        enemyBulExpSound[i].play()
                    else:
                        enemyBulHitSound[i].play()
                        health[0] -= enemyBulDmg[i]
                        # animation stuffs
                        changeAnimation -= 20 * enemyBulDmg[i]
                        if health[0] <= 0 and deathTimer < 0:
                            # set variables on death, play death music
                            deathTimer = 240
                            pygame.mixer.music.load('sounds/wasted.ogg')
                            timeSlow = [0.1, 0.1]
                            pygame.mixer.music.play(0)
                    break

                else:
                    enemyBulX[i] += enemyBulTarX[i] * timeSlow[1] / gap
                    enemyBulY[i] += enemyBulTarY[i] * timeSlow[1] / gap
                    # add hitting enemies here
                if j == gap - 1:
                    eCenter = enemyBulImg[i].get_rect()
                    screen.blit(enemyBulImg[i], (enemyBulX[i] - (eCenter[2]/2), enemyBulY[i] - (eCenter[3]/2)))

    # particle effects for enemy bullets
    for i in range(30):
        if -4 <= enemyBulActive[i] < 0:
            screen.blit(enemyBulImg[i], (enemyBulX[i] - 45, enemyBulY[i] - 45))
            enemyBulActive[i] += -1 * timeSlow[1]

    # ------------ PLAYER STUFF ------------ #
    pressed = pygame.key.get_pressed()

    # lose inaccuracy from recoil
    for i in range(3):
        if wpnInAcc[i] > parse.wAcc[i]:
            wpnInAcc[i] = wpnInAcc[i] - timeSlow[0] * ((wpnInAcc[i] - parse.wAcc[i]) * 0.03) - 0.01
        else:
            wpnInAcc[i] = parse.wAcc[i]

    # SLOW DOWN TIME...
    if timeBuffer[0] <= 0 and pressed[pygame.K_SPACE]:
        timeBuffer[0] = timeBuffer[1]
        if timeSlow[0] != 1 or timeSlow[1] != 1:
            timeSlow = [1.0, 1.0]

        elif mana[0] > 0:
            timeSlow = [1.0, 0.3]  # self slow, enemy slow
            manaChargeDelay[0] = manaChargeDelay[1]

    # move player and display player
    if meleeDashCD[0] < meleeDashCD[1] - 10:
        move_player(pressed, speed * timeSlow[0])

    screen.blit(playerImg, (posX - 20, posY - 20))

    # switch weapon (knife, wpn 0, wpn 1)
    if pressed[pygame.K_1]:
        curWpn = 0
        atkSound = pygame.mixer.Sound(parse.wSound[curWpn])
        speed = baseSpeed * parse.wSpeed[curWpn]
        if fireCD <= 15:
            fireCD = 15
    elif pressed[pygame.K_2]:
        curWpn = 1
        atkSound = pygame.mixer.Sound(parse.wSound[curWpn])
        speed = baseSpeed * parse.wSpeed[curWpn]
        if fireCD <= 15:
            fireCD = 15
    elif pressed[pygame.K_3]:
        curWpn = 2
        atkSound = pygame.mixer.Sound(parse.wSound[curWpn])
        speed = baseSpeed * parse.wSpeed[curWpn]
        if fireCD <= 15:
            fireCD = 15

    # ------------ SHOOTING AND BULLET STUFF ------------ #
    # shooting
    mousePos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()

    # manual reload
    if pressed[pygame.K_r] and -1 < wpnAmmo[curWpn] < parse.wAmmo[curWpn] and relCD[curWpn] <= 0:
        relCD[curWpn] = parse.wRel[curWpn] * 60

    # shoot
    if mouse[0] == 1 and fireCD <= 0 and relCD[curWpn] <= 0:
        # set cooldown and automatic reload
        fireCD = 60 / parse.wRate[curWpn]
        wpnAmmo[curWpn] += -1
        if wpnAmmo[curWpn] == 0:
            relCD[curWpn] = parse.wRel[curWpn] * 60  # RELOAD HERE

        # do special stuff for melee weapons
        if parse.wSpecial[curWpn] == "melee":
            atkSound.play()
            meleeAngle = (math.atan2(-(mousePos[1] - posY), mousePos[0] - posX))
            meleeAnimation = 5
            meleeImg = rot_center(parse.wBul[2], math.degrees(meleeAngle))
            enemiesHit = calc_melee_hit(posX, posY, enemyX, enemyY, enemyBox, 85, meleeAngle)

            for i in range(len(enemiesHit)):
                if enemyActive[enemiesHit[i]]:
                    # spawn dummy bullets there for effect
                    curBul += 1
                    if curBul >= 30:
                        curBul = 0
                    bulX[curBul] = enemyX[enemiesHit[i]]
                    bulY[curBul] = enemyY[enemiesHit[i]]
                    active[curBul] = -1
                    bulImg[curBul] = parse.wEff[curWpn]
                    effImg2[curBul] = parse.wEff2[curWpn]
                    bulHitSound[curBul] = pygame.mixer.Sound(parse.wHitSound[curWpn])
                    bulHitSound[curBul].play()

                    # do damage to enemies, bosses take 2x damage from melee
                    #if enemyIsBoss[enemiesHit[i]]:
                        #enemyHP[enemiesHit[i]] -= parse.wDmg[curWpn] * 2
                    #else:
                    enemyHP[enemiesHit[i]] -= parse.wDmg[curWpn]
                    if enemyHP[enemiesHit[i]] <= 0:
                        enemyActive[enemiesHit[i]] = False
                        score += enemyScore[enemiesHit[i]]
                        enemyX[enemiesHit[i]] = disLength + 25
                        enemyY[enemiesHit[i]] = 75 + 37
                        if enemyIsBoss[enemiesHit[i]]:
                            bossMode = False
                            bossMinSeparation = 10
                        elif not bossMode:
                            bossMinSeparation -= 1

        # randomize every bullet in the volley
        else:
            for i in range(parse.wVol[curWpn]):
                curBul += 1
                if curBul >= 30:
                    curBul = 0
                # set some bullet variables
                bulX[curBul] = posX
                bulY[curBul] = posY
                active[curBul] = 1
                bulTarX[curBul] = mousePos[0]
                bulTarY[curBul] = mousePos[1]
                bulDmg[curBul] = parse.wDmg[curWpn]
                bulProj[curBul] = parse.wProj[curWpn]
                bulSpec[curBul] = parse.wSpecial[curWpn]
                # TRIG YAY
                calc_bullet(bulX[curBul], bulY[curBul], wpnInAcc[curWpn])
                bulImg[curBul] = rot_center(parse.wBul[curWpn], math.degrees(bulAng[curBul]))
                effImg[curBul] = parse.wEff[curWpn]
                effImg2[curBul] = parse.wEff2[curWpn]
                bulExpSound[curBul] = pygame.mixer.Sound(parse.wExpSound[curWpn])
                bulHitSound[curBul] = pygame.mixer.Sound(parse.wHitSound[curWpn])

            # recoil!
            wpnInAcc[curWpn] += parse.wCoil[curWpn]
            # sounds
            atkSound.play()

    # draw melee attack
    if meleeAnimation > 0:
        meleeAnimation -= 1 * timeSlow[0]
        center = meleeImg.get_rect()
        screen.blit(meleeImg, (posX - center[2] / 2, posY - center[3] / 2))

    # special melee dash attacks
    elif mouse[2] == 1 and meleeDashCD[0] <= 0 and parse.wSpecial[curWpn] == "melee" and meleeAnimation <= 0:
        # play sounds, set target and cd
        atkSound.play()
        dashTarget = [mousePos[0], mousePos[1]]
        meleeDashCD[0] = meleeDashCD[1]
        # calculate angle and change in x and y
        dashAngle = (math.atan2(-(dashTarget[1] - posY), dashTarget[0] - posX))
        dashAlreadyHit = []
        dashImgRotated = rot_center(dashImg, math.degrees(dashAngle))
        meleeY = - math.sin(dashAngle) * dashSpeed
        meleeX = math.cos(dashAngle) * dashSpeed
        if fireCD < 20:
            fireCD = 20

    # dash forward
    if meleeDashCD[0] >= meleeDashCD[1] - 10:
        # make sure you dont bump into wall, move character otherwise
        if not wall_collision(posX + meleeX / 2, posY + meleeY / 2, 16):
            posX += meleeX / 2 * timeSlow[0]
            posY += meleeY / 2 * timeSlow[0]
        enemiesHit = calc_melee_hit(posX, posY, enemyX, enemyY, enemyBox, 35, dashAngle)
        if not wall_collision(posX + meleeX / 2, posY + meleeY / 2, 16):
            posX += meleeX / 2 * timeSlow[0]
            posY += meleeY / 2 * timeSlow[0]
        # display a little wave while dashing
        dCenter = dashImgRotated.get_rect()
        screen.blit(dashImgRotated, (posX - dCenter[2] / 2, posY - dCenter[3] / 2))
        for i in range(len(enemiesHit)):
            if enemiesHit[i] not in dashAlreadyHit and enemyActive[enemiesHit[i]]:
                # spawn dummy bullets there for effect
                curBul += 1
                if curBul >= 30:
                    curBul = 0
                bulX[curBul] = enemyX[enemiesHit[i]]
                bulY[curBul] = enemyY[enemiesHit[i]]
                active[curBul] = -1
                bulImg[curBul] = parse.wEff[curWpn]
                effImg2[curBul] = parse.wEff2[curWpn]
                bulHitSound[curBul] = pygame.mixer.Sound(parse.wHitSound[curWpn])
                bulHitSound[curBul].play()
                dashAlreadyHit.append(enemiesHit[i])

                # do damage to enemies, bosses take 2x dmg from melee weapons3
                #if enemyIsBoss[enemiesHit[i]]:
                    #enemyHP[enemiesHit[i]] -= 2 * parse.wDmg[2]
                #else:
                enemyHP[enemiesHit[i]] -= parse.wDmg[2]
                if enemyHP[enemiesHit[i]] <= 0:
                    enemyActive[enemiesHit[i]] = False
                    score += enemyScore[i]
                    enemyX[enemiesHit[i]] = disLength + 25
                    enemyY[enemiesHit[i]] = 75 + 37
                    if enemyIsBoss[enemiesHit[i]]:
                        bossMode = False
                        bossMinSeparation = 10
                    elif not bossMode:
                        bossMinSeparation -= 1

    # out of ammo sound
    elif mouse[0] == 1 and fireCD <= 0 and relCD[curWpn] > 0:
        outOfAmmoSound.play()
        fireCD = 60 / parse.wRate[curWpn]
        if fireCD > relCD[curWpn]:
            fireCD = relCD[curWpn]

    # displaying and resetting bullets
    for i in range(30):
        if active[i] > 0:
            # check if the bullet hits a wall or enemy, else display it
            gap = int(math.sqrt(bulTarX[i] ** 2 + bulTarY[i] ** 2)) // 8 + 1  # number of times to check for collision
            for j in range(gap):
                # check if the bullet hits a wall
                center = bulImg[i].get_rect()
                enemyCheck = enemy_collision(bulX[i], bulY[i], enemyX, enemyY, enemyActive, enemyBox, 2)
                if (wall_collision(bulX[i], bulY[i], 2) or bulX[i] + 10 > disLength or bulX[i] < 110 or bulY[i] + 10 > disHeight or bulY[i] < 10)\
                        and bulSpec[i] != "phase":
                    # draw the bullet for one frame before death
                    screen.blit(bulImg[i], (bulX[i] - (center[2] / 2), bulY[i] - (center[3] / 2)))
                    active[i] = -1
                    # change picture to explosion!!!
                    bulImg[i] = effImg[i]
                    bulExpSound[i].play()
                    break

                # check if the bullet hits an enemy
                elif enemyCheck > -1:
                    # effects on enemy (health loss, death check)
                    enemyHP[enemyCheck] -= bulDmg[i]
                    if enemyHP[enemyCheck] <= 0:
                        enemyActive[enemyCheck] = False
                        enemyX[enemyCheck] = disLength + 25
                        enemyY[enemyCheck] = 75 + 37
                        score += enemyScore[enemyCheck]
                        if enemyIsBoss[enemyCheck]:
                            bossMode = False
                            bossMinSeparation = 10
                        elif not bossMode:
                            bossMinSeparation -= 1

                    # draw the bullet for one frame before death
                    screen.blit(bulImg[i], (bulX[i] - (center[2] / 2), bulY[i] - (center[3] / 2)))
                    active[i] = -1
                    # change picture to explosion!!!
                    bulImg[i] = effImg[i]
                    bulHitSound[i].play()
                    break
                else:
                    bulX[i] += bulTarX[i] * timeSlow[0] / gap
                    bulY[i] += bulTarY[i] * timeSlow[0] / gap
                    # add hitting enemies here
                if j == gap - 1:
                    center = bulImg[i].get_rect()
                    screen.blit(bulImg[i], (bulX[i] - (center[2]/2), bulY[i] - (center[3]/2)))

    # particle effects for bullets
    for i in range(30):
        if -15 <= active[i] < 0:
            screen.blit(bulImg[i], (bulX[i] - 45, bulY[i] - 45))
            active[i] += -1 * timeSlow[0]
        # second frame effect
        if -6.5 <= active[i] < -5.5 and effImg2[i] != "":
            bulImg[i] = effImg2[i]
            active[i] += -1
        elif -6.5 <= active[i] < -5.5:
            active[i] = -16

    # ------------ UI ELEMENTS ------------ #
    # draw walls and stuff
    draw_map(wallCol, wallRandom, wallRandomY)

    # draw bullets on top of walls if they are phased
    if "phase" in bulSpec:
        for i in range(30):
            if bulSpec[i] == "phase" and active[i] > 0:
                center = bulImg[i].get_rect()
                screen.blit(bulImg[i], (bulX[i] - (center[2] / 2), bulY[i] - (center[3] / 2)))
    if "phase" in enemyBulSpec:
        for i in range(30):
            if enemyBulSpec[i] == "phase" and enemyBulActive[i] > 0:
                eCenter = enemyBulImg[i].get_rect()
                screen.blit(enemyBulImg[i], (enemyBulX[i] - (eCenter[2] / 2), enemyBulY[i] - (eCenter[3] / 2)))

    # draw enemy HP bars here so that they go above the stuffs
    for i in range(numEnemy):
        if enemyActive[i]:
            # draw HP bars (red inside then black outline)
            if not enemyIsBoss[i]:
                pygame.draw.rect(screen, UIHp, (enemyX[i] - 25, enemyY[i] - 40, enemyHP[i] / enemyMaxHP[i] * 50, 10))
                pygame.draw.rect(screen, (0, 0, 0), (enemyX[i] - 25, enemyY[i] - 40, 50, 10), 1)
            else:
                pygame.draw.rect(screen, UIHp, (enemyX[i] - 50, enemyY[i] - 50, enemyHP[i] / enemyMaxHP[i] * 100, 14))
                pygame.draw.rect(screen, (0, 0, 0), (enemyX[i] - 50, enemyY[i] - 50, 100, 14), 2)

    # draw crosshair
    dist = math.sqrt((mousePos[0] - posX) ** 2 + (mousePos[1] - posY) ** 2)
    draw_crosshair(mousePos[0], mousePos[1], dist, wpnInAcc[curWpn], curWpn)

    # draw UI for slow and not slowed time
    if timeSlow[0] != 1 or timeSlow[1] != 1:
        screen.fill(UISlow, [0, 0, 100, disHeight])
    else:
        screen.fill(UICol, [0, 0, 100, disHeight])
    pygame.draw.rect(screen, UIBod, [1, 1, 100, disHeight - 2], 3)

    # hp bars and stuff
    if changeAnimation < 0:  # took damage
        screen.fill(UIDmg, (22, 30 + health[0] * 20, 17, -changeAnimation))
        changeAnimation += 1
        pygame.draw.line(screen, [0, 0, 0], (20, 30 + (health[0] // 2) * 40), (40, 30 + (health[0] // 2) * 40))

    create_UI(health[0], mana[0], bossSpawnDelay)
    weapon_UI(parse.wImg[0], wpnAmmo[0], parse.wAmmo[0], 0, curWpn)
    weapon_UI(parse.wImg[1], wpnAmmo[1], parse.wAmmo[1], 1, curWpn)
    weapon_UI(parse.wImg[2], wpnAmmo[2], parse.wAmmo[2], 2, curWpn)

    # play a little animation on taking damage or healing
    if changeAnimation > 0:  # healed
        screen.fill(UIHeal, (22, 30 + health[0] * 20 - changeAnimation, 17, changeAnimation))
        changeAnimation -= 1

    if -2 < changeAnimation < 2:
        changeAnimation = 0

    # score
    score_text = msgFont.render(str(score), False, (25, 150, 25))
    screen.blit(score_text, (disLength - 30 - len(str(score)) * 10, 25))
    # make screen red when dying
    if deathTimer > 0:
        timeSlow = [0.1, 0.1]
        screen.blit(deathImg, (-25, -25))

    # update display!a
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

quit(print("YOU LOST HAHA"))
# :D

