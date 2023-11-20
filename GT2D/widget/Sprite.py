import pygame

TOPLEFT = 7
TOPRIGHT = 9
CENTER = 5
BOTTOMLEFT = 1
BOTTOMRIGHT = 3

class Sprite:

    def __init__(self, position: tuple[int,int], size: tuple[int,int], rotation: float=0, alpha: int=255):
        self.set_surface(size,position)
        self.set_rotation(rotation) 
        self.set_alpha(alpha)

    def set_surface(self, size: tuple[int,int], position: tuple[int,int]=(0,0)):
        self.surface = pygame.Surface(size,pygame.SRCALPHA,32) 
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

    def set_pos(self, position: tuple[int,int], point = TOPLEFT):
        self.rect = self.surface.get_rect()
        if point==TOPLEFT:
            self.rect.topleft = position
        elif point==TOPRIGHT:
            self.rect.topright = position
        elif point==CENTER:
            self.rect.center = position
        elif point==BOTTOMLEFT:
            self.rect.bottomleft = position
        elif point==BOTTOMRIGHT:
            self.rect.bottomright = position

    def get_pos(self):
        return (self.rect.x,self.rect.y)

    def set_alpha(self, alpha: int):
        self.alpha = alpha
    
    def get_alpha(self):
        return self.alpha

    def set_size(self, size: tuple[int,int]):
        self.surface = pygame.transform.scale(self.surface,size)
        self.rect.width = size[0]
        self.rect.height = size[1]
        

    def get_size(self):
        return self.surface.get_size()

    def blit(self, screen:pygame.Surface, surface:pygame.Surface,position=None):
        if self.angle!=0:
            new_surface = pygame.transform.rotate(surface,self.angle)
        else:
            new_surface = surface
        new_surface.set_alpha(self.alpha)
        if position==None:
            screen.blit(new_surface, self.rect)
        else:
            screen.blit(new_surface, position)

    def collidepoint(self,pos):
        return self.rect.collidepoint(pos)

    def colliderect(self,rect):
        return self.rect.colliderect(rect)

    def draw(self, screen):
        self.blit(screen, self.surface)

    def update(self):
        pass

    def event(self, events):
        pass

    def mask(self, size: tuple[int, int], focus_pos: tuple[int, int], focus_size:tuple[int, int]):
        mask_surface = pygame.Surface(focus_size,pygame.SRCALPHA,32)
        mask_surface.blit(self.surface, focus_pos)
        self.surface = pygame.transform.scale(mask_surface,size)
        self.rect.size = size