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
    pygame.display.update()

def get_mouse_cell(mouse_x, mouse_y):
    return int(mouse_y/scale), int(mouse_x/scale)

def get_random_skin(cell_logic):
    return (random.random()*1000)%len(colors[cell_logic])

def process_mouse():
    spread = get_spread()-1
    mouse_x, mouse_y = pygame.mouse.get_pos()
    i, j = get_mouse_cell(mouse_x, mouse_y)
    for I in range(-spread, spread+1):
            for J in range(-spread, spread+1):
                if state == SAND:
                    if random.random() < SAND_SPAWN_ODDS:
                        insert_cell(i+I,j+J,Cell(SAND,get_random_skin(SAND)))
                elif state == BLANK:
                        insert_cell(i+I,j+J,BLANK_CELL)
                elif state == WATER:
                    if random.random() < WATER_SPAWN_ODDS:
                        insert_cell(i+I, j+J, Cell(WATER,get_random_skin(WATER),velocity=pick_one(1,-1)))
                elif state == ACID:
                    if random.random() < ACID_SPAWN_ODDS:
                        insert_cell(i+I, j+J, Cell(ACID,get_random_skin(ACID),velocity=pick_one(1,-1),grade=ACID_STRENGTH))
                elif state == ROCK:
                    if random.random() < ROCK_SPAWN_ODDS and (I+J+2*spread)%2 == 0:
                        insert_cell(i+I, j+J, Cell(ROCK,get_random_skin(ROCK)))
                elif state == FIRE:
                    if random.random() < FIRE_SPAWN_ODDS and math.sqrt(I**2+J**2)<=spread:
                        insert_cell(i+I,j+J,FIRE_CORE_CELL)
                elif state == INERT:
                    insert_cell(i+I,j+J,Cell(INERT,get_random_skin(INERT)))



init()
running = True
READOUT = False

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
            elif event.key == pygame.K_a:
                state = ACID
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
            elif event.key == pygame.K_l:
                READOUT = True
            elif event.unicode.isdigit():
                set_spread(int(event.unicode))
        
    process_mouse()
    dt = c.tick(max_frame_rate)
    time = time+dt
    
    changes = evolve()
    render_screen(changes)

    if READOUT:
        print("----")
        fps = int(c.get_fps())
        print("performance:\t"+str(int(100*fps/max_frame_rate))+"%")
        print("step:\t"+str(get_step()))
        print("active cells:\t"+str(len(active_locations)))
        debug = {}
        for i in range(m):
            for j in range(n):
                if not matrix[i][j].logic in debug:
                    debug[matrix[i][j].logic] = 1
                else:
                    debug[matrix[i][j].logic] = debug[matrix[i][j].logic] + 1
        print("cell types:\t\t"+str(debug))
        active_debug = {}
        for t in active_locations:
            log = get_cell(t).logic
            if not log in active_debug:
                active_debug[log] = 1
            else:
                active_debug[log] = active_debug[log]+1
        print("active cell types:\t\t"+str(active_debug))
        READOUT = False   

    pass