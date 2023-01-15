from pygame import *

init()
font.init()
myClock = time.Clock()
timesFont = font.SysFont("Times New Roman", 25)

width, height = 1280, 720
screen = display.set_mode((width, height))

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

running = True
status = "menu"

# menu
menuRects = [Rect(865, 130*i+200, 350, 80) for i in range(4)] # Buttons in the menu.
menuText = ["PLAY", "INSTRUCTIONS", "SOMETHING", "QUIT"]
textPos = [(i[0]+20, i[1]+20) for i in menuRects]

instRects = [Rect(300*i+240, 190*i+70, 200, 200) for i in range(3)]
stage = 0

def menu():
    screen.fill(MIDTUYU)
    screen.blit(transform.smoothscale(image.load("images/WHATR.jpg"), (800, 720)), (0, 0))
    [draw.rect(screen, WHITE, i) for i in menuRects]
    [draw.rect(screen, BLACK, i, 5) for i in menuRects]
    [screen.blit(timesFont.render(i, True, BLACK),(j)) for i,j in zip(menuText, textPos)]

    display.flip()

def levels():
    # global status # TEMPORARY
    screen.fill((MIDTUYU))
    [draw.rect(screen, DARKTUYU, i) for i in instRects]
    screen.blit(transform.smoothscale(image.load("images/tuyuknife.jpg"), (200, 200)), (220, 50))
    for i in range(1, 4):
        screen.blit(transform.smoothscale(image.load(f"images/Level{i}.png"), (214, 48)), (i*301-65, i*190+90))
    # draw.line(screen, WHITE, (width/2, 0), (width/2, height), 5)
    # draw.line(screen, WHITE, (0, height/2), (width, height/2), 5)
    display.flip()
    # status = "play" # NEEDS TO BE UPDATED TO A BUTTON
# instructions 

def instructions():
    print("placeholder")

# gameplay
stage = 1

 # left top width height
playerRect = Rect(55, 325, 10, 50) # Player

platforms = [0, [Rect(100, 400, 200, 25), Rect(750, 325, 200, 25), Rect(700, 200, 100, 25)], [Rect(100, 200, 400, 20)]]
walls = [0, [Rect(0, 500, 640, 100), Rect(-1, 0, 1, height), Rect(width/2, 400, 50, 270), Rect(1230, 150, 50, 315), Rect(0, width-playerRect.width, 0, 1)], [Rect(0, 600, 1280, 100)]]

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

    [draw.rect(screen, LIGHTTUYU, i) for i in platforms[stage]]
    [draw.rect(screen, DARKTUYU, i) for i in walls[stage]]
    display.flip()

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

    if mb[0] and status == "menu":
        if menuRects[0].collidepoint(mx, my):
            status = "levels"
        if menuRects[1].collidepoint(mx, my):
            status = "instructions"
        if menuRects[3].collidepoint(mx, my):
            running = False   
            
quit()
