from pygame import *

init()
myClock = time.Clock()
consolasFont = font.SysFont("consolas", 40)

width, height = 1280, 720
screen = display.set_mode((width, height))
display.set_caption("TUYU's Bizarre Adventure")
icon = image.load("images/tuyulogo.jpg")
display.set_icon(icon)

RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

DARKTUYU = (23, 23, 41)
MIDTUYU = (80, 81, 124)
LIGHTTUYU = (206, 74, 125)
BLOODTUYU = (170, 48, 37)
SLAVETUYU = (32, 59, 50)
LEANCOL = (175, 73, 231)

running = True
status = "menu"

# images
tuyumenu = transform.smoothscale(image.load("images/tuyustart.jpg"), (800, 720))
tuyuknife = image.load("images/tuyuknife.jpg")
tuyudemon = image.load("images/tuyudemon.jpg")
tuyuslave = image.load("images/tuyuslave.jpg")

backText = image.load("images/Back.png")
instructionsText = image.load("images/Instructions.png")

# menu
menuRects = [Rect(865, 130*i+200, 350, 80) for i in range(4)] # Buttons in the menu.
menuText = ["PLAY", "INSTRUCTIONS", "SOMETHING", "QUIT"]
backRect = Rect(10, height-60, 100, 50)
textPos = [(i[0]+20, i[1]+23) for i in menuRects]

levelRects = [Rect(300*i+240, 190*i+70, 200, 200) for i in range(3)]
stage = 0

def menu():
    screen.fill(MIDTUYU)
    screen.blit(tuyumenu, (0, 0))
    [draw.rect(screen, DARKTUYU, i) for i in menuRects]
    [draw.rect(screen, DARKTUYU, i, 5) for i in menuRects]
    [screen.blit(consolasFont.render(i, True, WHITE),(j)) for i, j in zip(menuText, textPos)]

    display.flip()

def levels():
    screen.fill((MIDTUYU))
    draw.rect(screen, BLOODTUYU, (427, 0, 427, height))
    draw.rect(screen, SLAVETUYU, (854, 0, 427, height))
    [draw.rect(screen, DARKTUYU, i) for i in levelRects]
    screen.blit(tuyuknife, (220, 50))
    screen.blit(tuyudemon, (520, 240))
    screen.blit(tuyuslave, (820, 430))
    for i in range(1, 4):
        screen.blit(transform.scale(image.load(f"images/Level{i}.png"), (214, 48)), (i*301-75, i*190+90))
    # draw.line(screen, WHITE, (width/2, 0), (width/2, height), 5)
    # draw.line(screen, WHITE, (0, height/2), (width, height/2), 5)
    back(backRect)
    display.flip()


def back(backRect):
    global status
    if status in ["levels", "instructions"]:
        draw.rect(screen, DARKTUYU, backRect)
        screen.blit(backText, (29, height-45))
    if mb[0]:
        if backRect.collidepoint(mx, my):
            status = "menu"

def instructions():
    screen.fill(MIDTUYU)
    screen.blit(instructionsText, (50, 50))
    back(backRect)
    display.flip()

'''Gameplay'''
stage = 1

 # left top width height
playerRect = Rect(55, 325, 10, 50) # Player

platforms = [
    0,
    [Rect(200, 400, 25, 25), Rect(750, 325, 175, 25), Rect(900, 200, 100, 25), Rect(200, 300, 25, 25), Rect(20, 200, 75 , 25), Rect(1050, 150, 100, 25)],
    [Rect(100, 200, 400, 20)]
    ]
walls = [
    0,
    [Rect(0, 500, 640, 100), Rect(-1, 0, 1, height), Rect(width/2, 400, 50, 270), Rect(125, 250, 50, 100), Rect(120, 70, 100, 20), Rect(200, 0, 20, 70), Rect(1230, 150, 50, 315)],
    [Rect(0, 600, 1280, 100)]
    ]
lean_rects = [
    Rect(0, 0, 0, 0), 
    [Rect(0, height-10, width, 10)],
    ]
collectibles = [
    Rect(170, 50, 10, 10)
    ]
final_door = [
    0,
    0,
    0,
]

collectible_count = 0

X = 0
Y = 1
W = 2
H = 3
GROUND = height
gravity = 2
walkSpeed = 5
jump = -25
BOTTOM = 2
v = [0, 0, GROUND]

