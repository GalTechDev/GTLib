import GTLib as gt
import pygame as pg
import pygame.freetype as ft
import time
import random
import sys

WINDOWS_SIZE = (1920,1080)

app = gt.Advanced(size=WINDOWS_SIZE, fps=0, show_fps=True)



#jeu 
class Jeu(gt.Menu):
    def __init__(self) -> None:
        super().__init__()

        self.timer = time.time()
        self.cooldown = 10
        self.max_cible = 9
        self.square_size = 20

        self.i = 1

        self.pb = 0

        self.score = 0

        self.groupe_square = gt.UI.Group()
        self.add_sprite(self.groupe_square)
        self.update()

    def reset(self):
        self.timer = time.time()
        self.score = 0


jeu = Jeu()
score_text = gt.Text((WINDOWS_SIZE[0]-100,10), (100,40), "SCORE : 0", font=ft.SysFont('Verdana', 15))
time_text = gt.Text((WINDOWS_SIZE[0]-200,10), (100,40), "TIME : 10", font=ft.SysFont('Verdana', 15))
pb_text = gt.Text((WINDOWS_SIZE[0]-300,10), (100,40), "BEST : 0", font=ft.SysFont('Verdana', 15))
jeu.add_sprite(score_text)
jeu.add_sprite(time_text)
jeu.add_sprite(pb_text)

@jeu.update()
def gen_object():
    if len(jeu.groupe_square) < jeu.max_cible:
        jeu.groupe_square.add(gt.Text((random.randint(0, WINDOWS_SIZE[0]-jeu.square_size), random.randint(0, WINDOWS_SIZE[1]-jeu.square_size)), (jeu.square_size, jeu.square_size), text=str(jeu.i), font=ft.SysFont('Verdana', jeu.square_size) ,bgcolor=random.choice(["red", "blue", "green"])))
        jeu.i +=1
        if jeu.i > jeu.max_cible:
            jeu.i = 1
@jeu.update()
def check_time():
    if time.time() - jeu.timer > jeu.cooldown:
        if jeu.score > jeu.pb:
            jeu.pb = jeu.score
            pb_text.set_text(f"BEST : {jeu.pb}")
        jeu.reset()
        score_text.set_text(f"SCORE : {jeu.score}")
        app.drop_menu(jeu)
        app.call_menu(gameover_menu)
        gameover_menu.reset()
    
    time_text.set_text(f"TIME : {int(jeu.cooldown - (time.time()- jeu.timer))+1}")

@jeu.event()
def clic_object(event):
    if event.type == pg.MOUSEBUTTONDOWN and jeu.groupe_square[0].collidepoint(pg.mouse.get_pos()):
        jeu.groupe_square.remove(jeu.groupe_square[0])
        #jeu.cooldown -=0.1
        jeu.score+=1
        score_text.set_text(f"SCORE : {jeu.score}")
        jeu.timer+=1

@jeu.event()
def back_menu(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        jeu.reset()
        app.drop_menu(jeu)
        app.call_menu(menu_principal)


#eecran game over
class GameOver(gt.Menu):
    def __init__(self) -> None:
        super().__init__()
        self.timer = time.time()
        self.cooldown = 2

    def reset(self):
        self.timer = time.time()

gameover_menu = GameOver()
gameover_menu.add_sprite(gt.Text((WINDOWS_SIZE[0]//2-100//2,20), (100,40), "GAME OVER", fgcolor="red", font=ft.SysFont('Verdana', 40)))

@gameover_menu.update()
def check_for_end():
    if time.time() - gameover_menu.timer > gameover_menu.cooldown:
        app.drop_menu(gameover_menu)
        app.call_menu(menu_principal)


#menu principal
menu_principal = gt.Menu()

menu_principal.add_sprite(gt.Text((WINDOWS_SIZE[0]//2-100//2,20), (100,40), "G'OSU", fgcolor="pink", font=ft.SysFont('Verdana', 40)))

@menu_principal.event()
def get_clic(events):
    if events.type == pg.MOUSEBUTTONDOWN and menu_principal.objects[0].collidepoint(pg.mouse.get_pos()):
        app.drop_menu(menu_principal)
        app.call_menu(jeu)
        jeu.reset()
        score_text.set_text(f"SCORE : {jeu.score}")


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