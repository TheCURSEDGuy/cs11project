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
mixer.music.load("audio/otherworld.ogg")
mixer.music.play()

running = True
status = "menu"
t = 0

# images
tuyumenu = transform.smoothscale(image.load("images/tuyustart.jpg"), (800, 720))
tuyuknife = image.load("images/tuyuknife.jpg")
tuyudemon = image.load("images/tuyudemon.jpg")
tuyuslave = image.load("images/tuyuslave.jpg")
knifePic = transform.smoothscale(image.load("images/knife.png"), (40,10))
buschanW = transform.smoothscale(image.load("images/buschan1.png"),(30,50))
buschanI = image.load("images/buschan0.png")
ladder = transform.smoothscale(image.load("images/ladder.png"), (20,40))

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

knife = []

 # left top width height
playerRect = Rect(55, 325, 10, 50) # Player

platforms = [
    [None],
    [Rect(200, 400, 25, 25), Rect(750, 325, 175, 25), Rect(900, 200, 100, 25), Rect(200, 300, 25, 25), Rect(20, 200, 75 , 25), Rect(1050, 150, 100, 25)],
    []
    ]
ladders = [
    Rect(0,0,0,0),Rect(0,0,0,0),Rect(380,100,20,40*13)
    ]
walls = [
    [None],
    [Rect(0, 500, 640, 100), Rect(-1, 0, 1, height), Rect(width/2, 400, 50, 270), Rect(125, 250, 50, 100), Rect(120, 70, 100, 20), Rect(200, 0, 20, 70), Rect(0, -1, width/2, 1), Rect(1230, 150, 50, 315)],
    [Rect(0, 600, 1280, 100),Rect(400,200,1280-400,1000)]
    ]
lean_rects = [
    [0], 
    [Rect(0, height-10, width, 10)],
    [Rect(0,100,100,100)],
    ]
collectibles = [
    Rect(0,0,0,0),
    Rect(170, 50, 10, 10),
    Rect(300, 200, 10, 10)
    ]
door = [
    0,
    [Rect(140, 0, 20, 70)],
    [Rect(0, 0, 0, 0)]
]

collectible_count = 0
doors = [
    0,
    [Rect(140, 0, 20, 70)],
    [Rect(0, 0, 0, 0)]
]

puzzle_buttons = [Rect(380, 100, 200, 200), Rect(700, 100, 200, 200), Rect(380, 450, 200, 200), Rect(700, 450, 200, 200)]
puzzle_pattern = [1, 4, 3, 2]
user_pattern = []
button_clicked = [False, False, False, False]

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
    global status
    screen.fill(MIDTUYU)
    drawPlayer()
    drawEnemy()
    drawCollectibles(collectibles)
    lean(lean_rects)
    
    [screen.blit(ladder,(380,100+i*40)) for i in range(int(ladders[stage][H]/40))]
    [draw.rect(screen, DARKTUYU, i) for i in walls[stage]]
    [draw.rect(screen, LIGHTTUYU, i) for i in platforms[stage]]
    [draw.rect(screen, LEANCOL, i) for i in lean_rects[stage]]
    [draw.rect(screen, BLACK, i) for i in doors[stage] if doors != 0] # NOT WORKING

    if playerRect.collidelistall(doors[stage]):
        status = "puzzle"
        puzzle()
        doors.pop()
    
    for i in knife:
        if not (i[0].collidelistall(platforms[stage]) or i[0].collidelistall(walls[stage])):
            if i[1]:
                i[0][X] += 10
            else:
                i[0][X] -= 10
        
            knives(i)

    display.flip()

def drawCollectibles(collectibles):
    global collectible_count
    if collectibles[stage] != 0: 
        draw.rect(screen,YELLOW,collectibles[stage]) 
        if playerRect.colliderect(collectibles[stage]):
            collectibles[collectibles.index(collectibles[stage])] = 0
            collectible_count += 1
    # [draw.rect(screen, YELLOW, i) for i in collectibles]
    # for i in range(len(collectibles)):
    #     if playerRect.collidepoint(collectibles[i].x, collectibles[i].y):
    #         collectibles.pop(i)
    #         collectible_count += 1

