import pygame, color
import objects

color = color.Color((170,0,170))

class Terrain:
    def __init__(self,x,y,size,color,type,particle_list):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.type = type
        self.rect = pygame.Rect((x,y),size)
        self.particle_list = particle_list

        self.animation_action = "idle"
        self.animation_ticker = 0
        self.animation_frame = 0

class Water(Terrain):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,(color.chineseblue))
        #self.sprite = pygame.image.load("")
        #self.sprite.set_colorkey(color.colorkey)
class Tree(Terrain):
    def __init__(self,x,y,particle_list):
        super().__init__(x,y,(25,31),color.chineseblue,"Tree",particle_list)
        self.sprite = pygame.image.load("images/tree/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)
        self.offput = (-2,-1)

        self.animation_database = {
          "idle": [[24,24,24,24],[pygame.image.load("images/tree/idle1/0.png"),pygame.image.load("images/tree/idle1/1.png"),pygame.image.load("images/tree/idle1/0.png"),pygame.image.load("images/tree/idle1/2.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("idle")

        self.particle_spawner = objects.ParticleSpawner(self.rect.left,self.rect.right,self.rect.top,self.rect.bottom,self.rect.bottom + 5,particle_list)

    def blit(self,display):
        sprite = self.sprite
        #if self.flip:
        #    sprite = pygame.transform.flip(sprite, True, False)
        #    sprite.set_colorkey(color.colorkey)
        display.blit(sprite,(self.x + self.offput[0],self.y + self.offput[1]))
        #pygame.draw.rect(display,self.color,self.rect)

    def action(self,action):
        if self.animation_action == action:
            pass
        else:
            if self.animation_ticker == 0:
                self.animation_action = action
                self.animation_data = self.animation_database[action]
                self.animation_ticker = 0
                self.animation_frame = 0

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = 0
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)

    def shake(self,position):
        self.particle_spawner

class Stone(Terrain):
    def __init__(self,x,y,particle_list):
        super().__init__(x,y,(34,17),color.chineseblue,"Stone",particle_list)
        self.sprite = pygame.image.load("images/stone/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)
        self.offput = (-2,-1)

        self.animation_database = {
          "idle": [[24,24,24,24],[pygame.image.load("images/stone/idle/0.png"),pygame.image.load("images/stone/idle/1.png"),pygame.image.load("images/stone/idle/2.png"),pygame.image.load("images/stone/idle/1.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("idle")

        #self.particle_spawner = objects.ParticleSpawner(self.rect.left,self.rect.right,self.rect.top,self.rect.bottom,self.rect.bottom + 5,particle_list)

    def blit(self,display):
        #if self.flip:
        #    sprite = pygame.transform.flip(sprite, True, False)
        #    sprite.set_colorkey(color.colorkey)
        display.blit(self.sprite,(self.x + self.offput[0],self.y + self.offput[1]))
        #pygame.draw.rect(display,self.color,self.rect)

    def action(self,action):
        if self.animation_action == action:
            pass
        else:
            if self.animation_ticker == 0:
                self.animation_action = action
                self.animation_data = self.animation_database[action]
                self.animation_ticker = 0
                self.animation_frame = 0

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = 0
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)

class SmallStone(Terrain):
    def __init__(self,x,y,particle_list):
        super().__init__(x,y,(17,12),color.chineseblue,"SmallStone",particle_list)
        self.sprite = pygame.image.load("images/smallstone/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)
        self.offput = (-2,-2)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/smallstone/idle/0.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("idle")

        #self.particle_spawner = objects.ParticleSpawner(self.rect.left,self.rect.right,self.rect.top,self.rect.bottom,self.rect.bottom + 5,particle_list)

    def blit(self,display):
        #if self.flip:
        #    sprite = pygame.transform.flip(sprite, True, False)
        #    sprite.set_colorkey(color.colorkey)
        display.blit(self.sprite,(self.x + self.offput[0],self.y + self.offput[1]))
        #pygame.draw.rect(display,self.color,self.rect)

    def action(self,action):
        if self.animation_action == action:
            pass
        else:
            if self.animation_ticker == 0:
                self.animation_action = action
                self.animation_data = self.animation_database[action]
                self.animation_ticker = 0
                self.animation_frame = 0

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = 0
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)

class Tree1(Terrain):
    def __init__(self,x,y,particle_list):
        super().__init__(x,y,(25,30),color.chineseblue,"Tree",particle_list)
        self.sprite = pygame.image.load("images/tree/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)
        self.offput = (-2,-2)

        self.animation_database = {
          "idle": [[24,24,24,24],[pygame.image.load("images/tree/idle/0.png"),pygame.image.load("images/tree/idle/1.png"),pygame.image.load("images/tree/idle/0.png"),pygame.image.load("images/tree/idle/2.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("idle")

        self.particle_spawner = objects.ParticleSpawner(self.rect.left,self.rect.right,self.rect.top,self.rect.bottom,self.rect.bottom + 5,particle_list)

    def blit(self,display):
        sprite = self.sprite
        #if self.flip:
        #    sprite = pygame.transform.flip(sprite, True, False)
        #    sprite.set_colorkey(color.colorkey)
        display.blit(sprite,(self.x + self.offput[0],self.y + self.offput[1]))
        #pygame.draw.rect(display,self.color,self.rect)

    def action(self,action):
        if self.animation_action == action:
            pass
        else:
            if self.animation_ticker == 0:
                self.animation_action = action
                self.animation_data = self.animation_database[action]
                self.animation_ticker = 0
                self.animation_frame = 0

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = 0
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)
