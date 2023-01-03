from pygame import *

font.init()
myClock = time.Clock()
comicFont=font.SysFont("Comic Sans MS",25)

width,height= 1280,720
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE = (255, 255, 255)

menuRects = [Rect(800+(1280-800)/2-350/2, 130*i+200, 350, 80) for i in range(4)] # Rectangular buttons in the menu
menuTXT = ["PLAY","LEVELS","SOMETHING","SOMETHING"]
TXTPos = [(i[0]+20,i[1]+20) for i in menuRects]


running=True
bg = Rect(0,0,1280,720)
platformRect = Rect(0,500,1280,100)
draw.rect(screen,BLACK,platformRect)
pos = [55,325]
pRect = Rect(pos[0],pos[1],10,50)
g = 9.80665
vx = 0
vy = 0
t = 0
status = "menu"

upair = False

def menu(mx,my):
    
    # if menuRects.collidepoin(mx,my):
    #     return
    
    
    screen.fill((147,112,219))
    screen.blit(transform.smoothscale(image.load("images/WHATR.jpg"),(800,720)),(0,0))
    
    [draw.rect(screen,WHITE,i) for i in menuRects]
    [draw.rect(screen,BLACK,i,5) for i in menuRects]
    [screen.blit(comicFont.render(i,False,GREEN),(j)) for i,j in zip(menuTXT,TXTPos)]
    
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

def move(vx,vy):
    global upair
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

    return vx,vy

def gravity(vy):
    
    global t
    vy += 1/2*(g)*(t)**2
    return vy

def play(vx,vy,pos,t):
    vy = gravity(vy)
    if evt.type == KEYDOWN:
        vx,vy = move(vx,vy)
    
    if evt.type == KEYUP:
        if evt.key == K_RIGHT or evt.key == K_LEFT:
            vx = friction(vx)
            
    if pos[0] < 0: # Portal thingy v1
        pos[0] = 800

    if pos[0] > 800: # Portal thingy v2
        pos[0] = 0
    
            
    screen.fill(WHITE)

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

    return vx,vy,pos,t

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False

    mx,my = mouse.get_pos()

    if status == "menu":
        menu(mx,my)

    if status == "play":
        vx,vy,pos,t = play(vx,vy,pos,t)


    myClock.tick(60)
    
    display.flip()
            
quit()