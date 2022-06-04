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

    def collisions(self,object_list):
        collision_list = []
        for object in object_list:
            if object.rect.colliderect(self.rect):
                collision_list.append(object)
        print(len(collision_list))
        return collision_list

    def center(self):
        center = (self.x + self.size[0]//2,self.y + self.size[1]//2)
        return center

    def move(self,movement,enemy_list):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        #Collisions in x direction
        self.x += movement[0]
        self.rect.x = int(self.x)
        enemy_hit_list = self.collisions(enemy_list)
        for enemy in enemy_hit_list:
            if movement[0] > 0:
                self.rect.right = enemy.rect.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = enemy.rect.right
                collision_types['left'] = True
            self.x = self.rect.x
        #Collisions in y direction
        self.y += movement[1]
        self.rect.y = int(self.y)
        enemy_hit_list = self.collisions(enemy_list)
        for enemy in enemy_hit_list:
            if movement[1] > 0:
                self.rect.bottom = enemy.rect.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = enemy.rect.bottom
                collision_types['top'] = True
            self.y = self.rect.y
        return collision_types

class Slug(Enemy):
    def __init__(self,x,y):
        super().__init__(3,x,y,0.5,(13,13),(0,255,0))

class Rat(Enemy):
    def __init__(self,x,y):
        super().__init__(3,x,y,1,(11,11),(100,100,100))
