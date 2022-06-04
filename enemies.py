import pygame

class Enemy:
    def __init__(self,health,x,y,speed,size,color):
        self.health = health
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.rect = pygame.Rect((x,y),size)
        self.colour = color

    def collision_test(movement):
        t=0

    def center(self):
        center = (self.x + self.size[0]//2,self.y + self.size[1]//2)
        return center

    def move(self,movement):
        self.x = self.x + movement[0]
        self.y = self.y + movement[1]
        self.rect = pygame.Rect((self.x,self.y),self.size)

class Slug(Enemy):
    def __init__(self,x,y):
        super().__init__(3,x,y,0.5,(13,13),(0,255,0))

class Rat(Enemy):
    def __init__(self,x,y):
        super().__init__(3,x,y,1,(11,11),(100,100,100))
