import pygame, sys, math
import color, player, enemies
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (720, 720)
zoom = 2

DISPLAY_SIZE = (WINDOW_SIZE[0] // zoom, WINDOW_SIZE[1] // zoom)
print ('x: ' + str(DISPLAY_SIZE[0]) + ' y: ' + str(DISPLAY_SIZE[1]))

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

moving_left = False
moving_right = False
moving_up = False
moving_down = False

player = player.Player(20,20)
color = color.Color((170,0,170))

enemy_list = []

enemy_list.append(enemies.Slug(0, 0))
enemy_list.append(enemies.Slug(100, 0))
enemy_list.append(enemies.Slug(100, 100))

enemy_list.append(enemies.Rat(200, 100))

def cursor_player_angle(player_pos,cursor_pos):
    myradians = math.atan2(cursor_pos[1]-player_pos[1], cursor_pos[0]-player_pos[0])
    mydegrees = math.degrees(myradians)
    return mydegrees

print(cursor_player_angle((20,20),(20,20)))

while True:
    display.fill(color.white)

    movement = [0,0]

    if (moving_right):
        movement[0] = movement[0] + 2
    if (moving_left):
        movement[0] = movement[0] - 2
    if (moving_up):
        movement[1] = movement[1] - 2
    if (moving_down):
        movement[1] = movement[1] + 2

    player.move(movement[0],movement[1])

    x, y = pygame.mouse.get_pos()
    mouse_pos = (x//zoom,y//zoom)

    player.angle = cursor_player_angle(player.get_center(),mouse_pos) * -1
    rotimage = pygame.transform.rotate(player.sprite,player.angle)
    rotimage.set_colorkey(color.colorkey)
    rect = rotimage.get_rect(center=player.get_center())

    display.blit(rotimage,rect)
    #pygame.draw.rect(display, (0,0,255), pygame.Rect(player.get_center(),(1,1)))

    for enemy in enemy_list[:]:
        movement = [0,0]
        p_center = player.get_center()
        #other_enemies = enemy_list
        #other_enemies.remove(enemy)

        other_enemies = []
        for enemy_else in enemy_list:
            if enemy != enemy_else:
                other_enemies.append((enemy_else))

        if(p_center[0] + 1 > enemy.center()[0]):
            movement[0] = movement[0] + enemy.speed
        if(p_center[0] - 1 < enemy.center()[0]):
            movement[0] = movement[0] - enemy.speed
        if(p_center[1] - 1 < enemy.center()[1]):
            movement[1] = movement[1] - enemy.speed
        if(p_center[1] + 1 > enemy.center()[1]):
            movement[1] = movement[1] + enemy.speed

        enemy.move(movement,other_enemies)
        pygame.draw.rect(display, enemy.colour, enemy.rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = True
            if event.key == K_LEFT or event.key == K_a:
                moving_left = True
            if event.key == K_UP or event.key == K_w:
                moving_up = True
            if event.key == K_DOWN or event.key == K_s:
                moving_down = True

        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False
            if event.key == K_LEFT or event.key == K_a:
                moving_left = False
            if event.key == K_UP or event.key == K_w:
                moving_up = False
            if event.key == K_DOWN or event.key == K_s:
                moving_down = False

    surf = pygame.transform.scale(display,WINDOW_SIZE)

    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)
