import pygame as pg
import pygamebg

fps = 45

surface = pygamebg.open_window(400, 400, "Traffic Jam Simulation")

pg.draw.circle(surface, pg.Color("blue"), (200,200), 100)

pygamebg.wait_loop()