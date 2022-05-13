import pygame, sys
import colour
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (720, 720)
zoom = 12

DISPLAY_SIZE = (WINDOW_SIZE[0] // zoom, WINDOW_SIZE[1] // zoom)
print ('x: ' + str(DISPLAY_SIZE[0]) + ' y: ' + str(DISPLAY_SIZE[1]))

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

moving_left = False
moving_right = False
moving_up = False
moving_down = False

pos_x = 20
pos_y = 20

player_size = (5,5)
player_rect = pygame.Rect((pos_x, pos_y), player_size)


while True:
    display.fill((colour.white()))

    movement = [0,0]

    if (moving_right):
        movement[0] = movement[0] + 1
    if (moving_left):
        movement[0] = movement[0] - 1
    if (moving_up):
        movement[1] = movement[1] - 1
    if (moving_down):
        movement[1] = movement[1] + 1

    player_rect = player_rect.move(movement[0],movement[1])

    #player_rect = pygame.Rect((pos_x, pos_y), player_size)

    pygame.draw.rect(display, colour.red(), player_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                moving_up = True
            if event.key == K_DOWN:
                moving_down = True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False

    surf = pygame.transform.scale(display,WINDOW_SIZE)

    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)
