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

    def spawn_particle_random(self,time):
        self.particle_list.append(Particle(randrange(self.left,self.right),randrange(self.top,self.bottom),time,self.limit,0.9,0.4,(-0.06,0.25)))
