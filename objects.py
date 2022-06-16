import pygame,color,math,random
from random import randrange

color = color.Color((170,0,170))

leaf_list = [pygame.image.load("images/particles/leaf/0.png"),pygame.image.load("images/particles/leaf/1.png"),pygame.image.load("images/particles/leaf/2.png"),pygame.image.load("images/particles/leaf/3.png")]

class Particle():
    def __init__(self,x,y,time,limit,period,amplitude,movement):
        self.x = x
        self.y = y
        self.base = random.choice(leaf_list)
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

class ParticleSpawner():
    def __init__(self,left,right,top,bottom,limit,particle_list):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.limit = limit
        self.particle_list = particle_list

    def spawn_particle_random(self,time,period,amplitude,movement):
        self.particle_list.append(Particle(randrange(self.left,self.right),randrange(self.top,self.bottom),time,self.limit,period,amplitude,movement))

    def spawn_particle_position(self,position,impact_range,time,period,amplitude,movement,terrain_rect,amount):
        impact_rect = pygame.Rect(position[0] - impact_range,position[1] - impact_range,impact_range*2+1,impact_range*2+1)
        clipped_rect = terrain_rect.clip(impact_rect)

        for _ in range(amount):
            self.particle_list.append(Particle(randrange(clipped_rect.left,clipped_rect.right),randrange(clipped_rect.top,clipped_rect.bottom),time,self.limit,period,amplitude,movement))
        return clipped_rect


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
        self.base = pygame.image.load("images/bullet.png")
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
        # rotimage = pygame.transform.rotate(self.base,self.radian)
        # rotimage.set_colorkey(color.colorkey)
        #
        # center = self.center()
        # center = (center[0]-int(rotimage.get_width()/2),center[1]-int(rotimage.get_height()/2))
        #
        # display.blit(rotimage,center)
        display.blit(self.sprite,(self.x - self.sprite.get_width()//2,self.y -self.sprite.get_height()//2))
        #pygame.draw.rect(display,color.black,self.rect)

    def movement(self,player_center):
        radian = math.atan2(self.center()[1] - player_center[1],self.center()[0] - player_center[0])
        y = math.sin(radian) * -self.speed
        x = math.cos(radian) * -self.speed
        return (x,y)
