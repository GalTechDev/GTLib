
import pygame
import pyperclip
import sys
import PIL.Image
import urllib.request
import json


class MissingImport(Exception):
    pass
        
def is_import(module: str=None,modules: list=[]):
    for mod in modules:
        if not mod in sys.modules:
            raise MissingImport(f"{mod} not imported")
    if not module==None:
        if not module in sys.modules:
            raise MissingImport(f"{module} not imported")
    return True

try:
    pygame.init()
    FONT = pygame.font.SysFont(None, 32)
    COLOR_TEXT = pygame.Color('floralwhite')
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
except:
    is_import(modules=["pygame","pyperclip"])

global SCREEN
SCREEN = None
FPS = 60
all_groupe = []

class Window:
    def __init__(self,window_size,screen_resolution,title:str="pygame window"):

        global SCREEN
        SCREEN=screen_resolution

        # PARAMETER
        self.screen = pygame.Surface(SCREEN)
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        self.window = pygame.display.set_mode(window_size, flags,6) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()
        self.set_title(title)
        self.keep_screen_proportion = True
        self.keep_win_proportion = True

        # GROUPS
        self.active_menu = Group()
        # RUNNING
        self.is_running=True

        # OBJECTS
        self.background = Square(position=(0,0),size=SCREEN, color="black")
        
    def set_background_color(self,new_color):
        self.background.set_color(new_color)

    def set_title(self, new_title):
        pygame.display.set_caption(new_title)

    def call_menu(self, menu, *args):
        self.active_menu.add(menu(*args))

    def close_menu(self, menu):
        self.active_menu.remove(menu)

    #Sys fonction

    def run(self):
        '''WinLoop'''
        while self.is_running:
            self.clock.tick(FPS)
            self.sys_events()
            self.update()
            if self.is_running:
                self.draw()

    def update(self):
        self.active_menu.update()
        if not self.background.get_size() == SCREEN:
            self.background.set_size(SCREEN)
    
    def sys_events(self):
        all_events = pygame.event.get()
        self.active_menu.event(all_events)

        self.events(events=all_events)
        if all_events==[]:
            pass

        else:
            for event in all_events:
                if event.type == pygame.QUIT:
                    self.is_running=False
                    pygame.quit()
                    
    def events(self,events):
        pass

    def draw(self):
        self.background.draw(self.screen)
        self.active_menu.draw(self.screen)

        #if self.menu_is_running:
        #    self.menu.group_main_menu.draw(self.screen)
        if self.keep_screen_proportion:
            win_size=pygame.display.get_window_size() #800x800 1000x900 1000-800 900-800 200 100
            dif=min(win_size[0]-SCREEN[0],win_size[1]-SCREEN[1])
            win_size=(SCREEN[0]+dif,SCREEN[1]+dif)
            self.window.blit(pygame.transform.scale(self.screen,win_size),(0,0))
            if self.keep_win_proportion and not pygame.display.get_window_size()==win_size:
                pygame.display.set_mode(win_size, pygame.RESIZABLE)
        else:
            self.window.blit(pygame.transform.scale(self.screen,pygame.display.get_window_size()),(0,0))
        pygame.display.flip()

class Sprite:

    def __init__(self, position: tuple[int,int], size: tuple[int,int], rotation: float=0, alpha: int=255):
        self.set_surface(size,position)
        self.set_rotation(rotation) 
        self.set_alpha(alpha)

    def set_surface(self, size: tuple[int,int], position: tuple[int,int]=(0,0)):
        self.surface = pygame.Surface(size,pygame.SRCALPHA,32) 
        self.set_pos(position)

    def set_rotation(self, angle: float):
        self.angle = angle

    def get_rotation(self):
        return self.angle

    def set_pos(self, position: tuple[int,int]):
        self.rect = self.surface.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def get_pos(self):
        return (self.rect.x,self.rect.y)

    def set_alpha(self, alpha: int):
        self.alpha = alpha
    
    def get_alpha(self):
        return self.alpha

    def set_size(self, size: tuple[int,int]):
        self.surface = pygame.transform.scale(self.surface,size)

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
        pass

    def update(self):
        pass

    def event(self, events):
        pass

    def mask(self, size: tuple[int, int], focus_pos: tuple[int, int], focus_size:tuple[int, int]):
        mask_surface = pygame.Surface(focus_size,pygame.SRCALPHA,32)
        mask_surface.blit(self.surface, focus_pos)
        self.surface = pygame.transform.scale(mask_surface,size)
        self.rect.size = size


class Group:
    def __init__(self):
        all_groupe.append(self)
        self.all_sprite = []
    
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

    def event(self, events):
        for sprite in self.all_sprite:
            sprite.event(events)

    def update(self):
        for sprite in self.all_sprite:
            sprite.update()

    def draw(self, screen):
        for sprite in self.all_sprite:
            sprite.draw(screen)

    def ev_up_dr(self, events, screen):
        for sprite in self.all_sprite:
            sprite.event(events)
            sprite.update()
            sprite.draw(screen)
    
