import pygame
from .Sprite import Sprite
from .Square import Square
from .Text import Text
from ..tool import relative_mouse_pos

class Button(Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], square: Square, text: Text = None, rotation: float = 0, alpha: int = 255, color_hover=None,color_clic=None):
        self.square = square
        self.text = text
        super().__init__(position, size, rotation, alpha)
        self.square_color_n = self.square.color
        self.square_color_h = color_hover
        self.square_color_c = color_clic
        self.square.rect.center=self.rect.center
        if not self.text==None:
            self.text.rect.center=self.rect.center

        self.clicked = False

    def set_pos(self,pos):
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.square.rect.center=self.rect.center
        if not self.text==None:
            self.text.rect.center=self.rect.center

    def event(self, events):          
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                self.clicked = False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if self.collidepoint(relative_mouse_pos(pygame.display.get_window_size())):
                    self.clicked = True
        if self.clicked:
            self.square.set_color(self.square_color_c if not self.square_color_c is None else self.square_color_n)
        elif self.collidepoint(relative_mouse_pos(pygame.display.get_window_size())):
            self.square.set_color(self.square_color_h if not self.square_color_h is None else self.square_color_n)
        else:
            self.square.set_color(self.square_color_n)


    def draw(self, screen):
        self.square.draw(screen)
        if not self.text==None:
            self.text.draw(screen)
        