import pygame, color, math

color = color.Color((170,0,170))

animation_database = {
  "idle": [[12],[pygame.image.load("images/rat/idle/0.png")]],
  "movement": [[12,12],[pygame.image.load("images/rat/movement/0.png"),pygame.image.load("images/rat/movement/1.png")]]
}

class Enemy:
    def __init__(self,health,x,y,speed,size,default_color,offput):
        self.health = health
        self.x = x
        self.y = y
        self.speed = speed
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

class Slime(Enemy):
    def __init__(self,x,y):
        super().__init__(3,x,y,0.5,(13,11),color.green,(0,0))
        self.sprite = pygame.image.load("images/slime/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/slime/idle/0.png")]],
          "movement": [[12,12],[pygame.image.load("images/slime/movement/0.png"),pygame.image.load("images/slime/movement/1.png")]]}
        self.animation_data = animation_database["idle"]

        self.action("movement")

class Rat(Enemy):
    def __init__(self,x,y):
        super().__init__(2,x,y,1.5,(10,9),color.gray,(-3,-2))
        self.sprite = pygame.image.load("images/rat/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/rat/idle/0.png")]],
          "movement": [[12,12],[pygame.image.load("images/rat/movement/0.png"),pygame.image.load("images/rat/movement/1.png")]]}
        self.animation_data = animation_database["idle"]

        self.action("movement")

class Ogre(Enemy):
    def __init__(self,x,y):
        super().__init__(7,x,y,0.4,(25,29),color.brown,(0,0))
        self.sprite = pygame.image.load("images/ogre/idle/0.png")
        self.sprite.set_colorkey(color.colorkey)

        self.animation_database = {
          "idle": [[12],[pygame.image.load("images/ogre/idle/0.png")]],
          "movement": [[12,12,12,12],[pygame.image.load("images/ogre/movement/0.png"),pygame.image.load("images/ogre/movement/1.png"),pygame.image.load("images/ogre/movement/2.png"),pygame.image.load("images/ogre/movement/3.png")]]}
        self.animation_data = animation_database["idle"]

        self.action("movement")
