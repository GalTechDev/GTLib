import pygame as pg
import pygame.freetype as ft
from .sprite import Sprite

ft.init()

class Text(Sprite):
    def __init__(self, position, size, text:str, rotation=0, alpha=255, color: str="white", font=ft.SysFont('Verdana', 15)):
        '''A Text object: Need to call draw() intern fonction to work'''
        Sprite.__init__(self, position, size, rotation, alpha)
        
        self.color = color
        self.text = text
        self.font = font
        self.surface = self.font.render(self.text, self.color)[0]
        self.surface.set_alpha(alpha)
        self.set_pos(position)

    def set_text(self, new_text: str):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)
        
    def get_text(self):
        return self.text

    def set_font(self, font):
        self.font = font
        
    def add(self,ch):
        self.set_text(self.get_text()+ch)

    def pop(self, index=0):
        if index>=0 and index<len(self.text):
            self.set_text(self.text[:index]+self.text[index+1:])