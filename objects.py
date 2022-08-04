import pygame,color,math,random,enemies
from random import randrange,uniform,choice,choices

color = color.Color((170,0,170))

#leaf_list = [pygame.image.load("images/particles/leaf/0.png"),pygame.image.load("images/particles/leaf/1.png"),pygame.image.load("images/particles/leaf/2.png"),pygame.image.load("images/particles/leaf/3.png")]

class Particle():
    def __init__(self,x,y,time,limit,period,amplitude,movement,base):
        self.x = x
        self.y = y
        self.base = random.choice(base)
        self.sprite = self.base
        self.sprite.set_colorkey(color.colorkey)
        self.rotation = 0
        self.time = time
        self.limit = limit

        self.period = period
        self.amplitude = amplitude
        self.movement = movement

    def tick(self,sine_value):
        sine = round(math.sin(sine_value * self.period) * self.amplitude,2)
        self.move((sine + self.movement[0],self.movement[1]))

    def move(self,movement):
        self.x += movement[0]
        self.y += movement[1]

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center

    def rotate(self,added_rotation):
        self.rotation += added_rotation
        self.sprite = pygame.transform.rotate(self.base,self.rotation)
        self.sprite.set_colorkey(color.colorkey)

    def blit(self,display):
        display.blit(self.sprite,(self.x,self.y))

class Leaf(Particle):
    def __init__(self,x,y,time,limit,period,amplitude,movement):
        leaf_list = [pygame.image.load("images/particles/leaf/0.png"),pygame.image.load("images/particles/leaf/1.png"),pygame.image.load("images/particles/leaf/2.png"),pygame.image.load("images/particles/leaf/3.png")]
        super().__init__(x,y,time,limit,period,amplitude,movement,leaf_list)

class Stone(Particle):
    def __init__(self,x,y,time,limit,period,amplitude,movement):
        stone_list = [pygame.image.load("images/particles/stone/0.png"),pygame.image.load("images/particles/stone/1.png"),pygame.image.load("images/particles/stone/2.png")]
        super().__init__(x,y,time,limit,period,amplitude,movement,stone_list)

        self.movement = (uniform(-0.6,0.6),uniform(-0.6,0.2))

    def tick(self,sine_value):
        self.move((self.movement[0],self.movement[1]))

class LeafParticleSpawner():
    def __init__(self,left,right,top,bottom,limit,particle_list):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.limit = limit
        self.particle_list = particle_list

    def spawn_particle_random(self,time,period,amplitude,movement):
        self.particle_list.append(Leaf(randrange(self.left,self.right),randrange(self.top,self.bottom),time,self.limit,period,amplitude,movement))

    def spawn_particle_position(self,position,impact_range,time,period,amplitude,movement,terrain_rect,amount):
        impact_rect = pygame.Rect(position[0] - impact_range,position[1] - impact_range,impact_range*2+1,impact_range*2+1)
        clipped_rect = terrain_rect.clip(impact_rect)

        for _ in range(amount):
            self.particle_list.append(Leaf(randrange(clipped_rect.left,clipped_rect.right),randrange(clipped_rect.top,clipped_rect.bottom),time,self.limit,period,amplitude,movement))
        return clipped_rect

class StoneParticleSpawner():
    def __init__(self,left,right,top,bottom,limit,particle_list):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.limit = limit
        self.particle_list = particle_list

    def spawn_particle_random(self,time,period,amplitude,movement):
        pass
        #self.particle_list.append(Stone(randrange(self.left,self.right),randrange(self.top,self.bottom),time,self.limit,period,amplitude,movement))

    def spawn_particle_position(self,position,impact_range,time,period,amplitude,movement,terrain_rect,amount):
        impact_rect = pygame.Rect(position[0],position[1],1,1)
        clipped_rect = terrain_rect.clip(impact_rect)

        for i in range(amount):
            self.particle_list.append(Stone(position[0],position[1],10,self.limit,period,amplitude,movement))

class EnemySpawner():
    def __init__(self,left,right,top,bottom,enemy_list):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.enemy_list = enemy_list
        self.cooldown = randrange(200,800)

    def tick(self):
        self.cooldown += -1

    def spawn_enemies(self,level_rate):
        population = [enemies.SmallSlime(randrange(self.left,self.right),randrange(self.top,self.bottom)),enemies.MediumSlime(randrange(self.left,self.right),randrange(self.top,self.bottom)),enemies.Slime(randrange(self.left,self.right),randrange(self.top,self.bottom))]

        choice = choices(population,weights=level_rate[2],k=1)[0]
        self.enemy_list.append(choice)

        self.cooldown = randrange(500 + level_rate[0],700 + level_rate[1])

    def spawn_enemy(self,level_rate):
        population = [enemies.SmallSlime(randrange(self.left,self.right),randrange(self.top,self.bottom)),enemies.MediumSlime(randrange(self.left,self.right),randrange(self.top,self.bottom)),enemies.Slime(randrange(self.left,self.right),randrange(self.top,self.bottom))]

        choice = choices(population,weights=level_rate[2],k=1)[0]
        self.enemy_list.append(choice)


