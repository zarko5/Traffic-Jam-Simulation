from numpy.lib.shape_base import _column_stack_dispatcher
import pygame as pg
from pygame.sndarray import array
from pygame.time import delay
import pygamebg
from array import *
import numpy as np

br_semafora=10
br_car=10

class Car(object):  
    def __init__(self):
        self.image = pg.image.load("./car.png").convert_alpha()
        self.x = 0
        self.y = 0
        self.image = pg.transform.rotate(self.image,270)
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Road(object):  
    def __init__(self):
        self.image = pg.image.load("./road.png").convert_alpha()
        self.x = 0
        self.y = 0
       # self.image = pg.transform.rotate(self.image,270)
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

fps = 45
semafor = array('I',[110,10,200,50,250,300,300,350])
boje = ["Red","Red","Red","Red"]
surface = pygamebg.open_window(1600,800 , "Traffic Jam Simulation")

RoadArr=[[1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1],
        [0,0,0,2,0,0,0,2,0,2,0,0,2,0,0,0],
        [0,0,0,2,0,0,0,0,1,0,0,0,2,0,0,0],
        [1,1,1,0,1,0,0,2,0,0,0,0,2,0,0,0],
        [0,0,0,2,0,2,0,2,0,0,0,0,2,0,0,0],
        [0,0,0,2,0,0,1,1,1,1,1,1,0,1,1,1],
        [1,1,1,0,1,2,0,0,2,0,0,0,2,0,0,0],
        [0,0,0,2,0,0,0,0,2,0,0,0,2,0,0,0]]
RoadObj  = np.zeros(shape=(8,16), dtype=Road)

CarArr= np.zeros(shape=(8,16), dtype=Car)

for i in range(0,7):
    for y in range(0,15):
        if RoadArr[i][y]==2 :
            RoadObj[i][y]=Road()
            RoadObj[i][y].y=i*100 
            RoadObj[i][y].x=y*100
       
        elif RoadArr[i][y]==1:
            RoadObj[i][y]=Road()
            RoadObj[i][y].y=i*100 
            RoadObj[i][y].x=y*100 
            RoadObj[i][y].image=pg.transform.rotate(RoadObj[i][y].image,90)
            CarArr[i][y] = Car()
            CarArr[i][y].x=i*100
            CarArr[i][y].y=y*100+25

        
#car.y=15
#car2.x=20
#car2.y=65

Run=True
while Run:
    surface.fill((0,0,255))
    for i in range(0,7):
        for y in range(0,15):
            if RoadArr[i][y]!=0 :
                RoadObj[i][y].draw(surface)
                if RoadArr[i][y]==1:CarArr[i][y].draw(surface)
    #car.draw(surface)
    #car2.draw(surface)
    for i in range(0,6,2):
        pg.draw.circle(surface, pg.Color(boje[i//2]), (semafor[i],semafor[i+1]), 10)
    delay(10)
    if surface.get_at((CarArr[0][0].x+50,CarArr[0][0].y)) != pg.Color("Red") :
        CarArr[0][0].x=CarArr[0][0].x+1
    #else :car.x=car.

   # CarArr[].x=car2.x+1
    #if car2.x==200 :
     #   boje[0]="Green"
      #  car.x=car.x+1
    pg.display.update()
    for event in pg.event.get():
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_ESCAPE:
                   Run=False
                   pg.quit()

