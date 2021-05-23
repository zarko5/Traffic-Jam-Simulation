import pygame as pg
import pygamebg
from array import *
import numpy as np
import random


br_semafora=10
br_car=15

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
CarLocation = np.zeros(shape=(20,20),dtype=int)
CarArr= np.zeros(shape=(br_car+1), dtype=Car)
auto_index=0
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
            if round(random.random()) and auto_index<=br_car:
                CarLocation[i][y]=1
                CarArr[auto_index] = Car()
                CarArr[auto_index].x=y*100+100
                CarArr[auto_index].y=i*100+130
                auto_index+=1

Run=True
ciklus=0
while Run:
    ciklus+=1
    surface.fill((0,0,255))
    for i in range(0,7):
        for y in range(0,15):
            if RoadArr[i][y]!=0 :
                RoadObj[i][y].draw(surface)


    for i in range(0,5,2):
        pg.draw.circle(surface, pg.Color(boje[i//2]), (semafor[i],semafor[i+1]), 20)


    for aindex in range(0,auto_index-1):
        if CarArr[aindex]!=0:
            CarArr[aindex].draw(surface)
            if CarArr[aindex].x < 1600 and CarArr[aindex].y < 800 :
                if  surface.get_at((CarArr[aindex].x+75,CarArr[aindex].y)) != pg.Color("Red"):
                    if not CarLocation[(CarArr[aindex].x)//100+1][(CarArr[aindex].y)//100]:#
                        CarArr[aindex].x=CarArr[aindex].x+1
                        CarLocation[CarArr[aindex].x//100][CarArr[aindex].y//100]=1

                        #if CarArr[aindex].x//100 - (CarArr[aindex].x-10)//100 > 1:
                         #   CarLocation[(CarArr[aindex].x-45)//100][CarArr[aindex].y//100]=0
                        

                    #else :
                     #   print("F")
                       # if CarArr[auto_index].x%100==0:
                        #    print("")
                    #else:
                      #CarLocation[CarArr[aindex].x//100][CarArr[aindex].y//100]=1
                      #CarLocation[(CarArr[aindex].x-1)]
                             #   CarLocation[CarArr[aindex].y//100-1][CarArr[aindex].x//100-1]=0
                              
            else :                  
                  CarArr[aindex].x=100
    for x in CarLocation:
      print(x)
      print("\n")

    pg.display.update()
    for event in pg.event.get():
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_ESCAPE:
                   Run=False
                   pg.quit()

