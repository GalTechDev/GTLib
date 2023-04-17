import GTLib as gt
import pygame as pg
import pygame.freetype as ft
import time
import random
import sys

WINDOWS_SIZE = (800,800)

app = gt.Advanced(size=WINDOWS_SIZE, fps=0, show_fps=True)



#jeu 
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

@jeu.event()
def back_menu(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        app.drop_menu(jeu)
        app.call_menu(menu_principal)

#menu principal
menu_principal = gt.Menu()

menu_principal.add_sprite(gt.Text((WINDOWS_SIZE[0]//2-100//2,20), (100,40), "G'OSU", color="red", font=ft.SysFont('Verdana', 40)))

@menu_principal.event()
def get_clic(events):
    if events.type == pg.MOUSEBUTTONDOWN and menu_principal.objects[0].collidepoint(pg.mouse.get_pos()):
        app.drop_menu(menu_principal)
        app.call_menu(jeu)


app.call_menu(menu_principal)

@app.event()
def switch_fps(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_F3:
        app.show_fps(not app.fps_enable)

@menu_principal.event()
def quit(event):
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()

@app.event()
def quit(event):
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()

app.run()