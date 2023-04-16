import GTLib as gt
import pygame as pg

app = gt.Advanced(size=(800,800), fps=120, show_fps=True)

menu1 = gt.Menu()

app.call_menu(menu1)

@app.event()
def switch_fps(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_F3:
        app.show_fps(not app.fps_enable)

app.run()