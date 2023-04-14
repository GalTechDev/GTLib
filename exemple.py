import UI
from Window.Advanced_Window import *
import pygame as pg

app = Advanced(size=(800,800), fps=0, show_fps=True)

@app.event()
def switch_fps(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_F3:
        app.show_fps(not app.fps_enable)

app.run()