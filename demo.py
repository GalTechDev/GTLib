import pygame
pygame.init()
import GTlib as gt

#----------------- Global constante ---------------

SCREEN = (800,800)
gt.SCREEN = SCREEN
FPS = 60

#---------------------- Class ---------------------


#----------------- Main Window Class --------------

class main_window:
    def __init__(self):
        # PARAMETER
        pygame.display.set_caption("title here")
        self.screen = pygame.Surface(SCREEN)
        self.window = pygame.display.set_mode(SCREEN, pygame.RESIZABLE) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()
        self.keep_screen_proportion = True
        self.keep_win_proportion = True
        # NETWORK

        # GROUPS
        self.all_sprites = gt.Group()

        # RUNNING
        self.is_running=True
        self.menu_is_running=True
        self.music_On=False

        # OBJECTS
        self.background = gt.Image((0,0),"Image/black.png")
        self.input = gt.InputBox((0,0),(100,30), text="test")
        self.all_sprites.add(self.background)
        self.all_sprites.add(self.input)

        # Call
        self.call_menu()
        

    def run(self):
        '''WinLoop'''
        while self.is_running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            if self.is_running:
                self.draw()

    def update(self):
        self.all_sprites.update()


    def call_menu(self):
        return
        #menu = class menu
        if self.music_On:
            pygame.mixer.music.load('path here')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0)
        else:
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.pause()

    
    def events(self):
        all_events = pygame.event.get()
        self.all_sprites.event(all_events)

        if all_events==[]:
            if self.menu_is_running:
                #self.menu.event()
                None

        else:
            if self.menu_is_running:
                #self.menu.event(all_events)
                None

            for event in all_events:

                if event.type == pygame.QUIT:
                    self.is_running=False
                    pygame.quit()

    def draw(self):
        self.all_sprites.draw(self.screen)
        #if self.menu_is_running:
        #    self.menu.group_main_menu.draw(self.screen)
        if self.keep_screen_proportion:
            win_size=pygame.display.get_window_size() #800x800 1000x900 1000-800 900-800 200 100
            dif=min(win_size[0]-SCREEN[0],win_size[1]-SCREEN[1])
            win_size=(SCREEN[0]+dif,SCREEN[1]+dif)
            self.window.blit(pygame.transform.scale(self.screen,win_size),(0,0))
            if self.keep_win_proportion and not pygame.display.get_window_size()==win_size:
                pygame.display.set_mode(win_size, pygame.RESIZABLE)
        else:
            self.window.blit(pygame.transform.scale(self.screen,pygame.display.get_window_size()),(0,0))
        pygame.display.flip()


test_mode=True
if __name__ == '__main__':
    if test_mode:
        root=main_window()
        root.run()
    else:
        try:
            root=main_window()
            root.run()
        except:
            None