def stages(playerRect):
    global stage

    if playerRect[0] == width:
        playerRect[X] = 0
        stage += 1
        playerRect[Y] = walls[stage][0].y - playerRect.height
    
    if playerRect[0] < 0 and stage != 1:
        playerRect[X] = width - playerRect[W]
        stage -= 1
        playerRect[Y] = walls[stage][-1].y - playerRect.height

def drawScene():
    screen.fill(MIDTUYU)
    drawPlayer()
    drawCollectibles(collectibles)
    # lean(lean_rects)

    [draw.rect(screen, DARKTUYU, i) for i in walls[stage]]
    [draw.rect(screen, LIGHTTUYU, i) for i in platforms[stage]]

    display.flip()

def drawCollectibles(collectibles):
    global collectible_count
    [draw.rect(screen, YELLOW, j) for j in collectibles]
    for i in range(len(collectibles)):
        if playerRect.collidepoint(collectibles[i].x, collectibles[i].y):
            collectibles.pop(i)
            collectible_count += 1
        
# def lean(lean_rects):
#     [draw.rect(screen, LEANCOL, i) for i in lean_rects[stage] if stage == 1]
#     for i in range (len(lean_rects)):
#         if playerRect.collidepoint(lean_rects[stage][i].x, lean_rects[stage][i].y):
#             playerRect.x = 55
#             playerRect.y = 325

def drawPlayer():
    draw.rect(screen, (231, 220, 216), playerRect)  

def movePlayer(playerRect):
    v[X] = 0

    if (keys[K_w] and
        playerRect[Y] + playerRect[H] == v[BOTTOM] and
        v[Y] == 0 and 
        wallCollision(playerRect[X], playerRect[Y] - playerRect.height, walls) == -1):
        v[Y] = jump
    
    if keys[K_d] and wallCollision(playerRect[X] + playerRect.width/2, playerRect[Y], walls) == -1:
        v[X] = walkSpeed

    if keys[K_a] and wallCollision(playerRect[X] - playerRect.width/2, playerRect[Y], walls) == -1:
        v[X] = -walkSpeed
    
    v[Y] += gravity 
    playerRect[X] += v[X]
    
def collision(playerRect, platforms):
    for i in platforms[stage]: # Platforms that can be jumped down from.
        if (playerRect[X] + playerRect[W] > i[X] and 
            playerRect[X] < i[X] + i[W] and
            playerRect[Y] + playerRect[H] <= i[Y] and
            playerRect[Y] + playerRect[H] + v[Y] >= i[Y] and not
            keys[K_s]):
            v[BOTTOM] = i[Y]
            v[Y] = 0
            playerRect[Y] = v[BOTTOM]-playerRect[H]
    
    for i in walls[stage]:
        if (playerRect[X] + playerRect[W] > i[X] and 
            playerRect[X] < i[X] + i[W] and
            playerRect[Y] + playerRect[H] <= i[Y] and
            playerRect[Y] + playerRect[H] + v[Y] >= i[Y]):
            v[BOTTOM] = i[Y]
            v[Y] = 0
            playerRect[Y] = v[BOTTOM]-playerRect[H] 

    playerRect [Y] += v[Y]
    
    if playerRect[Y] + playerRect[H] >= GROUND:
        v[2] = GROUND
        v[Y] = 0
        playerRect[Y] = GROUND-playerRect[H]

def wallCollision(playerX, playerY, walls):
    playerRect = Rect(playerX, playerY, 10, 50)
    return playerRect.collidelist(walls[stage])

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    
    keys = key.get_pressed()
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    if status == "menu":
        menu()
    elif status == "instructions":
        instructions()
    elif status == "levels":
        levels()
    elif status == "play":
        stages(playerRect)
        movePlayer(playerRect)
        collision(playerRect, platforms)
        drawScene()
        myClock.tick(60) 

    if mb[0]:
        if status == "menu":
            if menuRects[0].collidepoint(mx, my):
                status = "levels"
            elif menuRects[1].collidepoint(mx, my):
                status = "instructions"
            elif menuRects[3].collidepoint(mx, my):
                running = False   
        
        if status == "levels":
            if levelRects[0].collidepoint(mx, my):
                status = "play"
            
quit()
