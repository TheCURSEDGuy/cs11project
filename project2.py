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
menuText = ["PLAY", "LEVELS", "SOMETHING", "QUIT"]
textPos = [(i[0]+20, i[1]+20) for i in menuRects]
stage = 0

def menu():
    screen.fill((147,112,219))
    screen.blit(transform.smoothscale(image.load("images/WHATR.jpg"),(800,720)),(0,0))
    [draw.rect(screen,WHITE,i) for i in menuRects]
    [draw.rect(screen,BLACK,i,5) for i in menuRects]
    [screen.blit(comicFont.render(i, True, BLACK),(j)) for i,j in zip(menuText,textPos)]

    display.flip()

# gameplay

stage = 1

                # left top width height
playerRect = Rect(55, 325, 10, 50) # player

plats = [Rect(100, 400, 200, 50)] # platforms
platsMain = [Rect(0, 500, 1280, 100)] # platforms that don't allow you to "jump down" from

X = 0
Y = 1
W = 2
H = 3

GROUND = height
BOTTOM = 2

gravity = 2
walkSpeed = 5
jump = -35

v = [0, 0, GROUND]

def stages():
    if playerRect[0] > width:
        print("e")


def drawScene():
    screen.fill(WHITE)
    drawPlayer()
    [draw.rect(screen, BLACK, i) for i in plats]
    display.flip()

def drawPlayer():
    draw.rect(screen, RED, playerRect)  

def movePlayer(playerRect):
    if keys[K_UP] and playerRect[Y] + playerRect[H]== v[BOTTOM] and v[Y] == 0:
        v[Y] = jump
    
    v[X] = 0

    if keys[K_RIGHT]:
        v[X] = walkSpeed

    if keys[K_LEFT]:
        v[X] = -walkSpeed
    
    v[Y] += gravity 

    playerRect[X] += v[X]
    
def collision(playerRect, plats):
    for i in plats:
        if playerRect[X]+ playerRect[W] > i[X] and playerRect[X] < i[X] + i[W] and playerRect[Y]+ playerRect[H] <= i[Y] and playerRect[Y] + playerRect[H]+ v[Y] >=i[Y] and not keys[K_DOWN]:
            v[BOTTOM]= i[Y]
            v[Y] = 0
            playerRect[Y]=v[2]-playerRect[H]

    playerRect [Y] += v[Y]
    
    if playerRect[Y] + playerRect[H] >= GROUND:
        v[2] = GROUND
        v[Y] = 0
        playerRect[Y] = GROUND - playerRect[H]

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    
    keys = key.get_pressed()
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    if status == "menu":
        menu()
    elif status == "play":
        movePlayer(playerRect)
        collision(playerRect, plats)
        drawScene()
        stages()
        
        myClock.tick(60) 

    if mb[0]:
        if menuRects[0].collidepoint(mx, my):
            status = "play"
            
quit()