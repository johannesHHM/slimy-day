import pygame, color

color = color.Color((170,0,170))

class Terrain:
    def __init__(self,x,y,size,color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = pygame.Rect((x,y),size)

class Water(Terrain):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,(color.chineseblue))
        #self.sprite = pygame.image.load("")
        #self.sprite.set_colorkey(color.colorkey)
