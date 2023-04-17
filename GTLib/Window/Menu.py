import pygame as pg
from ..Tools.function import void

class Menu:
    def __init__(self) -> None:
        self.objects = []

        self.custom_update = [void]
        self.custom_event = [void]

    def add_sprite(self, sprite):
        self.objects.append(sprite)

    def remove_sprite(self, sprite):
        self.objects.remove(sprite)

    def draw(self, screen):
        for object in self.objects:
            object.draw(screen)

    def update(self):
        #decorator for custom update
        def add_custom(func):
            self.custom_update.append(func)
            return func
        
        #update        
        [f() for f in self.custom_update]
        for object in self.objects:
            object.update()

        return add_custom

    def event(self, events=None):
        #decorator for custom update
        def add_custom(func):
            self.custom_event.append(func)
            return func
        
        #event
        if events!=None:
            [f(events) for f in self.custom_event]
            for object in self.objects:
                object.event(events)

        return add_custom