import pygame
from .Sprite import Sprite
from .Square import Square
from .. tool import relative_mouse_pos

class Cursor(Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], nb_pos=1,rotation: float = 0, alpha: int = 255, vertical=False, horizontal=False):
        super().__init__(position, size, rotation, alpha)

        self.square = Square(position=position,size=(size[0],size[1]//nb_pos))
        self.limit_y = (size[1]//nb_pos)*nb_pos
        self.limit_x = (size[0]//nb_pos)*nb_pos
        self.index=0
        self.nb_pos = nb_pos
        self.vertical = vertical
        self.horizontal = horizontal
        if self.horizontal:
            self.square.rect.centerx=self.rect.centerx
        if self.vertical:
            self.square.rect.centery=self.rect.centery
        self.clicked = False
        self.org_mouse = None

        self.set_index(0)

    def get_index(self):
        return self.index

    def get_stat(self):
        #print(self.square.rect.y-self.rect.y, self.rect.h-self.square.rect.h)
        #print(self.val_x, self.val_y)
        return [self.square.rect.y-self.rect.y, self.rect.h-self.square.rect.h]

    def set_index(self,index):
        self.index=index
        if self.horizontal:
            self.square.rect.x = self.rect.x+index*self.square.get_size()[0]
        if self.vertical:
            self.square.rect.y = self.rect.y+index*self.square.get_size()[1]

    def event(self, events):
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                self.clicked = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.collidepoint(relative_mouse_pos(pygame.display.get_window_size())):
                        self.org_mouse=relative_mouse_pos(pygame.display.get_window_size())
                        self.clicked = True
                elif event.button==4:
                    self.set_index(self.get_index()-1 if self.get_index()>0 else 0)
                elif event.button==5:
                    self.set_index(self.get_index()+1 if self.get_index()<self.nb_pos-1 else self.nb_pos-1)
        if self.clicked:
            if self.vertical:
                self.square.rect.y += relative_mouse_pos(pygame.display.get_window_size())[1]-self.org_mouse[1]
            if self.horizontal:
                self.square.rect.x += relative_mouse_pos(pygame.display.get_window_size())[0]-self.org_mouse[0]
            self.org_mouse=relative_mouse_pos(pygame.display.get_window_size())

        if self.square.rect.y < self.rect.y:
            self.square.rect.y = self.rect.y
        elif self.square.rect.y > self.rect.y+self.limit_y-self.square.rect.h:
            self.square.rect.y = self.rect.y+self.limit_y-self.square.rect.h

        if self.square.rect.x < self.rect.x:
            self.square.rect.x = self.rect.x
        elif self.square.rect.x > self.rect.x+self.rect.w-self.square.rect.w:
            self.square.rect.x = self.rect.x+self.rect.w-self.square.rect.w

        self.index=(self.square.rect.y-self.rect.y)//(self.rect.h//self.nb_pos)
        
        

    
    def draw(self, screen):
        self.square.draw(screen)
        pygame.draw.rect(screen, "white", self.rect, 2)