class Menu(Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], rotation: float = 0, alpha: int = 255):
        super().__init__(position, size, rotation, alpha)
        self.all_sprits=Group()

class Square(Sprite):
    def __init__(self, position: tuple[int,int], size: tuple[int,int], rotation: float=0, alpha: int=255 , color="black"):
        '''Make a simple square that include some methode.'''
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self,position,size,rotation,alpha)

        self.set_color(color)

    def set_color(self,color):
        self.color = color
        self.surface.fill(pygame.Color(self.color))

    def draw(self, screen):
        self.blit(screen, self.surface)

    def get_dic(self) -> dict:
        '''Return a dic with square information. Can be use to make json file.'''
        return {"x":self.rect.x,"y":self.rect.y,"color":self.color,"size_x":self.size_x,"size_y":self.size_y}

    def __str__(self) -> str:
        return f"Info of {self}:\nx: {self.rect.x} y: {self.rect.y}\nsize_w: {self.get_size()[0]} size_h: {self.get_size()[1]}\ncolor: {self.color}"

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

class InputBox(Sprite):
    def __init__(self, position: tuple[int,int], size: tuple[int,int]=(0,0), rotation: float=0, alpha: int=255, text: str='', inactive_color=COLOR_INACTIVE, active_color=COLOR_ACTIVE,font=FONT, min_char: int=0 ,max_char: int=None, default_text: str="", autolock: bool=False, continute_intup: bool=False):
        '''An input box object: Need event() and draw() fonction call to work correctly'''
        #pygame.sprite.Sprite.__init__(self)
        #self.surface = pygame.Surface(size)
        Sprite.__init__(self,position,size,rotation,alpha)
        
        self.active = False
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.color = inactive_color
        self.default_text = default_text
        self.text = Text(position, size, 0, 255, text)
        self.text.font = font

        self.autolock = autolock
        self.cont_input = continute_intup
        self.valide = False
        self.Backspace_pressed = False
        self.min_char = min_char
        self.max_char = max_char
        self.idx_cursor = 0
        
    def event(self, events:list):
        if not self.active and not self.valide:
            if self.get()=="":
                self.text.set_text(self.default_text)

        if self.Backspace_pressed and not self.valide:
            self.text.pop(len(self.text.get_text())-1)
            if not self.cont_input:
                self.Backspace_pressed=False

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.collidepoint(relative_mouse_pos(SCREEN)):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.active_color if self.active and not self.valide else self.inactive_color

            if event.type == pygame.KEYUP:
                self.Backspace_pressed = False

            if event.type == pygame.KEYDOWN:
                if self.active and not self.valide:
                    if event.key == pygame.K_BACKSPACE:
                        self.Backspace_pressed = True

                    elif event.key == pygame.K_RETURN:
                        if self.autolock:
                            self.valide = True
                            self.Backspace_pressed=False
                            self.color = self.inactive_color

                    elif event.key == pygame.K_LEFT:
                        if self.active and self.idx_cursor>0:
                            self.idx_cursor-=1

                    elif event.key == pygame.K_RIGHT:
                        if self.active and self.idx_cursor<len(self.get()):
                            self.idx_cursor+=1

                    else:
                        if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.text.add(str(pyperclip.paste()))
                        elif self.max_char == None:
                            self.text.add(event.unicode)
                        elif len(self.text.get_text())<self.max_char:
                            self.text.add(event.unicode)

    def update(self):
        '''Internal fonction, please don't use it.'''
        # Resize the box if the text is too long.
        if self.max_char == None:
            width = max(self.surface.get_size()[0], self.text.get_size()[1]+10)
            self.set_size((width,self.get_size()[1]))
        pos = self.get_pos()
        self.set_pos(pos)
        self.text.rect.centery = self.rect.centery

    def get(self) -> str:
        '''Return entered text.'''
        return self.text.get_text()

    def draw(self, screen):
        # Blit the text.
        new_surface = self.surface.copy()
        new_surface.fill("green")
        self.text.draw(new_surface)
        pygame.draw.rect(new_surface, self.color, self.rect, 2)
        self.blit(screen, new_surface)

class Text(Sprite):
    def __init__(self, position, size, text:str, rotation=0, alpha=255, color: str="white", font=FONT):
        '''A Text object: Need to call draw() intern fonction to work'''
        Sprite.__init__(self, position, size, rotation, alpha)
        
        self.color = color
        self.text = text
        self.font = font
        self.surface = self.font.render(self.text, True, self.color)
        self.surface.set_alpha()
        self.set_pos(position)

    def set_text(self, new_text: str):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)

    def get_text(self):
        return self.text

    def set_font(self, font):
        self.font = font

    def draw(self, screen):
        # Blit the text.
        self.blit(screen, self.surface)
        
    def add(self,ch):
        self.set_text(self.get_text()+ch)

    def pop(self, index=0):
        if index>=0 and index<len(self.text):
            self.set_text(self.text[:index]+self.text[index+1:])

