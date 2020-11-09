'''
Graphics Assignment by Rayton Chen

full list of items:
beach
sea (moving waves)
clouds (4, moving in cycle)
sun (clickable, 5 positions, changing colours between light and dark red)
boat (moving up and down)
sail (also moving with the boat, and clickable to change directions)
rope (moving with the boat on one end, tied to the tree on the other end)
trees (3)
beach chair (clickable, colour change)
umbrella (clickable; if clicked on the green part, the outside ring starts/stops changing colours. click again and it will stop/start again)
rocks (3, clickable. each one disappears indivdually if clicked)
fish (2 X 7 = 14 total. moving in a cycle at different speeds, changing colours)
seaweeds (12)

note that pygame arcs arent completely filled in so clicking on semi circles might not work the first time
'''


from pygame import *
from itertools import cycle
from random import *

width,height=1200,600

screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE = (255,255,255)
DGREEN = (31, 107, 32)

#calculation variables

PI = 3.1415926535897932384626

waves = [[x,550] for x in range(-100,1201,100)]

sail = 1

suncol = [190,0,0]
sunxpos = cycle([0,200,400,600,800,600,400,200])
sunx = next(sunxpos)

boatoffset = 0
x=1

cloudoffset = 0

fishoffset1 = 0
fishoffset2 = 0

colours = cycle(['green', 'pink', 'red', 'orange', 'yellow'])
firstc = next(colours)
nextc = next(colours)
curc = firstc
steps = 90
curstep = 1


rock1 = 1
rock2 = 1
rock3 = 1

utemp = firstc
uchange = 1

chaircols = cycle([(120,120,255),(80,200,80)])
chaircol = next(chaircols)

#main loop
running=True
clock = time.Clock()

