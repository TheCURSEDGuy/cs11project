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
textPos = [(i[0]+20,i[1]+20) for i in menuRects]
stage = 0

def menu():
    screen.fill((147,112,219))
    screen.blit(transform.smoothscale(image.load("images/WHATR.jpg"),(800,720)),(0,0))
    [draw.rect(screen,WHITE,i) for i in menuRects]
    [draw.rect(screen,BLACK,i,5) for i in menuRects]
    [screen.blit(comicFont.render(i,False,BLACK),(j)) for i,j in zip(menuText,textPos)]

    display.flip()


# gameplay
playerPos = [55, 325]
playerRect = Rect(playerPos[0], playerPos[1], 10, 50)

plats = [Rect(0, 500, 1280, 100), Rect(100, 400, 200, 50)]

gravity = 2
v = [0,0]

def drawScene():
    screen.fill(WHITE)
    drawPlayer()
    [draw.rect(screen,BLACK,i) for i in plats]
    display.flip()

def drawPlayer():
    draw.rect(screen, RED, playerRect)

def movePlayer():
    global playerRect
    v[0] = 0
    if keys[K_UP] and playerRect.collidelistall(plats):
        v[1] =  -25
        print(playerRect)
        print("up")
    if keys[K_DOWN]:
        print("placeholder")
    if keys[K_RIGHT]:
        v[0] = 2
    if keys[K_LEFT]:
        v[0] = -2

    playerRect[0] += v[0]
    playerRect[1] += v[1]
    
def collision():
    global v, playerRect
    # for i in plats:
        # if playerRect.colliderect((i[0], i[1], i[2], 1)):
        #     if v[1] > 0:
        #         playerRect[1] = i[1] - 50
        #         v[1] = 0

    if playerRect.collidelistall(plats):
        v[1] = 0
    else:
        v[1] += gravity


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
        movePlayer()
        drawScene()
        collision()
        myClock.tick(60) 

    if mb[0]:
        if menuRects[0].collidepoint(mx, my):
            status = "play"
            
quit()
