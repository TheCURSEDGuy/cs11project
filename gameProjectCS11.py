from pygame import *

width,height= 1024,768
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE = (255, 255, 255)
menuRects = [Rect(500, 100*i+100, 200, 60) for i in range(4)] # Rectangular buttons in the menu
myClock = time.Clock()
running=True
bg = Rect(0,0,800,500)
platformRect = Rect(0,500,800,100)
draw.rect(screen,BLACK,platformRect)
pos = [55,325]
pRect = Rect(pos[0],pos[1],10,50)
g = 9.80665
vx = 0
vy = 0
t = 0

upair = False

def menu():
    screen.fill(WHITE)
    [draw.rect(screen,BLACK,i) for i in menuRects]
    return

def collide():
    
    return

def friction(vx):
    if vx > 0:
        vx -= 0.2
    if vx < 0:
        vx += 0.2
    if -0.2 < vx < 0.2:
        vx = 0
    
    return vx

def gravity(vy):
    global t
    vy += 1/2*(g)*(t)**2
    return vy

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False

    if evt.type == KEYDOWN:
        if evt.key == K_UP and not upair:
            vy -= 4
            upair = True
        if evt.key == K_RIGHT:
            if vx < 5:
                vx+=0.1
            else:
                vx = 5
        if evt.key == K_LEFT:
            if vx > -5:
                vx-=0.1
            else:
                vx = -5
    
    if evt.type == KEYUP:
        if evt.key == K_RIGHT or evt.key == K_LEFT:
            vx = friction(vx)
            


    screen.set_clip(bg)
    
    if pos[0] < 0: # Portal thingy v1
        pos[0] = 800

    if pos[0] > 800: # Portal thingy v2
        pos[0] = 0
    
            
    screen.fill((255,255,255))

    pos[1] += vy
    pos[0] += vx

    draw.rect(screen,BLACK,platformRect)
    draw.rect(screen,RED,(pos[0],pos[1],10,50))
    pRect = Rect(pos[0],pos[1],10,50)
    
    if not pRect.colliderect(platformRect):
        vy = gravity(vy)
        t+=0.01
       

    if pRect.colliderect(platformRect):
        pos[1] = 450
        vy = 0
        t = 0
        upair = False

    myClock.tick(60)

    menu()
    
    display.flip()
            
quit()