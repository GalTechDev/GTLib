from .Base_Windows import *

import pygame.freetype as ft

class Advanced(Base):
    def __init__(self, size: tuple, fps: int=60, show_fps: bool=True):
        super().__init__(size, fps)

        self.show_fps(show_fps)

    def show_fps(self, enable: bool):
        self.fps_enable = enable
        if not self.fps_enable:
            self.draw_fps = void
        else:
            self.draw_fps = self.draw_fps_func

    def draw_fps_func(self):
        font = ft.SysFont('Verdana', 15)
        fps = f'{self.clock.get_fps() :.0f} FPS'
        font.render_to(self.screen, (0, 0), text=fps, fgcolor='green', bgcolor='black')

    def draw(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func

        self.screen.fill('black')
        
        #update        
        [f() for f in self.custom_update]
        for m in self.menu:
            m.draw(self.screen)
        self.draw_fps()

if __name__ == '__main__':
    app = Advanced()
    app.run()