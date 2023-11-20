import pygame
from .Sprite import Sprite
from .Text import Text
from ..tool import relative_mouse_pos

class Checkbox(Sprite):
    def __init__(self, position, size: int, rotation, alpha, check_str: str="X",color_bg="white", color_rect="black", color_check="black", is_check: bool=False, check_str_size: int=None):
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self, position, size, rotation, alpha)
        
        self.color_rect = color_rect
        self.color_bg = color_bg

        self.check_str_size = check_str_size if not check_str_size is None else size
        self.check = Text((0,0),(size,size), 0, 255, check_str, color=color_check,font=pygame.font.Font(None,self.check_str_size))
        self.is_check = is_check

    def event(self, events):
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP:
                if self.collidepoint(relative_mouse_pos(pygame.display.get_window_size())):
                    self.is_check = not self.is_check

    def update(self):
        pos = self.get_pos()
        self.set_pos(pos)
        self.check.rect.centery = self.rect.centery
        self.check.rect.centerx = self.rect.centerx

    def draw(self, screen):
        new_surface = self.surface.copy()
        new_surface.fill(self.color_bg)
        if self.is_check:
            self.check.draw(new_surface)
        pygame.draw.rect(new_surface, self.color_rect, self.rect, 2)
        self.blit(screen, new_surface)