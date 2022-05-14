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
        self.square = gt.Square(0,0,"blue",1,1)
        self.inputbox = gt.InputBox(10,10,200,30,default_text="Entrez du text")
        self.boutton = gt.Bouton(10,100,gt.Square(0,0,"white",100,30),gt.Text(0,0,100,30,"Bonjour",hidden=True, color="black",font=pygame.font.Font(None,32)), color_hover="green", color_clic="blue")
        self.check = gt.Checkbox(300,10,30,color_rect="blue")
        self.cursor = gt.Cursor(700,700,100,100,20,20,vertical=True,horizontal=True)
        self.text = gt.Text(0,0,100,30,"test")
        self.text.set_pos(y=200)
        self.all_sprites.add(self.background)
        self.card = gt.Gobject(0,0)
        self.card.load("C:/Users/Maxence/Pictures/test.gobj")
        
        

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
        self.boutton.event(all_events)
        self.inputbox.event(all_events)
        self.check.event(all_events)
        self.cursor.event(all_events)
        if not self.cursor.clicked:
            self.cursor.set_cursor(50,50)
            self.card.set_pos(pygame.mouse.get_pos())
        if all_events==[]:
            if self.menu_is_running:
                #self.menu.event()
                None

        else:
            if self.menu_is_running:
                #self.menu.event(all_events)
                None

            for event in all_events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.cursor.set_cursor(y=100)
                if event.type == pygame.QUIT:
                    pygame.quit()

    def draw(self):
        self.all_sprites.draw(self.screen) # actualise les sprites
        self.card.draw(self.screen)
        self.square.draw(self.screen)
        self.inputbox.draw(self.screen)
        self.boutton.draw(self.screen)
        self.check.draw(self.screen)
        self.cursor.draw(self.screen)
        self.text.draw(self.screen)
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