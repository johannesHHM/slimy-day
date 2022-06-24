import pygame, math, color

color = color.Color((170,0,170))

class Player:
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = 2.1
        self.size = (11,16)
        self.rect = pygame.Rect((x,y),self.size)
        self.color = color.martinique
        self.offput = (-5,-2)
        self.sprite = pygame.image.load("images/player/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)
        self.angle = 0
        self.invinc = 0
        self.flip = False
        self.kill_box = pygame.Rect((x - 18,y - 18),(47,52))

        self.animation_action = "idle"
        self.animation_ticker = 0
        self.animation_frame = 0
        self.animation_database = {
          "idle": [[12,12,12,12,12,12,24],[pygame.image.load("images/player/idle/0.png"),pygame.image.load("images/player/idle/0.png"),pygame.image.load("images/player/idle/0.png"),pygame.image.load("images/player/idle/0.png"),pygame.image.load("images/player/idle/0.png"),pygame.image.load("images/player/idle/0.png"),pygame.image.load("images/player/idle/1.png")]],
          "movement": [[6,6],[pygame.image.load("images/player/movement/1.png"),pygame.image.load("images/player/movement/0.png")]]}
        self.animation_data = self.animation_database["idle"]

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
        self.kill_box.x = self.x - 18
        self.kill_box.y = self.y - 18
        return collision_types

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center

    def blit(self,display):
        sprite = self.sprite
        if self.flip:
            sprite = pygame.transform.flip(sprite, True, False)
            sprite.set_colorkey(color.colorkey)
        display.blit(sprite,(self.x + self.offput[0],self.y + self.offput[1]))
        #pygame.draw.rect(display,color.amethyst,self.kill_box)
        #pygame.draw.rect(display,self.color,self.rect)

    def cursor_player_angle(self,cursor_pos):
        center = self.center()
        myradians = math.atan2(cursor_pos[1]-center[1], cursor_pos[0]-center[0])
        mydegrees = math.degrees(myradians)
        return mydegrees

    def action(self,action):
        if self.animation_action == action:
            pass
        else:
            if self.animation_ticker == 0 or action == "movement":
                self.animation_action = action
                self.animation_data = self.animation_database[action]
                self.animation_ticker = 0
                self.animation_frame = 0

                self.sprite = self.animation_data[1][self.animation_frame]
                self.sprite.set_colorkey(color.colorkey)

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = 0
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)
