import pygame, math

class Player:
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = 2.3
        self.size = (11,11)
        self.rect = pygame.Rect((x,y),self.size)
        self.color = (255,0,0)
        self.sprite = pygame.image.load("images/player.png")
        self.angle = 0
        self.invinc = 0

    def collisions(self,object_list):
        collision_list = []
        for object in object_list:
            if object.rect.colliderect(self.rect):
                collision_list.append(object)
        return collision_list

    def move(self,movement,objects_list):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        object_hit_list = self.collisions(objects_list)
        #Collisions in x direction
        last_pos = (self.x,self.y)
        self.x += movement[0]
        self.rect.x = int(self.x)
        object_hit_list = self.collisions(objects_list)
        for enemy in object_hit_list:
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
        object_hit_list = self.collisions(objects_list)
        for enemy in object_hit_list:
            if movement[1] > 0:
                self.rect.bottom = enemy.rect.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = enemy.rect.bottom
                collision_types['top'] = True
            self.y = self.rect.y
        object_hit_list = self.collisions(objects_list)
        if len(object_hit_list) > 0:
            self.x = last_pos[0]
            self.y = last_pos[1]
            self.rect.x = last_pos[0]
            self.rect.y = last_pos[1]
        return collision_types

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center

    def cursor_player_angle(self,cursor_pos):
        center = self.center()
        myradians = math.atan2(cursor_pos[1]-center[1], cursor_pos[0]-center[0])
        mydegrees = math.degrees(myradians)
        return mydegrees
