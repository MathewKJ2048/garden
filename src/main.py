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
    mouse_x, mouse_y = pygame.mouse.get_pos()
    i, j = get_mouse_cell(mouse_x, mouse_y)
    if state == SAND:
        set_sand(i, j, skin_type)
        for I in range(-spread, spread+1):
            for J in range(-spread, spread+1):
                if random.random() < SAND_SPAWN_ODDS:
                    set_sand(i+I, j+J, skin_type)
    elif state == WATER:
        for I in range(-spread, spread+1):
            for J in range(-spread, spread+1):
                if random.random() < WATER_SPAWN_ODDS:
                    set_water(i+I, j+J)
    elif state == BLANK:
        set_blank(i,j)  
    elif state == FIRE:
        set_fire(i,j)          
    elif state == ROCK:
        for I in range(-spread, spread+1):
            for J in range(-spread, spread+1):
                if random.random() < ROCK_SPAWN_ODDS:
                    set_rock(i+I, j+J, skin_type)



init()
running = True



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
            elif event.key == pygame.K_0:
                skin_type = 0
            elif event.key == pygame.K_1:
                skin_type = 1
            elif event.key == pygame.K_2:
                skin_type = 2
        
    process_mouse()
    dt = c.tick(max_frame_rate)
    time = time+dt
    changes = evolve()
    render_screen(changes)
    
    pygame.display.update()

    debug = {}
    for i in range(m):
        for j in range(n):
            if not matrix[i][j].logic in debug:
                debug[matrix[i][j].logic] = 1
            else:
                debug[matrix[i][j].logic] = debug[matrix[i][j].logic] + 1
    print(debug)

    pass