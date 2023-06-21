from operator import truediv
from warnings import catch_warnings
import pygame
from pygame.locals import *
import sys
import random
import math 

pygame.init()

resolution = pygame.display.Info()
gridsize =  15

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
color_light = (170,170,170)
color_dark = (100,100,100)
turquoise = (64, 224, 208)

lblue = (0, 1.5*47, 1.5*150)
blue = (0, 47, 150)
dblue = (0,12,37)

lpurple = (172, 37, 210)
purple = (128, 25, 140)
dpurple = (32, 6, 70)

lpink= (255, 0, 1.5*114 )
pink = (186, 0, 114)
dpink = (46, 0, 28)

lraspberry = (255, 61, 120)
raspberry = (219, 41, 80)
draspberry = (54, 10, 20)

lorange = (255, 129 ,66)
orange = (229, 93, 44)
dorange = (64, 23, 11)

lapricot = (255, 211, 0)
apricot = (186, 141, 0)
dapricot = (46, 35, 0)

lyellow =(255, 255, 0)
yellow = (191, 184, 0)
dyellow = (47, 46, 0)



width = resolution.current_w
wnum = width//gridsize
height = resolution.current_h
hnum = height//gridsize
resolution = (wnum*gridsize, hnum*gridsize)



# Idee: Man macht zwei mal Listen in einer Liste für alive und bors und
# dann noch jeweils Konstanten, die nach links oder rechts angepasst werden,
# wenn das Life den Rahmen verlässt, damit man anhand der Konstante die alten
# Koordinaten ausrechnen kann, die tatsächlich angezeigt werden. 

smallfont = pygame.font.SysFont('Corbel', 25)


screen = pygame.display.set_mode(resolution)
    


