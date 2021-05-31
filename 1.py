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


class Road(object):  # klasa za puteve
    def __init__(self):
        self.image = pg.image.load("./road.png").convert_alpha()
        self.x = 0
        self.y = 0
        # self.image = pg.transform.rotate(self.image,270)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


def osvezi_lokacije():  # Prolaz kroz sva polja CarLocation i proverava da li ima automobila na njima, mozda bi mogao i da se merguje sa CarDirection
    # mzd da zerouje arr na pocetku i prolazi kroz sve aute, ima x i y , podeli ih sa 100?? i dobije indexe???, npr auto 1 na lokaciji
    print("d")


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

CarLocation = np.zeros(shape=(20, 20), dtype=int)  # Lokacije auta u matrici

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

    for aindex in range(0, auto_index - 1):
        if CarArr[aindex] != 0:
            CarArr[aindex].draw(surface)
            if CarArr[aindex].x < 1600 and CarArr[aindex].y < 800:
                CarLocation[CarArr[aindex].x // 100][CarArr[aindex].y // 100] = 1
                if (
                    CarDirection[aindex] == 0
                    and surface.get_at((CarArr[aindex].x + 75, CarArr[aindex].y))
                    != pg.Color("Red")
                    and surface.get_at((CarArr[aindex].x + 75, CarArr[aindex].y))
                    != pg.Color("Blue")
                ):
                    if (
                        not CarLocation[(CarArr[aindex].x) // 100 + 1][
                            (CarArr[aindex].y) // 100
                        ]
                        and CarArr[aindex].x // 100 + 1 < 16
                    ):  #
                        CarArr[aindex].x = CarArr[aindex].x + 1
                        CarLocation[CarArr[aindex].x // 100][
                            CarArr[aindex].y // 100
                        ] = 1
                        # provera da li je polje ispred zauzeto sa autom //100+1 ako nije kreni napred , markiraj svoje polje kao zauzeto ,ako si izaso iz polja markiraj prethodno
                        # polje kao zauzeto
                        if (
                            abs(CarArr[aindex].x // 100 - (CarArr[aindex].x - 1) // 100)
                            == 1
                        ):
                            CarLocation[(CarArr[aindex].x) // 100 - 1][
                                CarArr[aindex].y // 100
                            ] = 0
                    elif (
                        CarArr[aindex].x // 100 + 1 > 15
                        and CarLocation[1][(CarArr[aindex].y) // 100] == 0
                    ):
                        #         print(CarLocation[1][CarArr[aindex].y//100])
                        CarLocation[(CarArr[aindex].x) // 100][
                            CarArr[aindex].y // 100
                        ] = 0
                        CarArr[
                            aindex
                        ].x = 100  # Teleportacija, prvo ispraznimo polje pa se prebacimo,ako je zauzeto
                    #                    else :
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
                            )

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
