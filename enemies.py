import pygame

class Slug:
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = 0.5
        self.size = (13,13)
        self.rect = pygame.Rect((x,y),self.size)
        self.colour = (0,255,0)

    def move(self,x,y):
        self.x = self.x + x
        self.y = self.y + y
        self.rect = pygame.Rect((self.x,self.y),self.size)

    def center(self):
        center = (self.x + self.size[0]//2,self.y + self.size[1]//2)
        return center

class Rat:
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = 1
        self.size = (11,11)
        self.rect = pygame.Rect((x,y),self.size)
        self.colour = (100,100,100)

    def move(self,x,y):
        self.x = self.x + x
        self.y = self.y + y
        self.rect = pygame.Rect((self.x,self.y),self.size)

    def center(self):
        center = (self.x + self.size[0]//2,self.y + self.size[1]//2)
        return center
