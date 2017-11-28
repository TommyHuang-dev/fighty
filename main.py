import parse
import pygame
import math
import sys
import random
import time

class Enemy:
    def __init__(self):
        pass


# appends the folder/name.png thingy to the file, instead of 1just name
def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


# some stackoverflow bs ¯\_(ツ)_/¯
def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


def draw_crosshair(cX, cY, dis, inAcc):
    # more spacing = more inaccurate
    spacing = (dis / 55) * inAcc + 3
    # right, left, up, down
    pygame.draw.line(screen, (0, 0,0), (cX + spacing, cY), (cX + spacing + 3, cY))
    pygame.draw.line(screen, (0, 0, 0), (cX - spacing, cY), (cX - spacing - 3, cY))

    pygame.draw.line(screen, (0, 0, 0), (cX, cY - spacing), (cX, cY - spacing - 3))
    pygame.draw.line(screen, (0, 0, 0), (cX, cY + spacing), (cX, cY + spacing + 3))


# this calculates angles and shit for the bullets
def calc_bullet(bX, bY, acc):
    global curBul, bulTarX, bulTarY, bulProj, bulAng
    bulAng[curBul] = (math.atan2(-(bulTarY[curBul] - bY), bulTarX[curBul] - bX))
    if acc > 0:
        randomAng = math.radians(random.uniform(-acc, acc))  # add some randomness to the bullets
        bulAng[curBul] = bulAng[curBul] + randomAng

    bulTarY[curBul] = - math.sin(bulAng[curBul]) * bulProj[curBul]
    bulTarX[curBul] = math.cos(bulAng[curBul]) * bulProj[curBul]


# this creates the health bar and mana bar
def create_UI(hp, mp):
    screen.fill(UIHp, (20, 30, 20, hp * 20))
    pygame.draw.rect(screen, [0, 0, 0], [20, 30, 20, 200], 2)
    pygame.draw.line(screen, [0, 0, 0],     [20, 130], [40, 130], 3)
    for i in range(10):
        pygame.draw.line(screen, [0, 0, 0], [20, 30 + 20 * i], [40, 30 + 20 * i])

    screen.fill(UIMana, (60, 30, 20, int(mp * 2)))
    pygame.draw.rect(screen, [0, 0, 0], [60, 30, 20, 200], 2)


# This function creates the little weapon sprites for switching weapons / displaying ammo
def weapon_UI(img, ammo, max_ammo, num, selected):  # num = weapon from 0 - 2 (top to bottom)
    global relCD
    screen.blit(img, (12, 250 + num * 120))
    if selected == num:
        pygame.draw.rect(screen, (0, 0, 0), (8, 250 + num * 120, 84, 70), 1)

    # ammo display
    ammo_words = str(ammo) + " / " + str(max_ammo)
    if relCD[num] > 0:
        ammo_words = "REL " + str(round(relCD[num] / 60, 1))
    elif ammo <= -1:
        ammo_words = "INF"
    ammo_text = ammoFont.render(ammo_words , False, (0, 0, 0))
    screen.blit(ammo_text, (50 - len(ammo_words) * 4.5, 330 + num * 120))


# This moves the player in the 4 cardinal directions + diagonally
def move_player(buttons, pSpd):
    global posX, posY
    num = [0, 0]

    # redoing dis shit, num[0] = x movement, num[1] = y movement
    if buttons[pygame.K_w]:
        if not wall_collision(posX, posY - pSpd, 15):
            num[0] = - pSpd
    elif buttons[pygame.K_s]:
        if not wall_collision(posX, posY + pSpd, 15):
            num[0] = pSpd
    if buttons[pygame.K_d]:
        if not wall_collision(posX + pSpd, posY, 15):
            num[1] = pSpd
    elif buttons[pygame.K_a]:
        if not wall_collision(posX - pSpd, posY, 15):
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
        if wallRandom[i] + hitbox + 37 > x > wallRandom[i] - hitbox - 38 and \
                            wallRandomY[i] + hitbox + 37 > y > wallRandomY[i] - hitbox - 38:
            return True
    return False


def spawn_enemy():
    pass


def move_enemy():
    pass


def draw_map(wall_col, rand, randY):
    pygame.draw.rect(screen, wall_col, (102, 2, 896, 596), 5)
    for i in range(len(rand)):
        screen.fill(wall_col, rect = (rand[i] - 37, randY[i] - 37, 75, 75))


def main_menu():
    pass


'''
|= = = = = = = = = = = = = = = = MAIN CODE STARTS NOW = = = = = = = = = = = = = = = = =|

TODO LIST:
    - add enemies
        - pathfinding and map generation in 75x75 grid
        pathfinding ideas:
        check which quadrant the player is in
        If low hp or need backup, find cover and run away, otherwise, advance.
        Add randomness so that enemies split up and sometimes surround the player.d
    - add barriers DONE (mostly)
    - add better visuals on hit for bullets (maybe 2 or 3 frames of effects instead of 1 pic)
    - add knife/ LIGHT SABRE (deflects bullets!)
    - multiple levels?!
    - sound effects

BUGS: ¯\_(ツ)_/¯
    - no bugs obviously all features
    - hitboxes sometimes derpy

'''

