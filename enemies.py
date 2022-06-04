import pygame, color, math

color = color.Color((170,0,170))

class Enemy:
    def __init__(self,health,x,y,speed,size,default_color):
        self.health = health
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.rect = pygame.Rect((x,y),size)
        self.colour = default_color

    def collisions(self,object_list):
        collision_list = []
        for object in object_list:
            if object.rect.colliderect(self.rect):
                collision_list.append(object)
        return collision_list

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center

    def movement(self,player_center):
        radian = math.atan2(self.center()[1] - player_center[1],self.center()[0] - player_center[0])
        y = math.sin(radian) * -self.speed
        x = math.cos(radian) * -self.speed
        return (x,y)

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
        super().__init__(3,x,y,0.5,(20,20),color.green)
        self.sprite = pygame.image.load("slime.png")
        self.sprite.set_colorkey(color.colorkey)

class Rat(Enemy):
    def __init__(self,x,y):
        super().__init__(2,x,y,1.5,(15,15),color.gray)
        self.sprite = pygame.image.load("rat.png")
        self.sprite.set_colorkey(color.colorkey)

class Ogre(Enemy):
    def __init__(self,x,y):
        super().__init__(5,x,y,0.4,(50,50),color.brown)
        self.sprite = pygame.image.load("ogre.png")
        self.sprite.set_colorkey(color.colorkey)
