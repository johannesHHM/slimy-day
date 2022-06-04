import pygame, sys, math
import color, player, enemies
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()
font = pygame.font.SysFont(None, 14)

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

debug_mode = False

player = player.Player(20,20)
color = color.Color((170,0,170))

enemy_list = []

enemy_list.append(enemies.Slug(0,0))
enemy_list.append(enemies.Slug(100,0))
enemy_list.append(enemies.Slug(100,100))

enemy_list.append(enemies.Rat(100,100))
enemy_list.append(enemies.Rat(200,200))
for i in range(10):
    enemy_list.append(enemies.Slug(200,200))

enemy_list.append(enemies.Ogre(300,300))

def cursor_player_angle(player_pos,cursor_pos):
    myradians = math.atan2(cursor_pos[1]-player_pos[1], cursor_pos[0]-player_pos[0])
    mydegrees = math.degrees(myradians)
    return mydegrees

while True:
    display.fill(color.white)

    movement = [0,0]

    if (moving_right):
        movement[0] = movement[0] + player.speed
    if (moving_left):
        movement[0] = movement[0] - player.speed
    if (moving_up):
        movement[1] = movement[1] - player.speed
    if (moving_down):
        movement[1] = movement[1] + player.speed

    player.move(movement[0],movement[1])

    x, y = pygame.mouse.get_pos()
    mouse_pos = (x//zoom,y//zoom)

    player.angle = cursor_player_angle(player.center(),mouse_pos) * -1
    rotimage = pygame.transform.rotate(player.sprite,player.angle)
    rotimage.set_colorkey(color.colorkey)

    p_center = player.center()
    p_center = (p_center[0]-int(rotimage.get_width()/2),p_center[1]-int(rotimage.get_height()/2))

    display.blit(rotimage,p_center)
    #pygame.draw.rect(display, color.red, player.rect)
    #pygame.draw.rect(display, (0,0,255), pygame.Rect(player.center(),(1,1)))

    for enemy in enemy_list[:]:
        movement = enemy.movement(player.center())
        other_enemies = enemy_list.copy()
        other_enemies.remove(enemy)

        enemy.move(movement,other_enemies)

        if enemy.rect.colliderect(player.rect):
            print("DIED TO ", enemy)

        if hasattr(enemy, "sprite"):
            display.blit(enemy.sprite,enemy.rect)
        else:
            pygame.draw.rect(display, enemy.colour, enemy.rect)

    if debug_mode:
        render_FPS = font.render("FPS: " + str(round(clock.get_fps(), 2)), True, (255,0,0))
        display.blit(render_FPS, (1, 1))

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
            if event.key == K_p:
                debug_mode = not debug_mode

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
