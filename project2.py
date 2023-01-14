from pygame import *

font.init()
myClock = time.Clock()
comicFont = font.SysFont("Comic Sans MS", 25)

width, height = 1280, 720
screen = display.set_mode((width, height))

RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

running = True
status = "menu"

# menu
menuRects = [Rect(865, 130*i+200, 350, 80) for i in range(4)] # Rectangular buttons in the menu
menuText = ["PLAY", "INSTRUCTIONS", "SOMETHING", "QUIT"]
textPos = [(i[0]+20, i[1]+20) for i in menuRects]
stage = 0

def menu():
    screen.fill((147, 112, 219))
    screen.blit(transform.smoothscale(image.load("images/WHATR.jpg"), (800, 720)), (0, 0))
    [draw.rect(screen, WHITE, i) for i in menuRects]
    [draw.rect(screen, BLACK, i, 5) for i in menuRects]
    [screen.blit(comicFont.render(i, True, BLACK),(j)) for i,j in zip(menuText, textPos)]

    display.flip()

# instructions 

def instructions():
    print("placeholder")

# gameplay
stage = 1

 # left top width height
playerRect = Rect(55, 325, 10, 50) # Player

platforms = [0, [Rect(100, 400, 200, 50), Rect(750, 325, 200, 50), Rect(600, 200, 200, 50)], [Rect(100, 200, 400, 20)]]
platformsMain = [0, [Rect(0, 500, 1280, 100)], [Rect(0, 600, 1280, 100)]] # Platforms that don't allow you to "jump down".
walls = [0, [Rect(-1, 0, 1, height), Rect(width/2, 400, 50, 300), Rect(1230, 150, 50, 320)], []]

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
        playerRect[Y] = platformsMain[stage][0].y - playerRect.height
    
    if playerRect[0] < 0 and stage != 1:
        playerRect[X] = width - playerRect[W]
        stage -= 1
        playerRect[Y] = platformsMain[stage][0].y - playerRect.height
        print(playerRect)
        print(platformsMain[stage][0].y)

def drawScene():
    screen.fill(WHITE)
    drawPlayer()

    [draw.rect(screen, BLUE, i) for i in platforms[stage]]
    [draw.rect(screen, BLACK, i) for i in platformsMain[stage]]
    [draw.rect(screen, BLACK, i) for i in walls[stage]]
    display.flip()

def drawPlayer():
    draw.rect(screen, RED, playerRect)  

def movePlayer(playerRect):
    v[X] = 0

    if keys[K_w] and playerRect[Y] + playerRect[H] == v[BOTTOM] and v[Y] == 0:
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
            playerRect[Y] = v[2]-playerRect[H]

    for i in platformsMain[stage]: # Platforms that cannot be jumped down from.
        if (playerRect[X] + playerRect[W] > i[X] and
            playerRect[X] < i[X] + i[W] and
            playerRect[Y] + playerRect[H] <= i[Y] and
            playerRect[Y] + playerRect[H] + v[Y] >= i[Y]):
            v[BOTTOM] = i[Y]
            v[Y] = 0
            playerRect[Y] = v[2]-playerRect[H]
    
    for i in walls[stage]:
        if (playerRect[X] + playerRect[W] > i[X] and 
            playerRect[X] < i[X] + i[W] and
            playerRect[Y] + playerRect[H] <= i[Y] and
            playerRect[Y] + playerRect[H] + v[Y] >= i[Y]):
            v[BOTTOM] = i[Y]
            v[Y] = 0
            playerRect[Y] = v[2]-playerRect[H]

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
    elif status == "levels":
        instructions()
    elif status == "play":
        stages(playerRect)
        movePlayer(playerRect)
        collision(playerRect, platforms)
        drawScene()
        myClock.tick(60) 

    if mb[0] and status == "menu":
        if menuRects[0].collidepoint(mx, my):
            status = "play"
        if menuRects[1].collidepoint(mx, my):
            status = "levels"
        if menuRects[3].collidepoint(mx, my):
            running = False
            
quit()