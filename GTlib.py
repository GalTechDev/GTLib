from asyncore import write
import pygame
import pyperclip
import sys


print("This Library need :\nimport pyperclip\nimport and init pygame before GTlib")
try:
    FONT = pygame.font.Font(None, 32)
    COLOR_TEXT = pygame.Color('floralwhite')
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
except:
    try:
        exec("import pygame")
        exec("pygame.init()")
    except:
        print("pygame not detected, please install pygame")
    try:
        exec("import pyperclip")
    except:
        print("pyperclip not detected, please install pyperclip")

        
            


def init(ref: int=0):
    '''Convert active file to a ready to code file for pygame dev'''
    dic={0:"base_file.py"}
    if ref not in dic.keys():
        ref=0
    base_code = dic[ref]
    path = sys.argv[0]
    with open(base_code, 'r') as base:
        with open(path, 'w') as file:
            file.write(base.read())

    print("Template Succesfuly applyed")


class Square(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, color, size_x:int, size_y:int):
        '''Make a simple square that include some methode.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_x,size_y))
        self.image.fill(pygame.Color(color))
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size_x = size_x
        self.size_y = size_y

    def update(self):
        '''Update sprite : rect, size and color.'''
        self.image.fill(pygame.Color(self.color))

    def __str__(self) -> str:
        return f"Info of {self}:\nx: {self.rect.x} y: {self.rect.y}\nsize_x: {self.size_x} size_y: {self.size_y}\ncolor: {self.color}"

    def get_dic(self) -> dict:
        '''Return a dic with square information. Can be use to make json file.'''
        return {"x":self.rect.x,"y":self.rect.y,"color":self.color,"size_x":self.size_x,"size_y":self.size_y}


class Image(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, ref:str):
        '''Simple way to manage image and rect'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ref)
        self.ref = ref
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def rescale(self,size_x,size_y):
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()


class InputBox(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, size_x:int, size_y:int,text: str='', inactive_color=COLOR_INACTIVE, active_color=COLOR_ACTIVE,font=FONT, min_char: int=0 ,max_char: int=None, default_text: str="", autolock: bool=False, continute_intup: bool=False):
        '''An input box object: Need intern event() and draw() fonction call to work correctly'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.active = False

        self.inactive_color = inactive_color
        self.active_color = active_color
        self.color = inactive_color
        self.default_text = default_text
        self.text = Text(self.rect.x, self.rect.y, self.size_x,self.size_y, text, hidden=True)
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
                self.text.text = self.default_text

        if self.Backspace_pressed and not self.valide:
            self.text.text = self.text.text[:-1]
            if not self.cont_input:
                self.Backspace_pressed=False

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
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
                            self.text.text = str(pyperclip.paste())
                        elif self.max_char == None:
                            self.text.text += event.unicode
                        elif len(self.text.text)<self.max_char:
                            self.text.text += event.unicode

            if self.max_char == None:
                self.update()
        # Re-render the text.
        self.text.txt_surface = self.text.font.render(self.text.text, True, self.color)

    def update(self):
        '''Internal fonction, please don't use it.'''
        # Resize the box if the text is too long.
        width = max(self.size_x, self.text.txt_surface.get_width()+10)
        self.rect.width = width

    def get(self) -> str:
        '''Return entered text.'''
        return self.text.text

    def draw(self, screen):
        # Blit the text.
        self.text.draw(screen)
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Text():
    def __init__(self, x:int, y:int, w:int, h:int, text:str, data: str="", color: str="White", font=FONT, hidden: bool=False):
        '''A Text object: Need to call draw() intern fonction to work'''
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.data = data
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.hidden = hidden

    def set_text(self, new_text: str):
        self.text = new_text
        self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        if not self.hidden:
            pygame.draw.rect(screen, self.color, self.rect, 2)


class Boutton(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, square:Square, text:Text, color_hover=None, color_clic=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((square.size_x,square.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.square = square
        self.square_color_n = self.square.color
        self.square_color_h = color_hover
        self.square_color_c = color_clic
        self.square.rect.x+=x
        self.square.rect.y+=y

        self.text = text
        self.text.rect.x+=x
        self.text.rect.y+=y

        self.clicked = False


    def event(self, events):          
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP:
                self.clicked = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True
        if self.clicked:
            self.square.color = self.square_color_c if not self.square_color_c is None else self.square_color_n
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            self.square.color = self.square_color_h if not self.square_color_h is None else self.square_color_n
        else:
            self.square.color = self.square_color_n


    def draw(self, screen):
        self.text.draw(screen)
        

class Checkbox(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int, check_str: str="X",color_bg="white", color_rect="black", color_check="black", is_check: bool=False, check_str_size: int=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.color_rect = color_rect

        self.color_bg = color_bg
        self.square = Square(x,y,self.color_bg,self.size,self.size)

        self.check_str_size = check_str_size if not check_str_size is None else self.size
        self.check = Text(x+size//10,y+size//15,size,size,check_str,color=color_check,font=pygame.font.Font(None,self.check_str_size), hidden=True)
        self.is_check = is_check

    def event(self, events):
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.is_check = not self.is_check

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_rect, self.rect, 2)
        if self.is_check:
            self.check.draw(screen)
        




