import pygame, sys, math, random
import color, playerC, enemies, terrain, objects,doodads
from pygame.locals import *
from random import randrange

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("Project-4")
font = pygame.font.SysFont(None, 14)
gui_font = pygame.font.SysFont(None, 30)

WINDOW_SIZE = (900,900)
zoom = 4

DISPLAY_SIZE = (WINDOW_SIZE[0] // zoom, WINDOW_SIZE[1] // zoom)
print ('x: ' + str(DISPLAY_SIZE[0]) + ' y: ' + str(DISPLAY_SIZE[1]))

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

#-------< Global Variables >-------#

moving_left = False
moving_right = False
moving_up = False
moving_down = False

debug_mode = False

player = playerC.Player(110,110)
player.health = 0
color = color.Color((170,0,170))
blink_rate = 5
score = 0
shooting = False
shooting_cooldown = 0

main_menu = True

sine_value = 0
enemy_list = []
terrain_list = []
particle_list = []
bullet_list = []
doodad_list = []
enemy_spawner_list = []
tempsprite_list = []

#-------< Images >-------#

heart_image = pygame.image.load("images/heart.png")
heart_image.set_colorkey(color.colorkey)
level_image = pygame.image.load("images/level.png")
level_image.set_colorkey(color.colorkey)

background = pygame.image.load("images/background.png")
end_screen = pygame.image.load("images/endscreen.png")
end_screen.set_colorkey(color.colorkey)

start_screen = pygame.image.load("images/menu.png")
start_screen.set_colorkey(color.colorkey)

zero_image = pygame.image.load("images/numbers/0.png")
zero_image.set_colorkey(color.colorkey)
one_image = pygame.image.load("images/numbers/1.png")
one_image.set_colorkey(color.colorkey)
two_image = pygame.image.load("images/numbers/2.png")
two_image.set_colorkey(color.colorkey)
three_image = pygame.image.load("images/numbers/3.png")
three_image.set_colorkey(color.colorkey)
four_image = pygame.image.load("images/numbers/4.png")
four_image.set_colorkey(color.colorkey)
five_image = pygame.image.load("images/numbers/5.png")
five_image.set_colorkey(color.colorkey)
six_image = pygame.image.load("images/numbers/6.png")
six_image.set_colorkey(color.colorkey)
seven_image = pygame.image.load("images/numbers/7.png")
seven_image.set_colorkey(color.colorkey)
eight_image = pygame.image.load("images/numbers/8.png")
eight_image.set_colorkey(color.colorkey)
nine_image = pygame.image.load("images/numbers/9.png")
nine_image.set_colorkey(color.colorkey)

number_dict = {
    "0": zero_image,
    "1": one_image,
    "2": two_image,
    "3": three_image,
    "4": four_image,
    "5": five_image,
    "6": six_image,
    "7": seven_image,
    "8": eight_image,
    "9": nine_image
}

#-------< Sounds >-------#

pygame.mixer.music.set_volume(0.1)

main_theme = pygame.mixer.music.load("sounds/music/music.wav")
pygame.mixer.music.play(-1)

level_rate_list = [[0,0,[0.85,0.1,0.05]],
[-20,-50,[0.82,0.17,0.1]],
[-50,-80,[0.7,0.18,0.12]],
[-70,-100,[0.67,0.2,0.13]],
[-100,-120,[0.64,0.22,0.14]],
[-100,-150,[0.61,0.23,0.16]],
[-120,-170,[0.58,0.25,0.17]],
[-140,-200,[0.55,0.27,0.18]],
[-160,-220,[0.53,0.28,0.19]],
[-170,-230,[0.5,0.3,0.2]]]

level = 0

#-------< Helping Functions >-------#

def generate_border(terrain_list,width):
    terrain_list.append(terrain.Terrain(0,0,(width,DISPLAY_SIZE[1]),color.azalea,"Border",particle_list))
    terrain_list.append(terrain.Terrain(0,0,(DISPLAY_SIZE[0],width),color.azalea,"Border",particle_list))
    terrain_list.append(terrain.Terrain(DISPLAY_SIZE[0]-width,0,(width,DISPLAY_SIZE[1]),color.azalea,"Border",particle_list))
    terrain_list.append(terrain.Terrain(0,DISPLAY_SIZE[1]-width,(DISPLAY_SIZE[0],width),color.azalea,"Border",particle_list))

def spawn_terrain(terrain_list):
    generate_border(terrain_list,1)
    terrain_list.append(terrain.SmallStone(150,170,particle_list))
    terrain_list.append(terrain.Stone(120,35,particle_list))
    terrain_list.append(terrain.Tree(40,50,particle_list))
    terrain_list.append(terrain.Tree(170,80,particle_list))
    terrain_list.append(terrain.Tree(50,140,particle_list))

def spawn_doodads(doodad_list):
    doodad_list.append(doodads.Flowers(10,15))
    doodad_list.append(doodads.Flowers(79,30))
    doodad_list.append(doodads.Flowers(132,85))
    doodad_list.append(doodads.Flowers(15,92))
    doodad_list.append(doodads.Flowers(81,107))
    doodad_list.append(doodads.Flowers(179,18))
    doodad_list.append(doodads.Flowers(192,146))
    doodad_list.append(doodads.Flowers(94,186))
    doodad_list.append(doodads.Flowers(17,193))
    pass

def spawn_enemy_spawners(enemy_spawner_list):
    enemy_spawner_list.append(objects.EnemySpawner(-30,-10,0,DISPLAY_SIZE[1]//2,enemy_list))
    enemy_spawner_list.append(objects.EnemySpawner(-30,-10,DISPLAY_SIZE[1]//2,DISPLAY_SIZE[1],enemy_list))
    enemy_spawner_list.append(objects.EnemySpawner(0,DISPLAY_SIZE[0]//2,-30,-10,enemy_list))
    enemy_spawner_list.append(objects.EnemySpawner(DISPLAY_SIZE[0]//2,DISPLAY_SIZE[0],-30,-10,enemy_list))

    enemy_spawner_list.append(objects.EnemySpawner(DISPLAY_SIZE[0] + 10,DISPLAY_SIZE[0] + 30,0,DISPLAY_SIZE[1]//2,enemy_list))
    enemy_spawner_list.append(objects.EnemySpawner(DISPLAY_SIZE[0] + 10,DISPLAY_SIZE[0] + 30,DISPLAY_SIZE[1]//2,DISPLAY_SIZE[1],enemy_list))
    enemy_spawner_list.append(objects.EnemySpawner(0,DISPLAY_SIZE[0]//2,DISPLAY_SIZE[1] + 10,DISPLAY_SIZE[1] + 30,enemy_list))
    enemy_spawner_list.append(objects.EnemySpawner(DISPLAY_SIZE[0]//2,DISPLAY_SIZE[0],DISPLAY_SIZE[1] + 10,DISPLAY_SIZE[1] + 30,enemy_list))

def reset_game():
    global player,blink_rate,score,shooting,shooting_cooldown,enemy_list,enemy_spawner_list,bullet_list,terrain_list,doodad_list
    player = playerC.Player(110,110)
    blink_rate = 5
    score = 0
    shooting = False
    shooting_cooldown = 0

    sine_value = 0

    enemy_list.clear()
    bullet_list.clear()
    enemy_spawner_list.clear()

    spawn_method()
    spawn_enemy_spawners(enemy_spawner_list)

def spawn_method():
    global terrain_list,doodad_list
    terrain_list = []
    doodad_list = []

    spawn_terrain(terrain_list)
    spawn_doodads(doodad_list)
    #spawn_enemy_spawners(enemy_spawner_list)

spawn_method()

spawner = objects.EnemySpawner(0,225,0,255,enemy_list)

while True:

    sine_value += 0.05
    sine = round(math.sin(sine_value),2)

    #-------< Background >-------#

    display.blit(background,(0,0))

    #-------< Doodad >-------#

    for doodad in doodad_list:
        doodad.blit(display)
        doodad.tick()

    #-------< Terrain >-------#

    for terr in terrain_list[:]:
        for bullet in bullet_list[:]:
            if terr.rect.colliderect(bullet.rect):
                bullet_list.remove(bullet)
                if not terr.type == "Border":
                    tempsprite_list.append(objects.BulletCrack(bullet.center(),False))
                if hasattr(terr,"particle_spawner"):
                    terr.particle_spawner.spawn_particle_position(bullet.center(),10,randrange(40,100),0.9,0.4,(-0.06,0.25),terr.rect,randrange(2,5))

        if hasattr(terr,"particle_spawner"):
            if randrange(0,29) == 0:
                terr.particle_spawner.spawn_particle_random(randrange(60,100),0.9,0.4,(-0.06,0.25))

        if hasattr(terr, "sprite"):
            terr.blit(display)
            terr.tick()
        else:
            pygame.draw.rect(display, terr.color, terr.rect)

    #-------< HUD >-------#

    if not main_menu:
        display.blit(level_image,(3,3))
        level_string = str(level + 1)
        level_number_pos = 2
        for i in range(len(level_string)):
            number = level_string[i]
            display.blit(number_dict[number],(31 + level_number_pos,3))
            level_number_pos += 12

        score_string = str(score)
        length = len(score_string)
        offset = (length*12)//2
        number_pos = (DISPLAY_SIZE[0]//2) - offset

        for i in range(length):
            number = score_string[i]
            display.blit(number_dict[number],(number_pos,3))
            number_pos += 12

        display.blit(heart_image,(197,2))
        display.blit(number_dict[str(player.health)],(211,3))

    #-------< Particles >-------#

    for particle in particle_list[:]:
        particle.tick(sine_value)
        particle.blit(display)
        particle.time += -1
        particle.rotate(2)
        if particle.time <= 0:
            particle_list.remove(particle)
        elif particle.limit <= particle.y:
            particle_list.remove(particle)

    #-------< Bullets >-------#

    for bullet in bullet_list[:]:
        bullet.move()
        bullet.blit(display)

    #-------< Level Spawning >-------#

    level = score//150
    if level > len(level_rate_list) - 1:
        level = 9

    #-------< Enemy Spawning >-------#

    if len(enemy_list) < 160:
        for spawner in enemy_spawner_list:
            spawner.tick()
            if spawner.cooldown <= 0:
                # Death spawning
                if player.health > 0:
                    if level <= len(level_rate_list) - 1:
                        spawner.spawn_enemies(level_rate_list[level])
                    else:
                        spawner.spawn_enemies(level_rate_list[len(level_rate_list) - 1])
                else:
                    spawner.spawn_enemies([-470,-600,4])

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
        move_data = enemy.move(movement,other_objects)

        if enemy.rect.colliderect(player.rect) and player.invinc <= 0:
            player.health += -1
            player.invinc = 80

        for bullet in bullet_list[:]:
            if enemy.rect.colliderect(bullet.rect):
                enemy.health += -1
                bullet_list.remove(bullet)
                tempsprite_list.append(objects.BulletCrack(bullet.center(),False))

        if enemy.health <= 0:
            score += enemy.score
            enemy_list.remove(enemy)
            enemy.destruct(tempsprite_list)
            #tempsprite_list.append(objects.SmallSlimeDeath(enemy.center()))

        if enemy.rect.colliderect(player.kill_box) and enemy.outside(DISPLAY_SIZE):
            enemy_list.remove(enemy)
            random.choice(enemy_spawner_list).spawn_enemy(level_rate_list[level])

        enemy.tick()
        enemy.action("movement")

        if debug_mode:
            enemy.action("idle")

        if hasattr(enemy, "sprite"):
            enemy.blit(display)
        else:
            pygame.draw.rect(display, enemy.color, enemy.rect)

    #-------< Tempsprite >-------#

    for tempsprite in tempsprite_list[:]:
        if tempsprite.finished:
            tempsprite_list.remove(tempsprite)
        else:
            tempsprite.tick()
            tempsprite.blit_center(display)

    #-------< Player Handling >-------#

    action = "idle"
    if player.health > 0:
        if player.invinc > 0:
            player.invinc += -1

        movement = [0,0]
        if moving_right:
            player.flip = True
            movement[0] = movement[0] + player.speed
        if moving_left:
            player.flip = False
            movement[0] = movement[0] - player.speed
        if moving_up:
            movement[1] = movement[1] - player.speed
        if moving_down:
            movement[1] = movement[1] + player.speed

        player.tick()
        if (not movement[0] == 0) or (not movement[1] == 0):
            action = "movement"
            if shooting:
                action = "movement_throw"
        else:
            action = "idle"
            if shooting:
                action = "idle_throw"

        player.action(action)

        if shooting and shooting_cooldown <= 0:
            bullet = objects.Bullet(player.center()[0] - 1,player.center()[1],mouse_pos)
            bullet_list.append(bullet)
            player.flip = bullet.direction()
            shooting_cooldown = 14

        shooting_cooldown += -1

        player.move(movement,terrain_list)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x//zoom,mouse_y//zoom)

        if player.invinc > 0:
            if blink_rate > 0:
                player.blit(display)
            blink_rate += -1
            if blink_rate <= -5:
                blink_rate = 5
        else:
            player.blit(display)

    #-------< Debug Mode >-------#

    if debug_mode:
        render_FPS = font.render("FPS: " + str(round(clock.get_fps(), 2)), True, (255,0,0))
        display.blit(render_FPS, (1, 1))

    #-------< Input Handling >-------#

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]//zoom
            y = pos[1]//zoom
            #print("(" + str(x) + "," + str(y) + ")")

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
            if event.key == K_c:
                enemy_list.append(enemies.Slime(mouse_pos[0], mouse_pos[1]))
                particle_list.append(objects.Leaf(mouse_pos[0],mouse_pos[1],randrange(40,80),85,0.9,0.4,(0,0.3)))
            if event.key == K_SPACE:
                shooting = True
                if player.health <= 0:
                    main_menu = not main_menu
                    if main_menu == False:
                        reset_game()
                        pygame.mixer.music.fadeout(100)
                        pygame.mixer.music.load("sounds/music/music_loop.wav")
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.fadeout(100)
                        pygame.mixer.music.load("sounds/music/music.wav")
                        pygame.mixer.music.play(-1)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False
            if event.key == K_LEFT or event.key == K_a:
                moving_left = False
            if event.key == K_UP or event.key == K_w:
                moving_up = False
            if event.key == K_DOWN or event.key == K_s:
                moving_down = False
            if event.key == K_SPACE:
                shooting = False

    #-------< Endscreen >-------#

    if player.health <= 0 and not main_menu:
        display.blit(end_screen,(0,0))

    #-------< Menu >-------#

    if main_menu:
        display.blit(start_screen,(0,0))

    #-------< Screen Handling >-------#

    surf = pygame.transform.scale(display,WINDOW_SIZE)

    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)
