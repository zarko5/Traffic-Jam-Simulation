#!/bin/python
import pygame as pg
import numpy as np
import random

# import pygame.mixer
# pg.init()
# pg.mixer.music.load("music1.ogg")
# pg.mixer.music.play(-1)

sirina = 1700
visina = 900


# CarDirection 0 je desno,1 je gore , 2 je dole
br_semafora = 10
br_car = 20


class Car(object):  # klasa za automobile
    def __init__(self):
        self.image = pg.image.load("./car.png").convert_alpha()
        self.x = 0
        self.y = 0
        self.image = pg.transform.rotate(self.image, 90)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def rotiraj(self,smer):
        #ovaj deo moze i da ima or da je smer = int da bi se poklapao sa CarDirection
        self.image = pg.image.load("./car.png").convert_alpha()
        if (smer == "gore" ):#or smer == 0):
            self.image = pg.transform.rotate(self.image,0) # U sustini ne radi nista sa slikom posto se uspravna slika ucitava pre if-a
        elif (smer == "dole"):
            self.image = pg.transform.rotate(self.image,180)
        elif (smer == "levo"):
            self.image = pg.transform.rotate(self.image,270)
        elif (smer == "desno"):
            self.image = pg.transform.rotate(self.image,90)

class Road(object):  # klasa za puteve
    def __init__(self):
        self.image = pg.image.load("./put.png").convert_alpha()
        self.x = 0
        self.y = 0
        
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Semafor(object):
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def draw(self,surface,boja):
         pg.draw.circle(surface, pg.Color(boja), (self.x, self.y), 20)


def osvezi_lokacije(aindx,CarLoc):  # Prolazi kroz sve aute i markira polja na kojima se nalaze kao zauzeta 
    for i in range(0,8):
        for y in range(0,17):
            CarLoc[i][y]=0
    for index in range(0,aindx):
        CarLoc[CarArr[index].y // 100][CarArr[index].x // 100] = 1
#    for index in br_semafora:#Menjamo polje na jedan samo ako je boja crvena



semafor = np.array([450, 140, 450, 440, 250, 300, 300, 350])#ovaj  array ce postati niz klasa nakon ubacivanja raskrsnica
boje = ["Red", "Red", "Red", "Red"]
#boje = []#Prazna lista + append kad se dodaje novi semafor, nakon sto se ubace raskrsnice

pg.init()
surface = pg.display.set_mode((sirina,visina))
pg.display.set_caption("Traffic Jam Simulation")


##const matrix puteva koji postoje,mozda kasnije i nasumicni
# Horizontalan put - 1
# Vertikalan put - 2
# Raskrsnica - 3
# T_put - 4
RoadArr = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
]

##
RoadObj = np.zeros(shape=(8, 16), dtype=Road)  # Objekti puteva

CarLocation = np.zeros(shape=(8, 17), dtype=int)  # Lokacije auta u matrici

CarArr = np.zeros(shape=(br_car + 1), dtype=Car)  # Objekti automobila

CarDirection = np.zeros(shape=(br_car + 1), dtype=int)  # smer kretanja automobila

semafori = np.zeros(shape=(8,17),dtype=Semafor)

auto_index = 0  # ovo treba promenu kako bi uvek bio ispunjen broj automobila br_car, samo se generisu na random lokacijama,
for i in range(0, 7):
    for y in range(0, 15):
        if RoadArr[i][y] == 2:
            RoadObj[i][y] = Road()
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
        elif RoadArr[i][y] == 1:
            RoadObj[i][y] = Road()
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
            RoadObj[i][y].image = pg.transform.rotate(RoadObj[i][y].image, 90)
            if round(random.random()) and auto_index <= br_car:
                CarLocation[i][y] = 1
                CarDirection[auto_index] = 0
                CarArr[auto_index] = Car()
                CarArr[auto_index].x = y * 100 + 100
                CarArr[auto_index].y = i * 100 + 130
                auto_index += 1


boja = 0
Run = True
ciklus = 0
random.seed(23617282344)#PRNG eksperiment
while Run:
    ciklus += 1
    surface.fill((0, 0, 255))
    for i in range(0, 7):
        for y in range(0, 15):
            if RoadArr[i][y] != 0:
                RoadObj[i][y].draw(surface)

    for i in range(0, 4, 2):# Stari nacin iscrtavanja semafora, bice obrisan nakon ubacivanja raskrsnica 
         pg.draw.circle(surface, pg.Color(boje[i // 2]), (semafor[i], semafor[i + 1]), 20)
    ##
    #Novi semafori
    ##

    #CarArr[0].rotiraj(0)
    
    osvezi_lokacije(auto_index,CarLocation)
    for aindex in range(0, auto_index ):
        CarArr[aindex].draw(surface)
        if CarArr[aindex].x < 1600 and CarArr[aindex].y < 800:
            if (
                CarDirection[aindex] == 0
                and surface.get_at((CarArr[aindex].x + 75, CarArr[aindex].y))
                != pg.Color("Red")
                and surface.get_at((CarArr[aindex].x + 75, CarArr[aindex].y))
                != pg.Color("Blue")
            ):
                if (CarLocation[(CarArr[aindex].y)//100][(CarArr[aindex].x)//100+1] != 1 and CarArr[aindex].x // 100 + 1 < 16):  #
                    CarArr[aindex].x = CarArr[aindex].x + 1
                elif (
                    CarArr[aindex].x // 100 + 1 > 15
                    and CarLocation[CarArr[aindex].y//100][1] == 0
                ):
                    CarArr[aindex].x = 100  # Teleportacija na pocetak 

                    """ if (Stvari nadalje su nepotrebne posto ce gore ici drugi sistem rotacije
                        abs(CarArr[aindex].x // 100 - (CarArr[aindex].x - 1) // 100)
                        == 1
                    ):
                        print("f")
                    #    CarLocation[(CarArr[aindex].x) // 100 - 1][
                        #CarArr[aindex].y // 100
                        #] = 0
                if surface.get_at(
                    (CarArr[aindex].x + 75, CarArr[aindex].y)
                ) == pg.Color("Blue"):
                    if surface.get_at(
                        (CarArr[aindex].x, CarArr[aindex].y + 75)
                    ) == pg.Color("Blue") and surface.get_at(
                        (CarArr[aindex].x, CarArr[aindex].y - 75)
                    ) == pg.Color(
                        "Blue"
                    ): 
                        CarDirection[aindex] = random.randint(1, 2)
                        if CarDirection[aindex] == 1:
                            angle = 90
                        else:
                            angle = 270
                        CarArr[aindex].image = pg.transform.rotate(
                            CarArr[aindex].image, angle
                        )

                    elif surface.get_at(
                        (CarArr[aindex].x, CarArr[aindex].y + 75)
                    ) == pg.Color("Blue"):
                        CarDirection[aindex] = 2
                        CarArr[aindex].image = pg.transform.rotate(
                            CarArr[aindex].image, 270
                        )
                    else:
                        CarDirection[aindex] = 1
                        CarArr[aindex].image = pg.transform.rotate(
                            CarArr[aindex].image, 90
                        )"""
                        # 
    
    if ciklus > 70 and random.randint(0,100)>99:
        random.seed(round(random.random()*10000))        
        ciklus = 0
        if boja == 0:
            boje[0] = pg.Color("Green")
            boje[1] = pg.Color("Green")
            boja = 1
        else:
            boje[0] = pg.Color("Red")
            boje[1] = pg.Color("Red ")
            boja = 0
    pg.display.update()

    # gasenje programa na ESC
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                Run = False
                pg.quit()
