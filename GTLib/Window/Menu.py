import pygame as pg
from ..Tools.function import void

class Menu:
    def __init__(self) -> None:
        self.objects = []

        self.custom_update = [void]
        self.custom_event = [void]

    def add_sprite():
        pass

    def remove_sprite():
        pass

    def draw(self, screen):
        for object in self.objects:
            object.blit(screen, self.surface)

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

    def event(self, events):
        #decorator for custom update
        def add_custom(func):
            self.custom_event.append(func)
            return func
        
        #event
        [f(events) for f in self.custom_event]
        for object in self.objects:
            object.event(events)