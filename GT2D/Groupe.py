all_groupes = []

class Group:
    def __init__(self):
        all_groupes.append(self)
        self.all_sprite = []
    
    def __len__(self):
        return len(self.all_sprite)

    def __getitem__(self, __i: int):
        return self.all_sprite[__i]

    def __str__(self) -> str:
        return str(self.all_sprite)

    def add(self, sprite):
        if not self.have(sprite):
            self.all_sprite.append(sprite)

    def remove(self, sprite):
        if self.have(sprite):
            self.all_sprite.remove(sprite)

    def index(self, sprite):
        return self.all_sprite.index(sprite)

    def pop(self, index=0):
        if index>=0 and index<len(self.all_sprite):
            self.all_sprite.pop(index)

    def have(self, sprite):
        return sprite in self.all_sprite

    def get_collidepoint(self,pos):
        collide=[]
        for sprite in self.all_sprite:
            if sprite.collidepoint(pos):
                collide.append(sprite)
        return collide

    def get_colliderect(self,rect):
        collide=[]
        for sprite in self.all_sprite:
            if sprite.colliderect(rect):
                collide.append(sprite)
        return collide

    def event(self, events):
        for sprite in self.all_sprite:
            sprite.event(events)

    def update(self):
        for sprite in self.all_sprite:
            sprite.update()

    def draw(self, screen):
        for sprite in self.all_sprite:
            sprite.draw(screen)

    def ev_up_dr(self, events, screen):
        for sprite in self.all_sprite:
            sprite.event(events)
            sprite.update()
            sprite.draw(screen)