class Bouton(Sprite):
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
                if self.collidepoint(relative_mouse_pos(SCREEN)):
                    self.clicked = True
        if self.clicked:
            self.square.set_color(self.square_color_c if not self.square_color_c is None else self.square_color_n)
        elif self.collidepoint(relative_mouse_pos(SCREEN)):
            self.square.set_color(self.square_color_h if not self.square_color_h is None else self.square_color_n)
        else:
            self.square.set_color(self.square_color_n)


    def draw(self, screen):
        self.square.draw(screen)
        if not self.text==None:
            self.text.draw(screen)
        
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
                if self.collidepoint(relative_mouse_pos(SCREEN)):
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
                    if self.collidepoint(relative_mouse_pos(SCREEN)):
                        self.org_mouse=relative_mouse_pos(SCREEN)
                        self.clicked = True
                elif event.button==4:
                    self.set_index(self.get_index()-1 if self.get_index()>0 else 0)
                elif event.button==5:
                    self.set_index(self.get_index()+1 if self.get_index()<self.nb_pos-1 else self.nb_pos-1)
        if self.clicked:
            if self.vertical:
                self.square.rect.y += relative_mouse_pos(SCREEN)[1]-self.org_mouse[1]
            if self.horizontal:
                self.square.rect.x += relative_mouse_pos(SCREEN)[0]-self.org_mouse[0]
            self.org_mouse=relative_mouse_pos(SCREEN)

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

class Gobject():
    def __init__(self,x,y,pixels: dict={},size=1, angle=0):
        """pixels a dict object build as : {"x,y":[r,g,b,a]}. imgtogobj() return the good object"""
        self.rotated_surface=pygame.Surface((10,10))
        self.surface=pygame.Surface((10,10))
        self.rect=self.surface.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.angle=angle
        self.pixels=pixels
        self.pixel_size=size
        self.image = []
        if pixels!={}:
            self.gen(pixels)

    def set_pos(self,pos:tuple):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def set_rotation(self,angle):
        self.angle = -angle
        self.rotated_surface=pygame.transform.rotate(self.surface,self.angle)

    def set_size(self,new_size):
        self.pixel_size = new_size
        self.gen(self.pixels)

    def gen(self,data):
        """data a dict object build as : {"x,y":[r,g,b,a]}"""
        self.pixels=data
        self.surface=pygame.Surface(((max([int(pixel.split(",")[0]) for pixel in data.keys()])-min([int(pixel.split(",")[0]) for pixel in data.keys()])),max([int(pixel.split(",")[1]) for pixel in data.keys()])-min([int(pixel.split(",")[1]) for pixel in data.keys()])))
        for pixel in data.keys():
            pixel = pixel.split(",")
            pixel = [int(coo) for coo in pixel]
            self.image.append(Square(pixel[0]*self.pixel_size+self.rect.x,pixel[1]*self.pixel_size+self.rect.y,(data[f"{pixel[0]},{pixel[1]}"][:-1]),self.pixel_size,self.pixel_size,data[f"{pixel[0]},{pixel[1]}"][-1]))
        self.set_rotation(-self.angle)

    def load(self,path):
        with open(path) as json_file:
            data = json.load(json_file)
        print(data)
        self.gen(data)

    def colliderect(self,sprite: pygame.sprite):
        for pixel in self.image:
            if pygame.sprite.collide_rect(pixel,sprite):
                return True
        return False

    def collidepoint(self, point: tuple | list):
        for pixel in self.image:
            if pixel.rect.collidepoint(point):
                return True
        return False

    def draw(self,screen):

        for pixel in self.image:
            pixel.draw(self.surface)
        self.set_rotation(-self.angle)
        #screen.blit(self.surface, self.rect)
        screen.blit(self.rotated_surface, self.rect)
        
def imgtogobj(image: PIL.Image=None, path=None, url=None):
    '''This fonction is using PIL library, image must be a PIL.Image object, url and path must point to .png file.'''
    if image is None:
        if path is None:
            if url is None:
                return
            else:
                urllib.request.urlretrieve(url,"tmp/temp_image.png")
                image = PIL.Image.open("tmp/temp_image.png")
        else:
            image = PIL.Image.open(path)
    img = image.convert('RGBA')
    size = img.size
    pixels={}
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = img.getpixel((x, y))
            pixels.update({f"{x},{y}":[r,g,b,a]})
    return pixels

def relative_mouse_pos(surface_size,surface_pos=(0,0)):
    return relative_pos(pygame.mouse.get_pos(),surface_pos,pygame.display.get_window_size(),surface_size)

def relative_pos(pos_on_parent,pos_child,screen_parent,screen_child):
    absolut_pos = pos_on_parent
    relative_pos = ((int(screen_child[0]/screen_parent[0]*absolut_pos[0]-pos_child[0]),int(screen_child[1]/screen_parent[1]*absolut_pos[1]-pos_child[1])))
    return relative_pos
