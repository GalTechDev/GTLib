from .widget import Sprite
from .Groupe import Group

class Menu(Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], rotation: float = 0, alpha: int = 255):
        super().__init__(position, size, rotation, alpha)
        self.all_sprits=Group()

    def draw(self, screen):
        surface = self.surface.copy()
        self.all_sprits.draw(surface)
        self.blit(screen, surface)

    def event(self, events):
        self.all_sprits.event(events)

    def update(self):
        self.all_sprits.update()
