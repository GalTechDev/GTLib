from .Base_Windows import *

import pygame.freetype as ft

class Advanced(Base):
    def __init__(self, size: tuple, show_fps: bool=True):
        super().__init__(size)

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
        self.screen.fill('black')
        self.draw_fps()

if __name__ == '__main__':
    app = Advanced()
    app.run()