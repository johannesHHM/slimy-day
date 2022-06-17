import pygame,color

color = color.Color((170,0,170))

class Doodad():
    def __init__(self,x,y,animation_database):
        self.x = x
        self.y = y
        self.sprite = animation_database["idle"][1][0]
        self.sprite.set_colorkey(color.colorkey)

        self.animation_action = "idle"
        self.animation_ticker = 0
        self.animation_frame = 0
        self.animation_database = animation_database
        self.animation_data = self.animation_database["idle"]

    def blit(self,display):
        display.blit(self.sprite,(self.x,self.y))

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = 0
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)

class Flowers(Doodad):
    def __init__(self,x,y):
        super().__init__(x,y,{"idle": [[36,36,36,36],[pygame.image.load("images/doodads/flowers/0.png"),pygame.image.load("images/doodads/flowers/1.png"),pygame.image.load("images/doodads/flowers/0.png"),pygame.image.load("images/doodads/flowers/2.png")]]})
