import pygame as pg
import pygame.freetype as ft
import sys

def _void(*args):
    pass

class Window:
    def __init__(self, show_fps=False):
        pg.init()
        self.screen = pg.display.set_mode((800,800), flags=pg.DOUBLEBUF)

        self.clock = pg.time.Clock()
        self.font = ft.SysFont('Verdana', 15)

        self.dt = 0.0
        if not show_fps:
            self.draw_fps = _void

        self.custom_update = [_void]
        self.custom_event = [_void]

    def update(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func
        
        #update        
        [f() for f in self.custom_update]
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

        return add_custom

    def draw_fps(self):
        fps = f'{self.clock.get_fps() :.0f} FPS'
        self.font.render_to(self.screen, (0, 0), text=fps, fgcolor='green', bgcolor='black')

    def draw(self):
        self.screen.fill('black')
        self.draw_fps()

    def event(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_event.append(func)
            return func
        
        #event
        for e in pg.event.get():
            [f(e) for f in self.custom_event]
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

        return add_custom

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = Window()
    app.run()