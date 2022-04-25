from asyncore import write
import pygame
import pyperclip
import sys

for i in range(2):
    try:
        FONT = pygame.font.Font(None, 32)
        COLOR_TEXT = pygame.Color('floralwhite')
        COLOR_INACTIVE = pygame.Color('lightskyblue3')
        COLOR_ACTIVE = pygame.Color('dodgerblue2')
    except:
        exec("import pygame")
        exec("pygame.init()")
        print("Please import and init pygame before GTlib")

class init():
    def __init__(self):
        '''Convert active file to a ready to code file for pygame dev'''
        base_code = "base_file.py"
        path = sys.argv[0]
        with open('base_file.py', 'r') as base:
            with open(path, 'w') as file:
                file.write(base.read())


class square(pygame.sprite.Sprite):
    def __init__(self,x:int(),y:int(),color,size_x:int(),size_y:int()):
        '''Make a simple square that include some methode.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_x,size_y))
        self.image.fill(pygame.Color(color))
        self.color = color
        self.rect = self.image.get_rect()
        self.rect = (x,y)
        self.size_x = size_x
        self.size_y = size_y

    def update(self):
        '''Update sprite : rect, size and color.'''
        self.image.fill(pygame.Color(self.color))

    def get_dic(self) -> dict():
        '''Return a dic with square information. Can be use to make json file.'''
        return {"x":self.rect.x,"y":self.rect.y,"color":self.color,"size_x":self.size_x,"size_y":self.size_y}


class Image(pygame.sprite.Sprite):
    def __init__(self,x:int(),y:int(),ref:str()):
        '''Simple way to manage image and rect'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ref)
        self.rect = self.image.get_rect()
        self.rect = (x,y)


class InputBox(pygame.sprite.Sprite):
    def __init__(self, x:int(), y:int(), size_x:int(), size_y:int(),text='', inactive_color=COLOR_INACTIVE, active_color=COLOR_ACTIVE,font=FONT, min_char=0 ,max_char=None):
        '''An input box object: Need intern event() and draw() fonction call to work correctly'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size_x,size_y))
        self.rect = (x,y)
        self.size_x = size_x
        self.size_y = size_y
        self.active = False

        self.inactive_color = inactive_color
        self.active_color = active_color
        self.color = inactive_color
        self.text = Text(self.rect.x+5, self.rect.y+5, text)
        self.text.font = font

        self.valide = False
        self.min_char = min_char
        self.max_char = max_char
        self.text.txt_surface = self.text.font.render(self.text.text, True, self.text.color)
        
    def event(self, events:list()):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.active_color if self.active else self.inactive_color

            if event.type == pygame.KEYDOWN:
                if self.active and not self.valide:
                    if event.key == pygame.K_BACKSPACE:
                        self.text.text = self.text.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.valide = True
                    else:
                        if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.text.text = str(pyperclip.paste())
                        if self.max_char == None:
                            self.text.text += event.unicode
                        elif len(self.text.text)<self.max_char:
                            self.text.text += event.unicode
                    # Re-render the text.
                    self.text.txt_surface = self.text.font.render(self.text.text, True, self.color)
            if self.max_char == None:
                self.update()

    def update(self):
        '''Internal fonction, please don't use it.'''
        # Resize the box if the text is too long.
        width = max(self.size_x, self.text.txt_surface.get_width()+10)
        self.size_x = width

    def get(self) -> str():
        '''Return entered text.'''
        return self.text.text

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.text.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)



class Text():
    def __init__(self, x:int(), y:int(), w:int(), h:int(), text:str(), data="", color="White", font=FONT, hidden=False):
        '''A Text object: Need to call draw() intern fonction to work'''
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.data = data
        self.text = text
        self.font = font
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.hidden = hidden
        

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        if not self.hidden:
            pygame.draw.rect(screen, self.color, self.rect, 2)
