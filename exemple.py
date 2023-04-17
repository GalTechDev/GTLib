import GTLib as gt
import pygame as pg
import time
import random

WINDOWS_SIZE = (800,800)

app = gt.Advanced(size=WINDOWS_SIZE, fps=0, show_fps=True)

class Jeu(gt.Menu):
    def __init__(self) -> None:
        super().__init__()

        self.timer = time.time()
        self.max_cible = 1
        self.square_size = 10

        self.update()


jeu = Jeu()

@jeu.update()
def gen_object():
    if len(jeu.objects) < jeu.max_cible:
        jeu.add_sprite(gt.Square((random.randint(0, WINDOWS_SIZE[0]-jeu.square_size), random.randint(0, WINDOWS_SIZE[1]-jeu.square_size)), (jeu.square_size, jeu.square_size), color=random.choice(["red", "yellow", "blue", "green"])))

@jeu.event()
def clic_object(event):
    if event.type == pg.MOUSEBUTTONDOWN and jeu.objects[0].collidepoint(pg.mouse.get_pos()):
        jeu.remove_sprite(jeu.objects[0])

#menu1.add_sprite(carre_rouge)
app.call_menu(jeu)

@app.event()
def switch_fps(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_F3:
        app.show_fps(not app.fps_enable)

app.run()