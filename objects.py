import pygame,color

color = color.Color((170,0,170))

class Particle():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load("images/particles/leaf/0.png")
        self.sprite.set_colorkey(color.colorkey)
        self.rotation = 0

    def move(self,movement):
        self.x += movement[0]
        self.y += movement[1]
        print("x: {} y: {}",self.x,self.y)

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center

    def rotate(self,added_rotation):
        self.rotation += added_rotation

    def blit(self,display):
        display.blit(self.sprite,(self.x,self.y))
