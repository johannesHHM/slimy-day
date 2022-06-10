import pygame, sys, math
import color, player, enemies, terrain
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()
font = pygame.font.SysFont(None, 14)
gui_font = pygame.font.SysFont(None, 30)

WINDOW_SIZE = (900,900)
zoom = 3

DISPLAY_SIZE = (WINDOW_SIZE[0] // zoom, WINDOW_SIZE[1] // zoom)
print ('x: ' + str(DISPLAY_SIZE[0]) + ' y: ' + str(DISPLAY_SIZE[1]))

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

moving_left = False
moving_right = False
moving_up = False
moving_down = False

debug_mode = False

player = player.Player(10,10)
color = color.Color((170,0,170))
BLINK_RATE = 5

enemy_list = []
terrain_list = []

heart_image = pygame.image.load("images/heart.png")
heart_image.set_colorkey(color.colorkey)

three_image = pygame.image.load("images/3.png")
three_image.set_colorkey(color.colorkey)
two_image = pygame.image.load("images/2.png")
two_image.set_colorkey(color.colorkey)
one_image = pygame.image.load("images/1.png")
one_image.set_colorkey(color.colorkey)

def cursor_player_angle(player_pos,cursor_pos):
    myradians = math.atan2(cursor_pos[1]-player_pos[1], cursor_pos[0]-player_pos[0])
    mydegrees = math.degrees(myradians)
    return mydegrees

def generate_border(width):
    border_terrain = []
    border_terrain.append(terrain.Terrain(0,0,(width,DISPLAY_SIZE[1]),color.gray))
    border_terrain.append(terrain.Terrain(0,0,(DISPLAY_SIZE[0],width),color.gray))
    border_terrain.append(terrain.Terrain(DISPLAY_SIZE[0]-width,0,(width,DISPLAY_SIZE[1]),color.gray))
    border_terrain.append(terrain.Terrain(0,DISPLAY_SIZE[1]-width,(DISPLAY_SIZE[0],width),color.gray))
    return border_terrain

def spawn_mobs(enemy_list):
    for i in range(20):
        enemy_list.append(enemies.Slime(110+i*10,200))
    for i in range(10):
        enemy_list.append(enemies.Rat(200,0+i*10))
    enemy_list.append(enemies.Rat(200,20))
    enemy_list.append(enemies.Ogre(200,200))
    enemy_list.append(enemies.Ogre(250,220))

def spawn_terrain(terrain_list):
    terrain_list.extend(generate_border(5))
    terrain_list.append(terrain.Terrain(40,20,(20,100),color.black))
    terrain_list.append(terrain.Terrain(200,60,(30,50),color.black))
    terrain_list.append(terrain.Water(20,200,(100,30)))

spawn_mobs(enemy_list)
spawn_terrain(terrain_list)

while True:
    display.fill(color.pastel)

    #-------< Terrain Handling >-------#

    for terrain in terrain_list[:]:
        pygame.draw.rect(display, terrain.color, terrain.rect)

    #-------< Heath Bar >-------#

    display.blit(heart_image,(212,2))
    if player.health == 3:
        display.blit(three_image,(232,2))
    elif player.health == 2:
        display.blit(two_image,(232,2))
    elif player.health == 1:
        display.blit(one_image,(232,2))

    #-------< Player Handling >-------#

    if player.invinc > 0:
        player.invinc += -1

    movement = [0,0]
    if moving_right:
        movement[0] = movement[0] + player.speed
    if moving_left:
        movement[0] = movement[0] - player.speed
    if moving_up:
        movement[1] = movement[1] - player.speed
    if moving_down:
        movement[1] = movement[1] + player.speed

    player.move(movement,terrain_list)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pos = (mouse_x//zoom,mouse_y//zoom)

    player.angle = cursor_player_angle(player.center(),mouse_pos) * -1
    rotimage = pygame.transform.rotate(player.sprite,player.angle)
    rotimage.set_colorkey(color.colorkey)

    p_center = player.center()
    p_center = (p_center[0]-int(rotimage.get_width()/2),p_center[1]-int(rotimage.get_height()/2))

    if player.invinc > 0:
        if BLINK_RATE > 0:
            display.blit(rotimage,p_center)
        BLINK_RATE += -1
        if BLINK_RATE <= -5:
            BLINK_RATE = 5
    else:
        display.blit(rotimage,p_center)
    #pygame.draw.rect(display, color.red, player.rect)
    #pygame.draw.rect(display, (0,0,255), pygame.Rect(player.center(),(1,1)))

    #-------< Enemy Handling >-------#

    for enemy in enemy_list[:]:
        movement = enemy.movement(player.center())
        other_objects = enemy_list.copy()
        other_objects.extend(terrain_list)
        other_objects.remove(enemy)

        if movement[0] < 0:
            enemy.flip = False
        else:
            enemy.flip = True
        enemy.move(movement,other_objects)

        if enemy.rect.colliderect(player.rect) and player.invinc <= 0:
            player.health += -1
            player.invinc = 80
        if hasattr(enemy, "sprite"):
            enemy.blit(display)
        else:
            pygame.draw.rect(display, enemy.color, enemy.rect)

        if hasattr(enemy, "animation_ticker"):
            enemy.tick()
            if debug_mode:
                enemy.action("idle")
            else:
                enemy.action("movement")

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
            if event.key == K_SPACE:
                enemy_list.append(enemies.Rat(mouse_pos[0], mouse_pos[1]))

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
