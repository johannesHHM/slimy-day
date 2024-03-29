import pygame, color, math, objects

color = color.Color((170,0,170))

class Enemy:
    def __init__(self,health,x,y,speed,score,size,default_color,offput):
        self.health = health
        self.x = x
        self.y = y
        self.speed = speed
        self.score = score

        self.size = size
        self.rect = pygame.Rect((x,y),size)
        self.color = default_color
        self.flip = False
        self.offput = offput

        self.animation_action = "idle"
        self.animation_ticker = 0
        self.animation_frame = 0

    def collisions(self,object_list):
        collision_list = []
        for object in object_list:
            if object.rect.colliderect(self.rect):
                if hasattr(object, "type") and object.type == "Border":
                    pass
                else:
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

    def move(self,movement,objects_list):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False,'stationary':False}
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
        if int(last_pos[0]) == int(self.x) and int(last_pos[1]) == int(self.y):
            collision_types['stationary'] = True
        return collision_types

    def blit(self,display):
        sprite = self.sprite
        if self.flip:
            sprite = pygame.transform.flip(sprite, True, False)
            sprite.set_colorkey(color.colorkey)
        #pygame.draw.rect(display,self.color,self.rect)
        display.blit(sprite,(self.x + self.offput[0],self.y + self.offput[1]))

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

    def destruct(self,list):
        pass

    def outside(self,display_size):
        if (self.x + self.size[0] < 0) or (self.y + self.size[1] < 0) or (self.x > display_size[0]) or (self.y > display_size[1]):
            return True
        else:
            return False

class Slime(Enemy):
    def __init__(self,x,y):
        super().__init__(6,x,y,0.25,10,(17,14),color.vivid_violet,(-1,-5))
        self.sprite = pygame.image.load("images/slime/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/slime/idle/0.png")]],
          "movement": [[12,12,12,12],[pygame.image.load("images/slime/movement/0.png"),pygame.image.load("images/slime/movement/1.png"),pygame.image.load("images/slime/movement/2.png"),pygame.image.load("images/slime/movement/3.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("movement")

    def destruct(self,list):
        list.append(objects.SlimeDeath(self.center(),self.flip))

class MediumSlime(Enemy):
    def __init__(self,x,y):     
        super().__init__(4,x,y,0.32,7,(13,11),color.amethyst,(-1,-2))
        self.sprite = pygame.image.load("images/mediumslime/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/mediumslime/idle/0.png")]],
          "movement": [[12,12,12],[pygame.image.load("images/mediumslime/movement/0.png"),pygame.image.load("images/mediumslime/movement/1.png"),pygame.image.load("images/mediumslime/movement/2.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("movement")

    def destruct(self,list):
        list.append(objects.MediumSlimeDeath(self.center(),self.flip))

class SmallSlime(Enemy):
    def __init__(self,x,y):
        super().__init__(3,x,y,0.5,5,(11,11),color.amethyst,(-1,-2))
        self.sprite = pygame.image.load("images/smallslime/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/smallslime/idle/0.png")]],
          "movement": [[12,12,12],[pygame.image.load("images/smallslime/movement/0.png"),pygame.image.load("images/smallslime/movement/1.png"),pygame.image.load("images/smallslime/movement/2.png")]]}
        self.animation_data = self.animation_database["idle"]
        self.action("movement")

    def destruct(self,list):
        list.append(objects.SmallSlimeDeath(self.center(),self.flip))
