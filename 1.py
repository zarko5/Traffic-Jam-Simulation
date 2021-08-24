#! /bin/python3
import pygame as pg
import numpy as np
import random

# import pygame.mixer
# pg.init()
# pg.mixer.music.load("music1.ogg")
# pg.mixer.music.play(-1)

sirina = 1700
visina = 1000


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
    def __init__(self,tip):
        self.x = 0
        self.y = 0
        if(tip == "put" or tip == 1):
            self.image = pg.image.load("./put.png").convert_alpha()
            self.rotiraj("desno")
        
        elif(tip == "putv" or tip == 2):
            self.image = pg.image.load("./put.png").convert_alpha()
            self.rotiraj("gore")

        elif(tip == "skretanje" or tip == 3):
            self.image = pg.image.load("./skretanje.png").convert_alpha()
        
        elif(tip == "raskrsnica" or tip == 4):
            self.image = pg.image.load("./raskrsnica.png").convert_alpha()
        
        elif(tip == "T_put" or tip == 5):
            self.image = pg.image.load("./T_put.png").convert_alpha()
        
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def rotiraj(self,smer):
        if (smer == "gore" ):
            self.image = pg.transform.rotate(self.image,0) 
        elif (smer == "dole"):
            self.image = pg.transform.rotate(self.image,180)
        elif (smer == "levo"):
            self.image = pg.transform.rotate(self.image,90)
        elif (smer == "desno"):
            self.image = pg.transform.rotate(self.image,270)

class Semafor(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.boja = "Red"
    
    def draw(self,surface):
         pg.draw.circle(surface, pg.Color(self.boja), (self.x, self.y), 20)

    def promeni_boju(self):
        if self.boja == "Green":
            self.boja = "Red" 
        else: self.boja = "Green"


def osvezi_lokacije(aindx,CarLoc):  # Prolazi kroz sve aute i markira polja na kojima se nalaze kao zauzeta 
    for i in range(0,8):
        for y in range(0,17):
            CarLoc[i][y]=0
    for index in range(0,aindx):
        CarLoc[CarArr[index].y // 100][CarArr[index].x // 100] = 1
#    for index in br_semafora:#Menjamo polje na jedan samo ako je boja crvena plus semafor moze da se promeni samo ako je slobodno polje

def obradi_raskrsnice(matrica,obradi_rotacije):
    for i in range(0,7):
        for y in range(0,15):
            if(matrica[i][y]>2): break
            if(i == 0):
                 up = 0
            else: 
                up = matrica[i-1][y]
            if(i == 7):
                down = 0
            else: 
                down = matrica[i+1][y]
            if(y == 0):
                left = 0
            else:
                left = matrica[i][y-1]
            if(y == 15):
                right = 0
            else:
                right = matrica[i][y+1]
            if(up == 2 and down == 2 and left == 1 and right == 1):
                matrica[i][y] = 4
            elif(up >= 2 and left>0 and right>0):
                matrica[i][y] = 5
            elif(down >= 2 and left>0 and right>0):
                matrica[i][y] = 5
                if(obradi_rotacije):
                    RoadObj[i][y].rotiraj("dole")
            elif(up >= 2 and down >= 2 and left>0 ):
                matrica[i][y] = 5
                if(obradi_rotacije):
                    RoadObj[i][y].rotiraj("levo")
            elif(up >= 2 and down >= 2 and right>0):
                matrica[i][y] = 5
                if(obradi_rotacije):
                    RoadObj[i][y].rotiraj("desno")
            elif(up == 2 and left and matrica[i][y] == 1):
                matrica[i][y] = 3
            elif(up == 2 and right and matrica[i][y] == 1):
                matrica[i][y] = 3
                if(obradi_rotacije):
                    RoadObj[i][y].rotiraj("desno")
            elif(down == 2 and left and matrica[i][y] == 1):
                matrica[i][y] = 3
                if(obradi_rotacije):
                    RoadObj[i][y].rotiraj("levo")
            elif(down == 2 and right and matrica[i][y] == 1):
                matrica[i][y] = 3
                if(obradi_rotacije):
                    RoadObj[i][y].rotiraj("dole")
            

semafor = np.array([450, 140, 450, 440, 250, 300, 300, 350])#ovaj  array ce postati niz klasa nakon ubacivanja raskrsnica
boje = ["Red", "Red", "Red", "Red"]
#boje = []#Prazna lista + append kad se dodaje novi semafor, nakon sto se ubace raskrsnice

pg.init()
surface = pg.display.set_mode((sirina,visina))
pg.display.set_caption("Traffic Jam Simulation")


##const matrix puteva koji postoje,mozda kasnije i nasumicni
# Horizontalan put - 1
# Vertikalan put - 2
# Skretanje - 3
# Raskrsnica - 4
# T_put - 5
RoadArr = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 2, 1, 1, 0, 0, 2, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
]
obradi_raskrsnice(RoadArr,0)

##
RoadObj = np.zeros(shape=(8, 16), dtype=Road)  # Objekti puteva

CarLocation = np.zeros(shape=(8, 17), dtype=int)  # Lokacije auta u matrici

CarArr = np.zeros(shape=(br_car + 1), dtype=Car)  # Objekti automobila

CarDirection = np.zeros(shape=(br_car + 1), dtype=int)  # smer kretanja automobila

semafori = np.zeros(shape=(8,17),dtype=Semafor)

auto_index = 0  # ovo treba promenu kako bi uvek bio ispunjen broj automobila br_car, samo se generisu na random lokacijama,
for i in range(0, 8):
    for y in range(0, 15):
        if RoadArr[i][y] == 1:
            RoadObj[i][y] = Road(1)
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
            #RoadObj[i][y].image = pg.transform.rotate(RoadObj[i][y].image, 90)
            if round(random.random()) and auto_index <= br_car:
                CarLocation[i][y] = 1
                CarDirection[auto_index] = 0
                CarArr[auto_index] = Car()
                CarArr[auto_index].x = y * 100 + 100
                CarArr[auto_index].y = i * 100 + 130
                auto_index += 1
        elif RoadArr[i][y] == 2: # Uspravan put
            RoadObj[i][y] = Road(2)
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
        elif RoadArr[i][y] == 3: # Skretanje 
            RoadObj[i][y] = Road(3)
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
        elif RoadArr[i][y] == 4: # Raskrsnica 
            RoadObj[i][y] = Road(4)
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
        elif RoadArr[i][y] == 5: # T_put
            RoadObj[i][y] = Road(5) 
            RoadObj[i][y].y = i * 100 + 100
            RoadObj[i][y].x = y * 100 + 100
obradi_raskrsnice(RoadArr,1)

boja = 0
Run = True
ciklus = 0
random.seed(23617282344)#PRNG eksperiment
while Run:
    ciklus += 1
    surface.fill((0, 0, 255))
    for i in range(0, 8):
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
