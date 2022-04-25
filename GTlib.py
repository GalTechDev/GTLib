from ast import List
import pygame

FONT = pygame.font.Font(None, 32)
COLOR_TEXT = pygame.Color('floralwhite')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class square(pygame.sprite.Sprite):
    def __init__(self,x,y,color,size_x,size_y):
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
        self.image.fill(pygame.Color(self.color))

    def get_json(self):
        return {"x":self.rect.x,"y":self.rect.y,"color":self.color,"size_x":self.size_x,"size_y":self.size_y}


class square_boutton:
    def __init__(self,ref,x,y,color,border_color,text_color,size_x,size_y,text):
        self.group_sprite = pygame.sprite.Group()
        self.ref=ref
        self.color=color
        self.border_color=border_color
        self.text_color=text_color
        self.out_square=square(x,y,border_color[0],size_x,size_y)
        self.in_square=square(x+1,y+1,color[0],size_x-2,size_y-2)
        self.text=Text(x+size_y//2,y+3,size_x,size_y,text,"",text_color[0])
        self.group_sprite.add(self.out_square)
        self.group_sprite.add(self.in_square)
        self.group_sprite.add(self.text.group_sprite)

    def sub_event(self,event=[]):
        if self.in_square.rect.collidepoint(pygame.mouse.get_pos()):
            self.in_square.color=self.color[1]
            self.in_square.update()
        elif self.in_square.color==self.color[1]:
            self.in_square.color=self.color[0]
            self.in_square.update()

    def is_touching_rect(self,sprit):
        return self.out_square.rect.colliderect(sprit.rect)

    def is_touching_point(self,pos):
        return self.out_square.rect.collidepoint(pos)

    def update(self):
        self.group_sprite.update()

    def kill(self):
        self.out_square.kill()
        self.in_square.kill()
        self.text.kill()

class menu_deroulant:
    def __init__(self,bouton:square_boutton, autogen=True, list=[]):
        self.group_sprite=pygame.sprite.Group()
        self.bouton=bouton
        #self.bg=square(self.bouton.out_square.rect.x,self.bouton.out_square.rect.y+self.bouton.out_square.size_y-1,"blue",self.bouton.out_square.size_x,1)
        self.auto=autogen
        self.list=[]
        self.ref=1
        self.show=True
        if not autogen:
            for element in list:
                self.ajout(element)
        else:
            self.autogen(list)

        self.group_sprite.add(self.bouton.group_sprite)
        self.show_change()

    def autogen(self,list):
        self.next_x=self.bouton.out_square.rect.x
        self.next_y=self.bouton.out_square.rect.y+self.bouton.out_square.size_y
        for element in list:
            self.ajout(square_boutton(self.ref,self.next_x,self.next_y,element[0],element[1],element[2],element[3],element[4],element[5]))
            self.next_x=self.list[-1].out_square.rect.x
            self.next_y=self.list[-1].out_square.rect.y+self.list[-1].out_square.size_y
            #self.bg.size_y+=self.list[-1].out_square.size_y
            print(self.list[-1].out_square.size_y)

    def ajout(self,element):
        self.list.append(element)
        self.group_sprite.add(self.list[-1].group_sprite)

    def remove(self,ref):
        for element in self.list:
            if element.ref==ref:
                element.kill()
                self.list.remove(element)

    def is_touching_menu(self, pos):
        for menu in self.list:
            if menu.is_touching_point(pos):
                return True
        return False

    def show_change(self):
        if not self.show:
            self.show=True
            for element in self.list:
                self.group_sprite.add(element.group_sprite)
        else:
            self.show=False  
            for element in self.list:
                self.group_sprite.remove(element.group_sprite)


    def sub_event(self,events):
        self.bouton.sub_event(events)
        for element in self.list:
            element.sub_event(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.bouton.is_touching_point(pygame.mouse.get_pos()):
                        self.show_change()
                else:
                    self.show=True
                    self.show_change()

    def draw(self,screen):
        self.group_sprite.draw(screen) 
                  
    
    def blit_text(self,screen):
        screen.blit(self.bouton.text.txt_surface, self.bouton.text.rect)
        for bouton in self.list:
            screen.blit(bouton.text.txt_surface, bouton.text.rect)


class menu_bouton(pygame.sprite.Sprite):
    def __init__(self,ref,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.ref = ref
        if not type(self.ref)==type(''):
            self.image = ref
        else:
            self.image = pygame.image.load(f"asset/image/{self.ref}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.scale = scale
        self.image_size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.image_size[0]//self.scale, self.image_size[1]//self.scale))

    def change_image(self,ref):
        self.ref=ref
        self.image = pygame.image.load(f"Image/{self.ref}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]//self.scale, self.image.get_size()[1]//self.scale))

class Image(pygame.sprite.Sprite):
    def __init__(self,x,y,ref):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ref)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#a revoir

class InputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, inactive_color, active_color,font=FONT, min_char=0 ,max_char=None,text='',titre='',show_valide=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite = []
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactive_color
        self.text_color = active_color
        self.text = text
        self.show_valid = show_valide
        self.min_char = min_char
        self.max_char = max_char
        self.txt_surface = font.render(text, True, self.color)
        self.txt_pseudo_surface = font.render(titre, True, self.text_color)
        self.active = False
        if self.show_valid:
            self.valide_bouton = menu_bouton("Menu/V Square Button",625,220,4)
            self.list_sprite.append(self.valide_bouton)
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_color if self.active else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.text = str(pyperclip.paste())
                    if self.max_char==None:
                        self.text += event.unicode
                    elif len(self.text)<self.max_char:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
        if self.max_char==None:
            self.update()

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        screen.blit(self.txt_pseudo_surface, (self.rect.x+25, self.rect.y-50))
        
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def kill(self):
        for sprite in self.list_sprite:
            sprite.kill()


class Text():
    def __init__(self, x, y, w, h, text, data="", color="White", font=FONT):
        self.group_sprite = pygame.sprite.Group()
        self.list_sprite=[]
        self.FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.data = data
        self.text = text
        self.font = font
        self.txt_surface = FONT.render(self.text, True, self.color)
        for sprite in self.list_sprite:
            self.group_sprite.add(sprite)
        

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        #pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def kill(self):
        for sprite in self.list_sprite:
            sprite.kill()