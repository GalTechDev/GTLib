import pygame as pg
import sys

def void(*args):
    pass

class Base:
    def __init__(self, size: tuple):
        pg.init()
        
        self.size = size
        self.screen = pg.display.set_mode(size, flags=pg.DOUBLEBUF)

        self.clock = pg.time.Clock()

        self.dt = 0.0

        self.custom_update = [void]
        self.custom_event = [void]

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

    def draw(self):
        self.screen.fill('black')

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