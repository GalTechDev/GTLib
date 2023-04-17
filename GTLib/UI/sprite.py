import pygame as pg
from ..Tools.function import void

class Sprite:
    def __init__(self, position: tuple[int,int], size: tuple[int,int], rotation: float=0, alpha: int=255):       
        self.set_surface(size,position)
        self.set_rotation(rotation) 
        self.set_alpha(alpha)

        self.custom_update = [void]
        self.custom_event = [void]

    def set_surface(self, size: tuple[int,int], position: tuple[int,int]=(0,0)):
        self.surface = pg.Surface(size,pg.SRCALPHA,32) 
        self.set_pos(position)

    def set_color_surface(self, color=None):
        if color==None:
            self.set_surface(self.get_size(),self.get_pos())
        else:
            self.surface.fill(color)

    def set_rotation(self, angle: float):
        self.angle = angle

    def get_rotation(self):
        return self.angle

    def set_pos(self, position: tuple[int,int], point = (0,0)):
        self.rect = self.surface.get_rect()
        self.rect.x = position[0] - point[0]
        self.rect.y = position[1] - point[1]

    def get_pos(self):
        return (self.rect.x,self.rect.y)

    def set_alpha(self, alpha: int):
        self.alpha = alpha
    
    def get_alpha(self):
        return self.alpha

    def set_size(self, size: tuple[int,int]):
        self.surface = pg.transform.scale(self.surface,size)
        self.rect.width = size[0]
        self.rect.height = size[1]
        

    def get_size(self):
        return self.surface.get_size()

    def blit(self, screen:pg.Surface, surface:pg.Surface,position=None):
        if self.angle!=0:
            new_surface = pg.transform.rotate(surface,self.angle)
        else:
            new_surface = surface
        new_surface.set_alpha(self.alpha)
        
        screen.blit(new_surface, self.rect)

    def collidepoint(self,pos):
        return self.rect.collidepoint(pos)

    def colliderect(self,rect):
        return self.rect.colliderect(rect)

    def draw(self, screen):
        self.blit(screen, self.surface)

    def update(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func
        
        #update        
        [f() for f in self.custom_update]

        return add_custom

    def event(self, events):
        #decorator for custom update
        def add_custom(func):
            self.custom_event.append(func)
            return func
        
        #event
        [f(events) for f in self.custom_event]

        return add_custom

    def mask(self, size: tuple[int, int], focus_pos: tuple[int, int], focus_size:tuple[int, int]):
        mask_surface = pg.Surface(focus_size,pg.SRCALPHA,32)
        mask_surface.blit(self.surface, focus_pos)
        self.surface = pg.transform.scale(mask_surface,size)
        self.rect.size = size


class Group:
    def __init__(self):
        self.all_sprite = []

        self.custom_update = [void]
        self.custom_event = [void]
    
    def __len__(self):
        return len(self.all_sprite)

    def __getitem__(self, __i: int):
        return self.all_sprite[__i]

    def __str__(self) -> str:
        return str(self.all_sprite)

    def add(self, sprite):
        if not self.have(sprite):
            self.all_sprite.append(sprite)

    def remove(self, sprite):
        if self.have(sprite):
            self.all_sprite.remove(sprite)

    def index(self, sprite):
        return self.all_sprite.index(sprite)

    def pop(self, index=0):
        if index>=0 and index<len(self.all_sprite):
            self.all_sprite.pop(index)

    def have(self, sprite):
        return sprite in self.all_sprite

    def get_collidepoint(self,pos):
        collide=[]
        for sprite in self.all_sprite:
            if sprite.collidepoint(pos):
                collide.append(sprite)
        return collide

    def get_colliderect(self,rect):
        collide=[]
        for sprite in self.all_sprite:
            if sprite.colliderect(rect):
                collide.append(sprite)
        return collide
   
    def update(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func
        
        #update        
        [f() for f in self.custom_update]
        for sprite in self.all_sprite:
            sprite.update()

        return add_custom

    def event(self, events=None):
        #decorator for custom update
        def add_custom(func):
            self.custom_event.append(func)
            return func
        
        #event
        [f(events) for f in self.custom_event]
        for sprite in self.all_sprite:
            sprite.event(events)

        return add_custom

    def draw(self, screen):
        for sprite in self.all_sprite:
            sprite.draw(screen)

    def ev_up_dr(self, events, screen):
        for sprite in self.all_sprite:
            sprite.event(events)
            sprite.update()
            sprite.draw(screen)