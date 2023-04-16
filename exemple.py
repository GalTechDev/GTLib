import GTLib as gt
import pygame as pg

app = gt.Advanced(size=(800,800), fps=0, show_fps=True)

menu1 = gt.Menu()
carre_rouge = gt.UI.Square((10,10), (50,50), color="red")

menu1.add_sprite(carre_rouge)


app.call_menu(menu1)

@app.event()
def switch_fps(event):
    if event.type == pg.KEYDOWN and event.key == pg.K_F3:
        app.show_fps(not app.fps_enable)

@carre_rouge.update()
def upt_carre():
    carre_rouge.set_pos(pg.mouse.get_pos())


app.run()