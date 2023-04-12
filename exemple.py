import UI
from Window import *
import pygame as pg

app = Window.Window(show_fps=True)

@app.update()
def test_update():
    pass

@app.event()
def test_event(event):
    pass

app.run()