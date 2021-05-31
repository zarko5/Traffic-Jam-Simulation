import pygame as pg
import pygamebg
import numpy as np
import random


# muzika, nakon inita
# import pygame.mixer
# pg.init()
# pg.mixer.music.load("music1.ogg")
# pg.mixer.music.play(-1)


# CarDirection 0 je desno,1 je gore , 2 je dole
br_semafora = 10
br_car = 10


class Car(object):  # klasa za automobile
    def __init__(self):
        self.image = pg.image.load("./car.png").convert_alpha()
        self.x = 0
        self.y = 0
        self.image = pg.transform.rotate(self.image, 90)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def rotiraj(self,smer):
        self.image = pg.image.load("./car.png").convert_alpha()
        if (smer == "gore"):
            self.image = pg.transform.rotate(self.image,0) # U sustini ne radi nista sa slikom posto se uspravna slika ucitava pre if-a 
        elif (smer == "dole"):
            self.image = pg.transform.rotate(self.image,180)
        elif (smer == "levo"):
            self.image = pg.transform.rotate(self.image,270)
        elif (smer == "desno"):
            self.image = pg.transform.rotate(self.image,90)

class Road(object):  # klasa za puteve
    def __init__(self):
        self.image = pg.image.load("./road.png").convert_alpha()
        self.x = 0
        self.y = 0
        # self.image = pg.transform.rotate(self.image,270)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


def osvezi_lokacije(aindx,CarLoc):  # Prolaz kroz sva polja CarLocation i proverava da li ima automobila na njima, mozda bi mogao i da se merguje sa CarDirectio
    # CarLoc = np.zeros(shape=(9,18),dtype=int)
    for i in range(0,8):
        for y in range(0,17):
            CarLoc[i][y]=0
    for index in range(0,aindx):
        #CarLocation[CarArr[aindex].y // 100][CarArr[aindex].x // 100] = 1
        CarLoc[CarArr[index].y // 100][CarArr[index].x // 100] = 1




semafor = np.array([450, 140, 450, 440, 250, 300, 300, 350])
boje = ["Red", "Red", "Red", "Red"]
surface = pygamebg.open_window(1700, 900, "Traffic Jam Simulation")

##const matrix puteva koji postoje,mozda kasnije i nasumicni
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
RoadObj = np.zeros(shape=(8, 16), dtype=Road)  # Objekti puteva

CarLocation = np.zeros(shape=(8, 17), dtype=int)  # Lokacije auta u matrici

CarArr = np.zeros(shape=(br_car + 1), dtype=Car)  # Objekti automobila

CarDirection = np.zeros(shape=(br_car + 1), dtype=int)  # smer kretanja automobila

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
while Run:
    ciklus += 1
    surface.fill((0, 0, 255))
    for i in range(0, 7):
        for y in range(0, 15):
            if RoadArr[i][y] != 0:
                RoadObj[i][y].draw(surface)

    for i in range(0, 4, 2):
        pg.draw.circle(
            surface, pg.Color(boje[i // 2]), (semafor[i], semafor[i + 1]), 20
        )
    
    #CarArr[0].rotiraj("desno")
    
    osvezi_lokacije(auto_index,CarLocation)
    for aindex in range(0, auto_index ):
        CarArr[aindex].draw(surface)
        # print("PRVI")
        # for i in CarLocation:
        #     print(i)
        # CarLocation[CarArr[aindex].y // 100][CarArr[aindex].x // 100] = 1
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
                    CarArr[aindex].x = 100  # Teleportacija, prvo ispraznimo polje pa se prebacimo,ako je zauzeto
                #                    
                    """ if (
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

    if ciklus > 500:
        ciklus = 0
        if boja == 0:
            boje[0] = pg.Color("Green")
            boja = 1
        else:
            boje[0] = pg.Color("Red")
            boja = 0
    pg.display.update()

    # gasenje programa na ESC
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                Run = False
                pg.quit()
