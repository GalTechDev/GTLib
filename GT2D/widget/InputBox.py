import pygame
from .Text import Text

class InputBox(Text):
    def __init__(self, position, size, text: str, rotation=0, alpha=255, color: str = "white", font=pygame.font.SysFont(None, 32)):
        super().__init__(position, size, text+"|", rotation, alpha, color, font)
        
        self.is_placeholder = False
        self.inx = -1

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.set_text(self.get_text()[:self.inx-1]+self.get_text()[self.inx:])
                elif event.key == pygame.K_LEFT:
                    if self.inx>-len(self.get_text()):
                        if self.inx!=-1:
                            txt = self.get_text()
                            txt = txt[:self.inx-1]+"|"+txt[self.inx-1:self.inx]+txt[self.inx+1:]
                            self.inx-=1
                        else:
                            txt = self.get_text()[:self.inx]
                            self.inx-=1
                            txt = txt[:self.inx+1]+"|"+txt[self.inx+1:]
                        
                        self.set_text(txt)
                        
                elif event.key == pygame.K_RIGHT:
                    if self.inx<-1:
                        if self.inx == -2:
                            txt = self.get_text()
                            txt = txt[:-2]+txt[-1:]+"|"
                            self.inx+=1
                            
                        elif self.inx!=-len(self.get_text()):
                            txt = self.get_text()
                            txt = txt[:self.inx]+txt[self.inx+1:self.inx+2]+"|"+txt[self.inx+2:]
                            self.inx+=1
                        
                        else:
                            txt = self.get_text()[1:2]+"|"+self.get_text()[2:]
                            self.inx+=1
                        
                        self.set_text(txt)


                else:
                    self.set_text(self.get_text()[:self.inx]+event.unicode+self.get_text()[self.inx:])