import pygame
import pyperclip
import sys

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
    pyperclip.paste

    COLOR_TEXT = pygame.Color('floralwhite')
    COLOR_TEXT_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_TEXT_ACTIVE = pygame.Color('dodgerblue2')
    BLACK = pygame.Color('black')
except:
    is_import(modules=["pygame","pyperclip"])


