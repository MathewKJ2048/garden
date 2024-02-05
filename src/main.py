import pygame
import math
import random
from cells import *
from render import *
from conf import *

state = None

skin_type = 0

pygame.init()


height = m*scale
width = n*scale


screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Garden")

c = pygame.time.Clock()

def render_screen(changes):
    tp = get_colors(changes)
    for t in tp:
        i, j = t
        pygame.draw.rect(screen, get_render(i,j), (j*scale, i*scale, scale, scale))

def get_mouse_cell(mouse_x, mouse_y):
    return int(mouse_y/scale), int(mouse_x/scale)

def process_mouse():
    spread = get_spread()-1
    mouse_x, mouse_y = pygame.mouse.get_pos()
    i, j = get_mouse_cell(mouse_x, mouse_y)
    for I in range(-spread, spread+1):
            for J in range(-spread, spread+1):
                if state == SAND:
                    if random.random() < SAND_SPAWN_ODDS:
                        set_mixed(i+I, j+J, SAND, skin_type)
                elif state == BLANK:
                        set_mono(i+I,j+J,BLANK_CELL)
                elif state == WATER:
                    if random.random() < WATER_SPAWN_ODDS:
                        set_mixed(i+I, j+J, WATER, skin_type)
                elif state == ROCK:
                    if random.random() < ROCK_SPAWN_ODDS and (I+J+2*spread)%2 == 0:
                        set_mixed(i+I, j+J, ROCK,skin_type)
                elif state == FIRE:
                    if random.random() < FIRE_SPAWN_ODDS:
                        set_mono(i+I,j+J,FIRE_CORE_CELL)
                elif state == INERT:
                    set_mixed(i+I,j+J,INERT,skin_type)



init()
running = True


last_time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                state = SAND
            elif event.key == pygame.K_c:
                state = None
            elif event.key == pygame.K_w:
                state = WATER
            elif event.key == pygame.K_r:
                state = ROCK
            elif event.key == pygame.K_b:
                state = BLANK
            elif event.key == pygame.K_f:
                state = FIRE
            elif event.key == pygame.K_i:
                state = INERT
            elif event.key == pygame.K_g:
                invert_gravity()
            elif event.key == pygame.K_0:
                set_spread(0)
            elif event.key == pygame.K_1:
                set_spread(1)
            elif event.key == pygame.K_2:
                set_spread(2)
            elif event.key == pygame.K_3:
                set_spread(3)
        
    process_mouse()
    dt = c.tick(max_frame_rate)
    time = time+dt
    
    changes = evolve()
    render_screen(changes)
    pygame.display.update()

    if int((time-last_time)/ 1000) != 0:
        last_time = time
        print("framerate:"+str(int(c.get_fps())))
        if TALLY_DEBUG:
            debug = {}
            for i in range(m):
                for j in range(n):
                    if not matrix[i][j].logic in debug:
                        debug[matrix[i][j].logic] = 1
                    else:
                        debug[matrix[i][j].logic] = debug[matrix[i][j].logic] + 1
            print(debug)

    pass