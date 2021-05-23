#from numpy.lib.shape_base import _column_stack_dispatcher
import pygame as pg
#from pygame.sndarray import array
#from pygame.time import delay
import pygamebg
from array import *
import numpy as np
import random


br_semafora=10
br_car=10

class Car(object):  
    def __init__(self):
        self.image = pg.image.load("./car.png").convert_alpha()
        self.x = 0
        self.y = 0
        self.image = pg.transform.rotate(self.image,90)
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Road(object):     
    def __init__(self):
        self.image = pg.image.load("./road.png").convert_alpha()
        self.x = 0
        self.y = 0
        #self.image = pg.transform.rotate(self.image,270)
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

fps = 45
semafor = array('I',[450,140,450,440,250,300,300,350])
boje = ["Red","Red","Red","Red"]
surface = pygamebg.open_window(1700,900 , "Traffic Jam Simulation")

RoadArr=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,2,0,0,0,2,0,2,0,0,2,0,0,0],
        [0,0,0,2,0,0,0,1,1,1,0,0,2,0,0,0],
        [1,1,1,1,1,1,1,2,0,0,0,0,2,0,0,0],
        [0,0,0,2,0,2,0,2,0,0,0,0,2,0,0,0],
        [0,0,0,2,0,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,2,0,0,2,0,0,0,2,0,0,0],
        [0,0,0,2,0,0,0,0,2,0,0,0,2,0,0,0]]
RoadObj  = np.zeros(shape=(8,16), dtype=Road)
CarLocation = np.zeros(shape=(8,16),dtype=int)
CarArr= np.zeros(shape=(8,16), dtype=Car)

for i in range(0,7):
    for y in range(0,15):
        if RoadArr[i][y]==2 :
            RoadObj[i][y]=Road()
            RoadObj[i][y].y=i*100+100 
            RoadObj[i][y].x=y*100+100
        elif RoadArr[i][y]==1:
            RoadObj[i][y]=Road()
            RoadObj[i][y].y=i*100 +100
            RoadObj[i][y].x=y*100 + 100
            RoadObj[i][y].image=pg.transform.rotate(RoadObj[i][y].image,90)
            if round(random.random()):
                CarLocation[i][y]=1
                CarArr[i][y] = Car()
                CarArr[i][y].x=y*100+100
                CarArr[i][y].y=i*100+130

Run=True
while Run:
    surface.fill((0,0,255))
    for i in range(0,7):
        for y in range(0,15):
            if RoadArr[i][y]!=0 :
                RoadObj[i][y].draw(surface)


    for i in range(0,5,2):
        pg.draw.circle(surface, pg.Color(boje[i//2]), (semafor[i],semafor[i+1]), 20)


    for i in range(0,7):
        for y in range(0,15):
                if CarArr[i][y]!=0:
                    CarArr[i][y].draw(surface)
                    if CarArr[i][y].x < 1600 and CarArr[i][y].y < 800 :
                        if  surface.get_at((CarArr[i][y].x+75,CarArr[i][y].y)) != pg.Color("Red") and not CarLocation[i+1][y]:#and surface.get_at((CarArr[i][y].x+35,CarArr[i][y].y)) != pg.Color("Red") :
                            CarArr[i][y].x=CarArr[i][y].x+1
                        if CarArr[i][y].x%100==0:
                            print("")
                           # if not CarLocation[CarArr[i][y].y//100][CarArr[i][y].x//100]:
                            #    CarLocation[CarArr[i][y].y//100][CarArr[i][y].x//100]=1
                             #   CarLocation[CarArr[i][y].y//100-1][CarArr[i][y].x//100-1]=0
                              #  for x in CarLocation:
                               #     print(x)
                               # print("\n") 
                    else :
                          CarArr[i][y].x=100

    pg.display.update()
    for event in pg.event.get():
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_ESCAPE:
                   Run=False
                   pg.quit()