class game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        self.mode = True # set to True for endless mode
        self.aura = False # "Leuchten um die lebendigen Zellen"
        self.minesweepermode = False #
        self.status = True
        self.color = True
        self.sparkle = True
        self.torusmode = True # False für Rand
        self.clock = pygame.time.Clock()
        self.alive = [[False for i in range(hnum)] for j in range(wnum)]
        self.bors = [[0 for i in range(hnum)] for j in range(wnum)]
        self.alivegen1 = [[False for i in range(hnum)] for j in range(wnum)]
        self.alivegen2 = [[False for i in range(hnum)] for j in range(wnum)]
        self.alivegen3 = [[False for i in range(hnum)] for j in range(wnum)]
        self.alivegen4 = [[False for i in range(hnum)] for j in range(wnum)]
        self.alivegen5 = [[False for i in range(hnum)] for j in range(wnum)]
        self.alivegen6 = [[False for i in range(hnum)] for j in range(wnum)]


    def brighten(self, x):
        return (min(255,x[0]*1.5), min(255,x[1]*1.5), min(255,x[2]*1.5))


    #def brighten(self,x):
    #    return x

    #def borsnum(self, x, y):
    #    count = 0
    #    if(x>0):
    #        if(y>0):
    #            if self.alive[x-1][y-1]:
    #                count += 1
    #        if self.alive[x-1][y]:
    #            count+=1
    #        if (y<hnum):
    #            if self.alive[x-1][y+1]:
    #                count+=1
    #    if(x<wnum):
    #        if(y>0):
    #            if self.alive[x+1][y-1]:
    #                count+=1
    #        if self.alive[x+1][y]:
    #            count+=1
    #        if (y<hnum):
    #            if self.alive[x+1][y+1]:
    #                count+=1
    #    if(y>0):
    #        if self.alive[x][y-1]:
    #            count+=1
    #    if(y<hnum):
    #        if self.alive[x][y+1]:
    #            count+=1
    #    return count



    def addbors(self, x, y):
        self.bors[(x-1) % wnum][(y-1) % hnum] += 1
        self.bors[(x-1) % wnum][y] += 1
        self.bors[(x-1) % wnum][(y+1) % hnum] += 1
        self.bors[(x+1) % wnum][(y-1) % hnum] += 1
        self.bors[(x+1) % wnum][y] += 1
        self.bors[(x+1) % wnum][(y+1) % hnum] += 1
        self.bors[x][(y-1) % hnum] += 1
        self.bors[x][(y+1) % hnum] += 1

    

    def removebors(self, x, y):
        self.bors[(x-1) % wnum][(y-1) % hnum] -= 1
        self.bors[(x-1) % wnum][y] -= 1
        self.bors[(x-1) % wnum][(y+1) % hnum] -= 1
        self.bors[(x+1) % wnum][(y-1) % hnum] -= 1
        self.bors[(x+1) % wnum][y] -= 1
        self.bors[(x+1) % wnum][(y+1) % hnum] -= 1
        self.bors[x][(y-1) % hnum] -= 1
        self.bors[x][(y+1) % hnum] -= 1
    


    #def addbors(self,x,y):
    #    if(x>0):
    #        if(y>0):
    #            self.bors[x-1][y-1]+=1
    #        self.bors[x-1][y]+=1
    #        if (y<hnum):
    #            self.bors[x-1][y+1]+=1
    #    if(x<wnum):
    #        if(y>0):
    #            self.bors[x+1][y-1]+=1
    #        self.bors[x+1][y]+=1
    #        if (y<hnum):
    #            self.bors[x+1][y+1]+=1
    #    if(y>0):
    #        self.bors[x][y-1]+=1
    #    if(y<hnum):
    #        self.bors[x][y+1]+=1

            

    #def removebors(self,x,y):
    #    if(x>0):
    #        if(y>0):
    #            self.bors[x-1][y-1]-=1
    #        self.bors[x-1][y]-=1
    #        if (y<hnum):
    #            self.bors[x-1][y+1]-=1
    #    if(x<wnum):
    #        if(y>0):
    #            self.bors[x+1][y-1]-=1
    #        self.bors[x+1][y]-=1
    #        if (y<hnum):
    #            self.bors[x+1][y+1]-=1
    #    if(y>0):
    #        self.bors[x][y-1]-=1
    #    if(y<hnum):
    #        self.bors[x][y+1]-=1



    def rainbow(self, x,y):
        max = wnum 
        if (x < max/7):
            return lblue if (self.alive[x][y] and (not self.alivegen1[x][y])) else blue
        else:
            if (x < (2*max)/7):
                return lpurple if (self.alive[x][y] and (not self.alivegen1[x][y])) else purple
            else:
                if(x < (3*max)/7):
                    return lpink if (self.alive[x][y] and (not self.alivegen1[x][y])) else pink
                else:
                    if(x < (4*max)/7):
                        return lraspberry if (self.alive[x][y] and (not self.alivegen1[x][y])) else raspberry 
                    else:
                        if(x < (5*max)/7):
                            return lorange if (self.alive[x][y] and (not self.alivegen1[x][y])) else orange
                        else:
                            if(x <(6*max)/7):
                                return lapricot if (self.alive[x][y] and (not self.alivegen1[x][y])) else apricot
                            else:
                                return lyellow if (self.alive[x][y] and (not self.alivegen1[x][y])) else yellow

                            
    
    def darkrainbow(self, x,y):
        max = wnum 
        if (x < max/7):
            return dblue
        else:
            if (x < (2*max)/7):
                return dpurple
            else:
                if(x < (3*max)/7):
                    return dpink
                else:
                    if(x < (4*max)/7):
                        return draspberry 
                    else:
                        if(x < (5*max)/7):
                            return dorange
                        else:
                            if(x <(6*max)/7):
                                return dapricot
                            else:
                                return dyellow

        
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                if mouse_presses[0]:
                    if  10 <= pos[0] <= 80 and 10 <= pos[1] <= 40:
                        self.status = not self.status
                    else:
                        if 100 <= pos[0] <= 170 and 10 <= pos[1] <= 40:
                            self.status = True
                            self.alive = [[False for i in range(hnum)] for j in range(wnum)]
                            self.bors = [[0 for i in range(hnum)] for j in range(wnum)]
                        else:
                            if self.status:
                                x = pos[0]//gridsize
                                y = pos[1]//gridsize
                                self.alive[x][y] = not self.alive[x][y]
                                if self.alive[x][y]:
                                    self.addbors(x,y)
                                else:
                                    self.removebors(x,y)



    def updatelife(self):
        tempadd = []
        tempdel = []
        for x in range(wnum):
            for y in range(hnum):
                if self.bors[x][y]>0 or self.alive[x][y]:
                    if not self.alive[x][y] and self.bors[x][y] == 3:
                        tempadd.append([x,y])
                    if self.alive[x][y] and (self.bors[x][y] <2 or self.bors[x][y]>3):
                        tempdel.append([x,y])
        if self.mode:
            for x in range(wnum):
                for y in range(hnum):
                    self.alivegen6[x][y] = self.alivegen5[x][y]
                    self.alivegen5[x][y] = self.alivegen4[x][y]
                    self.alivegen4[x][y] = self.alivegen3[x][y]
                    self.alivegen3[x][y] = self.alivegen2[x][y]
                    self.alivegen2[x][y] = self.alivegen1[x][y]
                    self.alivegen1[x][y] = self.alive[x][y]
        for a in tempadd:
            self.alive[a[0]][a[1]] = True
            self.addbors(a[0],a[1])
        for d in tempdel:
            self.alive[d[0]][d[1]] = False
            self.removebors(d[0],d[1])
        if not (tempadd or tempdel):
            if self.mode:
                dead = True
                for x in range(wnum):
                    for y in range(hnum):
                        dead = dead and (not self.alive[x][y])
                if not dead:
                    borslist = []
                    for x in range(wnum):
                        for y in range(hnum):
                            if (self.alive[x][y] == False) and (self.bors[x][y]>0):
                                borslist.append([x,y])
                    length = len(borslist)
                    pick = borslist[random.randint(0,length-1)]
                    self.alive[pick[0]][pick[1]]= True
                    self.addbors(pick[0],pick[1])
                else:
                    for z in range(5*wnum):
                        x = random.randint(0,wnum-1)
                        y = random.randint(0,hnum-1)
                        if not self.alive[x][y]:
                            self.alive[x][y]=True
                            self.addbors(x,y)
            else:
                self.status = True
        else:
            if self.mode:
                cycle = True
                for x in range(wnum):
                    for y in range(hnum):
                        cycle = cycle and (self.alive[x][y] == self.alivegen6[x][y])
                dead = True
                for x in range(wnum):
                    for y in range(hnum):
                        dead = dead and (not self.alive[x][y])
                if cycle and (not dead):
                    borslist = []
                    for x in range(wnum):
                        for y in range(hnum):
                            if (not self.alive[x][y] ) and self.bors[x][y] > 0:
                                borslist.append([x,y])
                    length = len(borslist)
                    pick = borslist[random.randint(0,length-1)]
                    self.alive[pick[0]][pick[1]]= True
                    self.addbors(pick[0],pick[1])


    
    
    def run(self):
        time=0
        while True:
            time+=1
            self.handleEvents()
            self.screen.fill(black)
            mouse = pygame.mouse.get_pos()

            if not self.status:
                if time>=60:
                    self.updatelife()
                    time=0

            #for x in range(wnum):
            #    pygame.draw.line(screen, white, [x*gridsize, 0], [x*gridsize, height], 1)
            #for y in range(hnum):
            #    pygame.draw.line(screen, white, [0, y*gridsize], [width, y*gridsize], 1)

            for i in range(wnum):
                for j in range(hnum):
                    if self.alive[i][j]:
                        if self.color:
                            pygame.draw.rect(screen, self.rainbow(i,j),[i*gridsize, j*gridsize, gridsize, gridsize], 0)
                        else:
                            pygame.draw.rect(screen, turquoise, [i*gridsize, j*gridsize, gridsize, gridsize])
                        

            if self.aura:
                for i in range(wnum):
                    for j in range(hnum):
                        if not self.alive[i][j] and self.bors[i][j]>0:
                            if self.color:
                                pygame.draw.rect(screen, self.darkrainbow(i,j),[i*gridsize, j*gridsize, gridsize, gridsize], 0)
                            else:
                                pygame.draw.rect(screen, turquoise, [i*gridsize, j*gridsize, gridsize, gridsize])
    
            # start/stop button
            if 10 <= mouse[0] <= 80 and 10 <= mouse[1] <= 40:
                pygame.draw.rect(screen,color_dark, [10, 10, 70, 30])
            else:
                pygame.draw.rect(screen,color_light, [10, 10, 70, 30])
            if self.status:
                screen.blit(smallfont.render('start', True, black), [20, 12, 50, 20])
            else: 
                screen.blit(smallfont.render('stop', True, black), [20, 12, 50, 20])

            # clear button
            if 100 <= mouse[0] <= 170 and 10 <= mouse[1] <= 40:
                pygame.draw.rect(screen,color_dark, [100, 10, 70, 30])
            else:
                pygame.draw.rect(screen,color_light, [100, 10, 70, 30])
            screen.blit(smallfont.render('clear', True, black), [110, 12, 50, 20])

            if self.minesweepermode:
                for x in range(wnum):
                    for y in range(hnum):
                        if self.alive[x][y] or self.bors[x][y]>0:
                            if self.alive[x][y]:
                                screen.blit(smallfont.render(str(self.bors[x][y]), True, white), [x*gridsize+2, y*gridsize-4, gridsize/2, gridsize/2])
                            else:
                                screen.blit(smallfont.render(str(self.bors[x][y]), True, white), [x*gridsize+2, y*gridsize-4, gridsize/2, gridsize/2])

            self.clock.tick(200)
            pygame.display.flip()


game().run()


   