class TemporarySprite():
    def __init__(self,center,animation_data,flip):
        self.center = center
        self.flip = flip
        self.animation_data = animation_data
        self.sprite = self.animation_data[1][0]
        self.sprite.set_colorkey(color.colorkey)

        self.animation_ticker = 0
        self.animation_frame = 0
        self.finished = False

    def tick(self):
        self.animation_ticker += 1
        if self.animation_ticker > self.animation_data[0][self.animation_frame]:
            self.animation_ticker = 0
            self.animation_frame += 1
            if self.animation_frame > len(self.animation_data[0]) - 1:
                self.animation_frame = len(self.animation_data[0]) - 1
                self.finished = True
            self.sprite = self.animation_data[1][self.animation_frame]
            self.sprite.set_colorkey(color.colorkey)

    def blit_center(self,display):
        sprite = self.sprite
        x = int(sprite.get_width()/2)
        y = int(sprite.get_height()/2)
        if self.flip:
            sprite = pygame.transform.flip(sprite, True, False)
            sprite.set_colorkey(color.colorkey)
        display.blit(sprite,(self.center[0] - x,self.center[1] - y))

class BulletCrack(TemporarySprite):
    def __init__(self,center,flip):
        super().__init__(center,[[3,3],choice([[pygame.image.load("images/bullet/destruct/0.png"),pygame.image.load("images/bullet/destruct/1.png")],[pygame.image.load("images/bullet/destruct/2.png"),pygame.image.load("images/bullet/destruct/3.png")],[pygame.image.load("images/bullet/destruct/4.png"),pygame.image.load("images/bullet/destruct/5.png")]])],flip)

class SmallSlimeDeath(TemporarySprite):
    def __init__(self,center,flip):
        super().__init__(center,[[12,12,36],[pygame.image.load("images/smallslime/destruct/0.png"),pygame.image.load("images/smallslime/destruct/1.png"),pygame.image.load("images/smallslime/destruct/2.png")]],flip)

class SlimeDeath(TemporarySprite):
    def __init__(self,center,flip):
        super().__init__(center,[[12,12,12,36],[pygame.image.load("images/slime/destruct/0.png"),pygame.image.load("images/slime/destruct/1.png"),pygame.image.load("images/slime/destruct/2.png"),pygame.image.load("images/slime/destruct/3.png")]],flip)

class MediumSlimeDeath(TemporarySprite):
    def __init__(self,center,flip):
        super().__init__(center,[[12,12,12,36],[pygame.image.load("images/mediumslime/destruct/0.png"),pygame.image.load("images/mediumslime/destruct/1.png"),pygame.image.load("images/mediumslime/destruct/2.png"),pygame.image.load("images/mediumslime/destruct/3.png")]],flip)

class Bullet():
    def __init__(self,x,y,mouse_pos):
        self.x = x
        self.y = y
        self.mouse_pos = mouse_pos
        self.speed = 4
        self.size = (4,4)
        self.rect = pygame.Rect((self.x,self.y),self.size)

        self.radian = math.atan2(self.center()[1] - self.mouse_pos[1],self.center()[0] - self.mouse_pos[0])
        self.angle = math.degrees(self.radian) * 1
        self.movement = (math.cos(self.radian) * -self.speed,math.sin(self.radian) * -self.speed)
        self.base = pygame.image.load("images/bullet/bullet.png")
        self.sprite = pygame.transform.rotate(self.base,self.angle)
        self.sprite.set_colorkey(color.colorkey)

    def move(self):
        self.x += self.movement[0]
        self.y += self.movement[1]
        self.rect.left = self.x
        self.rect.top = self.y

    def direction(self):
        if abs(self.angle) > 90:
            return True
        else:
            return False
        print(self.angle)

    def center(self):
        center = (self.x + int(self.size[0]/2),self.y + int(self.size[1]/2))
        return center

    def blit(self,display):
        display.blit(self.sprite,(self.x - self.sprite.get_width()//2,self.y -self.sprite.get_height()//2))

    def movement(self,player_center):
        radian = math.atan2(self.center()[1] - player_center[1],self.center()[0] - player_center[0])
        y = math.sin(radian) * -self.speed
        x = math.cos(radian) * -self.speed
        return (x,y)
