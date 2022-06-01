import pygame

class Player:
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = 2
        self.size = (20,20)
        self.rect = pygame.Rect((x,y),self.size)
        self.colour = (255,0,0)
        self.sprite = pygame.image.load("arrow.png")

    def move(self,x,y):
        self.x = self.x + x
        self.y = self.y + y
        self.rect = pygame.Rect((self.x,self.y),self.size)

    def get_center(self):
        center = (self.x + self.size[0]//2,self.y + self.size[1]//2)
        return center