# initiate pygame and cursors
pygame.mixer.pre_init(22050, -16, 6, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
time.sleep(1)

cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
pygame.mouse.set_cursor(*pygame.cursors.diamond)


# setup the screen and main clock
disLength = 1000
disHeight = 600
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("shooty")
clock = pygame.time.Clock()

ammoFont = pygame.font.SysFont('Courier New', 15)

# background and objects like walls
backCol = [240, 240, 240]
UIBod = [125, 125, 225]
UICol = [220, 240, 240]
UISlow = [190, 200, 220]
UIHp = [250, 70, 70]
UIMana = [100, 100, 240]
wallCol = [120, 120, 120]

wallRandom = []
wallRandomY = []
wallCount = 0  # number of walls in total, should not exceed 8
wallCountC = 0  # number of walls in a single column, should not exceed 3
ran = 0
wallGrid = []
for i in range(12):  # x axis
    wallGrid.append([])
    wallCountC = 0
    for k in range(8):  # y axis
        # better walls[tm]
        if random.randint(0, 60) + ran >= 56 and 1 <= i <= 9 and wallCountC < 3 and wallCount < 9:
            wallGrid[i].append(True)
            wallCountC += 1
            wallCount += 1
            ran = 5
            wallRandom.append(125 + i * 75 + 37) # center of the wall X and Y
            wallRandomY.append(k * 75 + 37)
        else:
            wallGrid[i].append(False)
            ran = 0

# global game variables
level = 0
timescale = 1.0
timeBuffer = [0, 20]  # used so that pressing space doesn't accidentally do it 2 times
timeSlow = [1.0, 1.0]  # self slow, enemy slow

# player variables
playerImg = pygame.image.load("player.png").convert_alpha()
posX = 150.0  # start in the top left corner
posY = 50.0
speed = 5.0
health = [10, 10]  # min/max hp
mana = [100, 100]
manaCharge = [0, 30]
fireCD = 0.0  # used when shooting
wpnAmmo = [parse.wAmmo[0], parse.wAmmo[1]]
wpnInAcc = [parse.wAcc[0], parse.wAcc[1]]
relCD = [0, 0]  # used by weapon 1 and weapon 2 when reloading.
curWpn = 0
atkSound = pygame.mixer.Sound(parse.wSound[curWpn])

# player bullet variables
bulImg = []  # should probably add different pictures
effImg = []
effImg2 = []
bulX = []
bulY = []
active = []
bulDmg = []
bulProj = []
bulTarX = []
bulTarY = []
bulAng = []
bulExpSound = []
curBul = 0

# effect pictures and stuff
expSmall = pygame.image.load("effects/exp_small.png").convert_alpha()

# bullet array :D
for i in range(12):
    bulImg.append(parse.wBul)
    effImg.append(expSmall)
    effImg2.append("")
    bulX.append(-50.0)  # top left corner for inactive bullets
    bulY.append(-50.0)
    active.append(0)
    bulDmg.append(0)
    bulProj.append(0.0)
    bulTarX.append(-50.0)
    bulTarY.append(-50.0)
    bulAng.append(0.0)
    bulExpSound.append(parse.wExpSound[curWpn])

#2nd frame of effects (optional)
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

# load sounds
pygame.mixer.set_num_channels(8)
#asdf

# ========= GAME LOGIC =========
while True:
    screen.fill(backCol)

    # lose inaccuracy from recoil
    for i in range(2):
        if wpnInAcc[i] > parse.wAcc[i]:
            wpnInAcc[i] = wpnInAcc[i] - timeSlow[0] * ((wpnInAcc[i] - parse.wAcc[i]) * 0.03) - 0.01
        else:
            wpnInAcc[i] = parse.wAcc[i]

    # tick down timers, recharge mana
    for i in range(2):
        relCD[i] += -1 * timeSlow[0]
        if -1 <relCD[i] <= 0:
            wpnAmmo[i] = parse.wAmmo[i]
            relCD[i] += -1

    timeBuffer[0] += -1
    fireCD += -1 * timeSlow[0]
    if timeSlow[0] != 1:
        mana[0] += -0.25
    else:
        manaCharge[0] += -1
        if manaCharge[0] <= 0 and mana[0] < mana[1]:
            mana[0] += 0.25
    if mana[0] <= 0:
        timeSlow[0] = 1.0
        timeSlow[1] = 1.0

    # ------------ PLAYER STUFF ------------ #
    pressed = pygame.key.get_pressed()

    # SLOW DOWN TIME...
    if timeBuffer[0] <= 0 and pressed[pygame.K_SPACE]:
        timeBuffer[0] = timeBuffer[1]
        if timeSlow[0] != 1 or timeSlow[1] != 1:
            timeSlow = [1.0, 1.0]
        else:
            timeSlow = [0.5, 0.25]
            manaCharge[0] = 30

    # move player and display player
    move_player(pressed, speed * timeSlow[0])
    screen.blit(playerImg, (posX - 25, posY - 25))

    # switch weapon (knife, wpn 0, wpn 1)
    if pressed[pygame.K_1]:  # knife later
        curWpn = 0
        atkSound = pygame.mixer.Sound(parse.wSound[curWpn])
        if fireCD <= 30:
            fireCD = 30

    elif pressed[pygame.K_2]:
        curWpn = 1
        atkSound = pygame.mixer.Sound(parse.wSound[curWpn])
        if fireCD <= 30:
            fireCD = 30

    elif pressed[pygame.K_3]:
        curWpn = 2
        atkSound = pygame.mixer.Sound(parse.wSound[curWpn])
        if fireCD <= 30:
            fireCD = 30

    # ------------ SHOOTING AND BULLET STUFF ------------ #
    # shooting
    mousePos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1 and fireCD <= 0 and relCD[curWpn] <= 0:
        curBul += 1
        if curBul >= 12:
            curBul = 0
        bulX[curBul] = posX
        bulY[curBul] = posY
        active[curBul] = 1
        bulTarX[curBul] = mousePos[0]
        bulTarY[curBul] = mousePos[1]
        bulDmg[curBul] = parse.wDmg[curWpn]
        bulProj[curBul] = parse.wProj[curWpn]
        # TRIG YAY
        calc_bullet(bulX[curBul], bulY[curBul], wpnInAcc[curWpn])
        bulImg[curBul] = rot_center(parse.wBul[curWpn], math.degrees(bulAng[curBul]))
        effImg[curBul] = parse.wEff[curWpn]
        effImg2[curBul] = parse.wEff2[curWpn]
        # recoil!
        wpnInAcc[curWpn] += parse.wCoil[curWpn]
        # sounds
        atkSound.play()
        bulExpSound[curBul] = pygame.mixer.Sound(parse.wExpSound[curWpn])

        # set cooldown and automatic reload
        fireCD = 60 / parse.wRate[curWpn]
        wpnAmmo[curWpn] += -1
        if wpnAmmo[curWpn] == 0 or pressed[pygame.K_r]:
            relCD[curWpn] = parse.wRel[curWpn] * 60  # RELOAD HERE

    # manual reload
    if pressed[pygame.K_r] and wpnAmmo[curWpn] < parse.wAmmo[curWpn]:
        relCD[curWpn] = parse.wRel[curWpn] * 60

    # displaying and resetting bullets
    for i in range(12):
        if active[i] > 0:
            # check if the bullet hits a wall, else display it
            gap = int(math.sqrt(bulTarX[i] ** 2 + bulTarY[i]** 2)) // 15 + 1  # number of times to check for collision
            for j in range(gap):
                if wall_collision(bulX[i], bulY[i], 2) or bulX[i] + 15 > disLength or bulX[i] < 105 or bulY[i] + 15 > disHeight or bulY[i] < 5:
                    active[i] = -1
                    bulImg[i] = effImg[i]
                    bulExpSound[i].play()
                    break
                else:
                    bulX[i] += bulTarX[i] * timeSlow[0] / gap
                    bulY[i] += bulTarY[i] * timeSlow[0] / gap
                    # add hitting enemies here
                if j == gap - 1:
                    screen.blit(bulImg[i], (bulX[i] - 15, bulY[i] - 15))

    # ------------ ENEMY STUFF ------------ #
    # LITERALLY NOTHING

    # ------------ UI ELEMENTS ------------ #
    # draw walls and stuff
    draw_map(wallCol, wallRandom, wallRandomY)

    # particle effects for bullets
    for i in range(12):
        if -15 <= active[i] < 0:
            screen.blit(bulImg[i], (bulX[i] - 45, bulY[i] - 45))
            active[i] += -1 * timeSlow[0]
        # second frame effect
        if -6.5 <= active[i] < -5.5 and effImg2[i] != "":
            bulImg[i] = effImg2[i]
            active[i] += -1
        elif -6.5 <= active[i] < -5.5:
            active[i] = -16

    # draw crosshair
    if wpnInAcc[curWpn] > 0:
        dist = math.sqrt((mousePos[0] - posX) ** 2 + (mousePos[1] - posY) ** 2)
        draw_crosshair(mousePos[0], mousePos[1], dist, wpnInAcc[curWpn])

    # draw UI for slow and not slowed time
    if timeSlow[0] != 1 or timeSlow[1] != 1:
        screen.fill(UISlow, [0, 0, 100, disHeight])
    else:
        screen.fill(UICol, [0, 0, 100, disHeight])
    pygame.draw.rect(screen, UIBod, [1, 1, 100, disHeight - 2], 3)

    # hp bars and stuff
    create_UI(health[0], mana[0])
    weapon_UI(parse.wImg[0], wpnAmmo[0], parse.wAmmo[0], 0, curWpn)
    weapon_UI(parse.wImg[1], wpnAmmo[1], parse.wAmmo[1], 1, curWpn)

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
