import pygame as pg
import pygame.freetype as ft
from .sprite import Sprite

ft.init()

class Text(Sprite):
    def __init__(self, position, size, text:str, rotation=0, alpha=255, fgcolor: str="white", bgcolor: str="black", font=ft.SysFont('Verdana', 15)):
        '''A Text object: Need to call draw() intern fonction to work'''
        Sprite.__init__(self, position, size, rotation, alpha)
        
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.text = text
        self.font = font
        self.set_text(text)
        self.surface.set_alpha(alpha)
        self.set_pos(position)

    def set_fgcolor(self, new_fgcolor):
        self.fgcolor = new_fgcolor

    def set_bgcolor(self, new_bgcolor):
        self.fgcolor = new_bgcolor

    def set_text(self, new_text: str):
        self.text = new_text
        self.surface = self.font.render(self.text, self.fgcolor, self.bgcolor)[0]
        
    def get_text(self):
        return self.text

    def set_font(self, font):
        self.font = font
        
    def add(self,ch):
        self.set_text(self.get_text()+ch)

    def pop(self, index=0):
        if index>=0 and index<len(self.text):
            self.set_text(self.text[:index]+self.text[index+1:])