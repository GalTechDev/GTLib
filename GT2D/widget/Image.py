import pygame
from .Sprite import Sprite

class Image(Sprite):
    def __init__(self, position: tuple[int,int], path: str, size: tuple[int,int]=None, rotation: float=0, alpha: int=255):
        '''Simple way to manage image'''
        self.surface = pygame.Surface((0,0))
        Sprite.__init__(self,position,(0,0),rotation,alpha)
        self.set_path(path)
        self.load_image()
        if not size==None:
            self.set_size(size)

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def load_image(self):
        pos=(self.rect.x,self.rect.y)
        self.surface = pygame.image.load(self.path)
        self.set_pos(pos)
        

    def draw(self, screen):
        self.blit(screen, self.surface) #pygame.transform.scale(self.surface, self.get_size()