while running:
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type == MOUSEBUTTONDOWN:
            #since we do not want press and hold, the following goes under MOUSEBUTTONDOWN
            #chair
            if screen.get_at((mx,my)) == GREY:
                chaircol = next(chaircols)
            #umbrella
            if screen.get_at((mx,my)) == GREEN and my < 450:
                uchange = (uchange+1)%2
                       
    ########################### calculations ###########################
    
    #waves
    for i in range(len(waves)):
     waves[i][0]+=5
     if waves[i][0] == 1250:
         waves[i][0]-=1300

    #sail
    if mb[0] and screen.get_at((mx,my)) == WHITE:
        sail = (sail+1)%2

    #sun
    if suncol[0] == 255:
        change = -1
    elif suncol[0] == 190:
        change = 1
    suncol[0] += change
    suncol[1] += change
    if mb[0] and Rect(30+sunx,30,80,80).collidepoint(mx,my):
        sunx = next(sunxpos)

    #clouds
    if cloudoffset < -1200:
        cloudoffset = +1200
    cloudoffset -= 2

    #fish1
    if fishoffset1 >1200:
        fishoffset1 = -500
    fishoffset1 += 3

    #fish2
    if fishoffset2 >600:
        fishoffset2 = -1000
    fishoffset2 += 4

    #fishcolour
    curstep += 1
    if curstep < steps: #if we havent reached the next colour
        curc = [x + (((y-x)/steps)*curstep) for x, y in zip(color.Color(firstc), color.Color(nextc))] #change per step * curstep. iterate thru firstc and nextc at the same time, fading firstc into nextc        
    else: #reached next colour, go to the next colour after that
        curstep = 1
        firstc = nextc
        nextc = next(colours)
        
    #boat up and down
    if boatoffset == -25:
        x = 1
    elif boatoffset == 25:
        x = -1
    boatoffset += x

    #rocks
    if mb[0]:
        if screen.get_at((mx,my)) == (92, 76, 46, 255):
            rock1 = 0
        if screen.get_at((mx,my)) == (102, 86, 46 ,255):
            rock2 = 0
        if screen.get_at((mx,my)) == (82, 66, 36, 255):
            rock3 = 0
        

    ########################### draw stuff ###########################
    screen.fill((3, 248, 252))
    
    #beach
    draw.circle(screen, YELLOW, (1000,2200),1900)
    
    #trees
    draw.polygon(screen,(196, 85, 16),[(700,330),(750,330),(700,180),(650,180),])
    draw.arc(screen, DGREEN, (525,150,150,60),0,PI,25)
    draw.arc(screen, DGREEN, (675,150,150,65),0,PI,25)
    
    draw.polygon(screen,(196, 85, 16),[(600,370),(650,370),(600,230),(550,230),])
    draw.arc(screen, DGREEN, (425,200,150,60),0,PI,25)
    draw.arc(screen, DGREEN, (575,200,150,65),0,PI,25)

    draw.polygon(screen,(196, 85, 16),[(500,410),(550,410),(500,280),(450,280),])
    draw.arc(screen, DGREEN, (325,250,150,60),0,PI,25)
    draw.arc(screen, DGREEN, (475,250,150,65),0,PI,25)

    #boat and sail
    draw.polygon(screen,(196, 85, 16),[(20,360+boatoffset),(320,360+boatoffset),(270,450+boatoffset),(70,450+boatoffset)])
    draw.rect(screen,(176, 65, 0),(160,200+boatoffset,20,160))
    draw.line(screen,BLACK,(320,360+boatoffset),(525,345),5)
    if sail:
        draw.polygon(screen,WHITE,[(180,200+boatoffset),(180,360+boatoffset),(280,280+boatoffset)])
    else:
        draw.polygon(screen,WHITE,[(160,200+boatoffset),(160,360+boatoffset),(60,280+boatoffset)])

    #sun
    draw.rect(screen,YELLOW,(30+sunx,30,80,80))
    draw.polygon(screen,YELLOW,[(15+sunx,70),(70+sunx,15),(125+sunx,70),(70+sunx,125)])
    draw.circle(screen,suncol,(70+sunx,70),40)

    #clouds
    draw.circle(screen,(225, 252, 249),(230+cloudoffset,80), 40)
    draw.circle(screen,(225, 252, 249),(260+cloudoffset,60), 40)
    draw.circle(screen,(225, 252, 249),(320+cloudoffset,80), 40)
    draw.circle(screen,(225, 252, 249),(270+cloudoffset,80), 40)

    draw.circle(screen,(225, 252, 249),(430+cloudoffset,60), 40)
    draw.circle(screen,(225, 252, 249),(490+cloudoffset,40), 40)
    draw.circle(screen,(225, 252, 249),(520+cloudoffset,60), 40)
    draw.circle(screen,(225, 252, 249),(470+cloudoffset,60), 40)
    
    draw.circle(screen,(225, 252, 249),(630+cloudoffset,100), 40)
    draw.circle(screen,(225, 252, 249),(660+cloudoffset,80), 40)
    draw.circle(screen,(225, 252, 249),(720+cloudoffset,100), 40)
    draw.circle(screen,(225, 252, 249),(670+cloudoffset,100), 40)
    draw.ellipse(screen,(225,252,249),(720+cloudoffset,55,110,80))

    draw.circle(screen,(225, 252, 249),(1030+cloudoffset,80), 40)
    draw.circle(screen,(225, 252, 249),(1090+cloudoffset,60), 40)
    draw.circle(screen,(225, 252, 249),(1120+cloudoffset,80), 40)
    draw.circle(screen,(225, 252, 249),(1070+cloudoffset,80), 40)
    draw.ellipse(screen,(225,252,249),(920+cloudoffset,40,110,80))

    #beach chair 
    draw.polygon(screen,chaircol,[(830,220),(1000,220),(980,310),(810,310)])
    draw.polygon(screen,(0,0,150),[(980,310),(810,310),(710,340),(880,340)])
    draw.rect(screen,GREY,(710,340,170,40))
    draw.polygon(screen, BLACK,[(980,310),(880,340),(880,380),(980,350)])
    draw.polygon(screen, BLACK,[(1000,260),(1000,220),(980,310),(980,350)])
    draw.line(screen,BLACK,(810,310),(980,310))

    #umbrella
    draw.rect(screen,(0,0,0),(1030,170,20,200))
    draw.arc(screen, GREEN, (870,0,340,340),0,PI,170)
    if uchange:
        utemp = curc
    draw.arc(screen,utemp, (870,0,340,340),0,PI,85)

    #rocks
    if rock1 == 1:
        draw.ellipse(screen, (92, 76, 46), (1100,360,40,30))
    if rock2 == 1:
        draw.ellipse(screen, (102, 86, 46), (1130,350,40,30))
    if rock3 == 1:
        draw.ellipse(screen, (82, 66, 36), (1130,370,40,30))
    

    #sea
    draw.rect(screen,BLUE,(0,450,1200,200))
    for i in range(len(waves)):
         draw.circle(screen,BLUE,waves[i],150)

    #fish
    ##first pack
    draw.polygon(screen,curc,[(140+fishoffset1,480),(140+fishoffset1,500),(160+fishoffset1,490)])
    draw.ellipse(screen,curc,(155+fishoffset1,475,60,30))

    draw.polygon(screen,curc,[(180+fishoffset1,440),(180+fishoffset1,460),(200+fishoffset1,450)])
    draw.ellipse(screen,curc,(195+fishoffset1,435,60,30))

    draw.polygon(screen,curc,[(240+fishoffset1,470),(240+fishoffset1,490),(260+fishoffset1,480)])
    draw.ellipse(screen,curc,(255+fishoffset1,465,60,30))

    draw.polygon(screen,curc,[(280+fishoffset1,430),(280+fishoffset1,450),(300+fishoffset1,440)])
    draw.ellipse(screen,curc,(295+fishoffset1,425,60,30))

    draw.polygon(screen,curc,[(210+fishoffset1,510),(210+fishoffset1,530),(230+fishoffset1,520)])
    draw.ellipse(screen,curc,(225+fishoffset1,505,60,30))

    draw.polygon(screen,curc,[(310+fishoffset1,500),(310+fishoffset1,520),(330+fishoffset1,510)])
    draw.ellipse(screen,curc,(325+fishoffset1,495,60,30))

    ##second pack
    draw.polygon(screen,curc,[(140+600+fishoffset2,480),(140+600+fishoffset2,500),(160+600+fishoffset2,490)])
    draw.ellipse(screen,curc,(155+600+fishoffset2,475,60,30))

    draw.polygon(screen,curc,[(180+600+fishoffset2,440),(180+600+fishoffset2,460),(200+600+fishoffset2,450)])
    draw.ellipse(screen,curc,(195+600+fishoffset2,435,60,30))

    draw.polygon(screen,curc,[(240+600+fishoffset2,470),(240+600+fishoffset2,490),(260+600+fishoffset2,480)])
    draw.ellipse(screen,curc,(255+600+fishoffset2,465,60,30))

    draw.polygon(screen,curc,[(280+600+fishoffset2,430),(280+600+fishoffset2,450),(300+600+fishoffset2,440)])
    draw.ellipse(screen,curc,(295+600+fishoffset2,425,60,30))

    draw.polygon(screen,curc,[(210+600+fishoffset2,510),(210+600+fishoffset2,530),(230+600+fishoffset2,520)])
    draw.ellipse(screen,curc,(225+600+fishoffset2,505,60,30))

    draw.polygon(screen,curc,[(310+600+fishoffset2,500),(310+600+fishoffset2,520),(330+600+fishoffset2,510)])
    draw.ellipse(screen,curc,(325+600+fishoffset2,495,60,30))

    #seaweed
    for i in range(0,1200,100):
        draw.arc(screen,GREEN, (i+40,550,30,100),PI/2,PI,10)
        draw.arc(screen,GREEN, (i+10,550,30,100),0,PI/2,10)

    
    clock.tick(30)
    display.flip()            
quit()
