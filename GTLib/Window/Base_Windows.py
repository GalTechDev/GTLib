import pygame as pg
import sys
from ..Tools.function import void
from .Menu import *
import asyncio


class Base:
    def __init__(self, size: tuple, fps:int = 60):
        pg.init()
        
        self.size = size
        self.screen = pg.display.set_mode(size, flags=pg.DOUBLEBUF)

        self.fps = fps
        self.clock = pg.time.Clock()

        self.dt = 0.0

        self.menu = []

        self.custom_update = [void]
        self.custom_event = [void]
        self.custom_draw = [void]

    def drop_menu(self, menu: Menu):
        """
        Remove from called Menu a gived menu\n
        Raise Exeption if not called
        """
        layer = self.get_layer(menu)
        if layer == -1:
            raise Exception("The gived menu is not found, unable to drop it")
        else:
            self.menu.pop(layer)


    def call_menu(self, menu: Menu, layer: int = -1):
        self.menu.insert(layer, menu)

    def switch_menu(self, layer1: int, layer2: int):
        self.menu[layer1], self.menu[layer2] = self.menu[layer2], self.menu[layer1]

    def switch_menu_layer(self, menu_1: Menu, menu_2: Menu):
        layer_1 = self.get_layer(menu_1)
        layer_2 = self.get_layer(menu_2)
        if layer_1 == -1 or layer_2 == -1:
            raise Exception("The given menu are not found, unable to switch them")
        
        self.switch_menu(self.get_layer(menu_1), self.get_layer(menu_2))

    def get_menu(self, layer: int):
        """
        Return the menu of at the gived layer\n
        Raise IndexError if not found
        """
        return self.menu[layer]

    def get_layer(self, menu: Menu):
        """
        Return the layer (or the index) of a given menu\n
        Return -1 if not found
        """
        for i, m in enumerate(self.menu):
            if m == menu:
                return i
        return -1

    def update(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func
        
        #update        
        [f() for f in self.custom_update]
        for m in self.menu:
            m.update()
        pg.display.flip()
        self.dt = self.clock.tick(self.fps) * 0.001

        return add_custom

    async def draw(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func

        self.screen.fill('black')
        
        #update        
        [f() for f in self.custom_update]
        for m in self.menu:
            m.draw(self.screen)

        return add_custom

    def event(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_event.append(func)
            return func
        
        #event
        for e in pg.event.get():
            [f(e) for f in self.custom_event]
            for m in self.menu:
                m.event(e)

        return add_custom

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()