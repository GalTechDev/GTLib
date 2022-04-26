import pygame
pygame.init()
import GTlib as gt

#----------------- Global constante ---------------

SCREEN = (800,800)
FPS = 60

#---------------------- Class ---------------------


#----------------- Main Window Class --------------

class main_window:
    def __init__(self):
        # PARAMETER
        pygame.display.set_caption("title here")
        self.screen = pygame.display.set_mode(SCREEN) #pygame.FULLSCREEN
        self.clock = pygame.time.Clock()

        # NETWORK

        # GROUPS
        self.all_sprites = pygame.sprite.Group()

        # RUNNING
        self.is_running=True
        self.menu_is_running=True
        self.music_On=False

        # OBJECTS
        self.background = gt.Image(0,0,"Image/black.png")
        self.square = gt.Square(0,0,"blue",10,10)
        self.inputbox = gt.InputBox(10,10,200,30,default_text="Entrez du text")
        self.boutton = gt.boutton(10,100,gt.Square(0,0,"white",100,30),gt.Text(0,0,100,30,"Bonjour",hidden=True, color="black"))
        self.all_sprites.add(self.background)
        self.all_sprites.add(self.square)
        self.all_sprites.add(self.boutton.square)
        

        # Call
        self.call_menu()
        

    def run(self):
        '''WinLoop'''
        while self.is_running:
            self.clock.tick(FPS)
            self.events()
            self.update()
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
        self.square.rect = pygame.mouse.get_pos()
        self.inputbox.event(all_events)
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
                    pygame.quit()

    def draw(self):
        self.all_sprites.draw(self.screen) # actualise les sprites
        self.inputbox.draw(self.screen)
        self.boutton.draw(self.screen)
        #if self.menu_is_running:
        #    self.menu.group_main_menu.draw(self.screen)
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