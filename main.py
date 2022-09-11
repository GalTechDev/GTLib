import GTlib as gt

SCREEN = (1000,800)
gt.SCREEN = SCREEN

class Menu1(gt.Menu):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], rotation: float = 0, alpha: int = 255):
        super().__init__(position, size, rotation, alpha)

        self.square = gt.Square((0,0), (10,10))
        self.titre = gt.Text((50,50), (100,30), text="This is a text")
        self.inputtext = gt.InputBox((50,100), (100,30), text="tap here some text")
        self.all_sprits.add(self.square)
        self.all_sprits.add(self.titre)
        self.all_sprits.add(self.inputtext)

    def event(self, events):
        self.all_sprits.event(events)
        self.square.set_pos(gt.relative_mouse_pos(gt.SCREEN), gt.center)
        self.titre.set_pos(gt.relative_mouse_pos(gt.SCREEN))



root = gt.Window(SCREEN,SCREEN,"DEMO")
root.keep_win_proportion = False

root.call_menu(Menu1, (0,0), SCREEN)

root.run()