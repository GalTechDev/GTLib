import pygame
from .widget import Square
from .Groupe import Group
from . import tool

class Window:
    def __init__(self, window_size, screen_resolution, title: str="pygame window", fps: int=60):

        self.SCREEN=screen_resolution
        self.FPS = fps

        # PARAMETER
        self.screen = pygame.Surface(self.SCREEN)
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        self.window = pygame.display.set_mode(window_size, flags,6) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()
        self.set_title(title)
        self.keep_screen_proportion = True
        self.keep_win_proportion = True

        # GROUPS
        self.active_menu = Group()
        # RUNNING
        self.is_running=True

        # OBJECTS
        self.background = Square(position=(0,0),size=self.SCREEN, color="green")
        
    def set_background_color(self,new_color):
        self.background.set_color(new_color)

    def set_title(self, new_title):
        pygame.display.set_caption(new_title)

    def call_menu(self, menu, *args):
        self.active_menu.add(menu(*args))

    def close_menu(self, menu):
        self.active_menu.remove(menu)

    #Sys fonction

    def run(self):
        '''WinLoop'''
        while self.is_running:
            self.clock.tick(self.FPS)
            self.sys_events()
            self.update()
            if self.is_running:
                self.draw()

    def update(self):
        self.active_menu.update()
        if not self.background.get_size() == self.SCREEN:
            self.background.set_size(self.SCREEN)
    
    def sys_events(self):
        all_events = pygame.event.get()
        self.active_menu.event(all_events)

        self.events(events=all_events)
        if all_events==[]:
            pass

        else:
            for event in all_events:
                if event.type == pygame.QUIT:
                    self.is_running=False
                    pygame.quit()
                    
    def events(self,events):
        pass

    def draw(self):
        self.background.draw(self.screen)
        self.active_menu.draw(self.screen)

        #if self.menu_is_running:
        #    self.menu.group_main_menu.draw(self.screen)
        if self.keep_screen_proportion:
            win_size=pygame.display.get_window_size() #800x800 1000x900 1000-800 900-800 200 100
            dif=min(win_size[0]-self.SCREEN[0],win_size[1]-self.SCREEN[1])
            win_size=(self.SCREEN[0]+dif,self.SCREEN[1]+dif)
            self.window.blit(pygame.transform.scale(self.screen,win_size),(0,0))
            if self.keep_win_proportion and not pygame.display.get_window_size()==win_size:
                pygame.display.set_mode(win_size, pygame.RESIZABLE)
        else:
            self.window.blit(pygame.transform.scale(self.screen,pygame.display.get_window_size()),(0,0))
        pygame.display.flip()