def drawEnemy():
    for i in enemy[stage]:

        if i[0].colliderect(playerRect):
            playerRect.x = 55
            playerRect.y = 325

        for j in knife:
            if i[0].colliderect(j[0]):
                enemy[stage].pop(enemy[stage].index(i))


        if i[0][X] + i[0][W] >= width:
            i[1] = False

        elif i[0][X] <= i[2]:
            i[1] = True
            
        if i[1]:
            i[0][X] += 1
        
        else:
            i[0][X] -=1


        draw.rect(screen,RED,i[0])
        
def lean(lean_rects):
    for i in range (len(lean_rects[stage])):
        if playerRect.collidelistall(lean_rects[stage]):
            playerRect.x = 55
            playerRect.y = 325

def drawPlayer():
    draw.rect(screen, BLUE, playerRect)

def knives(pos):
    if pos[1]:
        screen.blit(transform.flip(knifePic, True, False), (pos[0][X], pos[0][Y]))
    else:
        screen.blit(knifePic, (pos[0][X], pos[0][Y]))

def movePlayer(playerRect):
    global t
    v[X] = 0

    if (keys[K_w] and
        playerRect[Y] + playerRect[H] == v[BOTTOM] and
        v[Y] == 0 and 
        wallCollision(playerRect[X], playerRect[Y] - playerRect.height, walls) == -1):
        v[Y] = jump
    
    if keys[K_w] and playerRect.colliderect(ladders[stage]):
        v[Y] = -5
    elif playerRect.colliderect(ladders[stage]):
        v[Y] = 2
    
    if keys[K_d] and wallCollision(playerRect[X] + playerRect.width/2, playerRect[Y], walls) == -1:
        v[X] = walkSpeed

    if keys[K_a] and wallCollision(playerRect[X] - playerRect.width/2, playerRect[Y], walls) == -1:
        v[X] = -walkSpeed

    if keys[K_RIGHT]:
        if t > 2:
            knife.append([Rect(playerRect[X]+playerRect[W], playerRect[Y]+playerRect[H]/2, 15, 5), True])
            t = 0

    if keys[K_LEFT]:
        if t > 2:
            knife.append([Rect(playerRect[X]-40, playerRect[Y]+playerRect[H]/2, 15, 5), False])
            t = 0

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

        if playerRect.colliderect(i):
            v[Y] = 6

    playerRect [Y] += v[Y]
    
    if playerRect[Y] + playerRect[H] >= GROUND:
        v[2] = GROUND
        v[Y] = 0
        playerRect[Y] = GROUND-playerRect[H]

def wallCollision(playerX, playerY, walls):
    playerRect = Rect(playerX, playerY, 10, 50)
    return playerRect.collidelist(walls[stage])

def puzzle():
    global status
    screen.fill(DARKTUYU)
    for i in range(len(puzzle_buttons)):
        if button_clicked[i]:
            draw.rect(screen, GREEN, puzzle_buttons[i])
            
        else:
            draw.rect(screen, WHITE, puzzle_buttons[i])
    draw.line(screen, WHITE, (width/2, 0), (width/2, height))
    draw.line(screen, WHITE, (0, height/2), (width, height/2))

    if puzzle_pattern == user_pattern:
        status = "play"
    
    print(user_pattern)
    display.flip()

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if status == "puzzle":
            for i in range(len(puzzle_buttons)):
                if evt.type == MOUSEBUTTONDOWN and puzzle_buttons[i].collidepoint(mx, my):
                    button_clicked[i] = True
                    user_pattern.append(i+1)
    
    t += 5/60
    keys = key.get_pressed()
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    if mixer.music.get_busy() == False:
        mixer.music.play()
    
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
        
        if status == "puzzle":
            puzzle()
            
quit()
