import pygame

class Player:
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = 3
        self.size = (15,15)
        self.rect = pygame.Rect((x,y),self.size)
        self.colour = (255,0,0)
        self.sprite = pygame.image.load("player1.png")
        self.angle = 0
        self.invinc = 0

    def move(self,x,y):
        self.x = self.x + x
        self.y = self.y + y
        self.rect = pygame.Rect((self.x,self.y),self.size)

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center
