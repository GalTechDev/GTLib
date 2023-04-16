import pygame as pg
from .sprite import Sprite


class Square(Sprite):
    def __init__(self, position: tuple[int,int], size: tuple[int,int], rotation: float=0, alpha: int=255 , color="black"):
        '''Make a simple square that include some methode.'''
        pg.sprite.Sprite.__init__(self)
        Sprite.__init__(self,position,size,rotation,alpha)

        self.set_color(color)

    def set_color(self,color):
        self.color = color
        self.surface.fill(pg.Color(self.color))

    def draw(self, screen):
        self.blit(screen, self.surface)

    def get_dic(self) -> dict:
        '''Return a dic with square information. Can be use to make json file.'''
        return {"x":self.rect.x,"y":self.rect.y,"color":self.color,"size_x":self.size_x,"size_y":self.size_y}

    def __str__(self) -> str:
        return f"Info of {self}:\nx: {self.rect.x} y: {self.rect.y}\nsize_w: {self.get_size()[0]} size_h: {self.get_size()[1]}\ncolor: {self.color}"