import pygame
import math
import random
from cells import *
from render import *

pygame.init()


scale = 4
height = m*scale
width = n*scale
max_frame_rate = 60


screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Garden")

c = pygame.time.Clock()

def render_screen():
    get_colors()
    for i in range(m):
        for j in range(n):
            pygame.draw.rect(screen, render[i][j], (j*scale, i*scale, scale, scale))

def get_mouse_cell(mouse_x, mouse_y):
    return int(mouse_y/scale), int(mouse_x/scale)

def process_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    i, j = get_mouse_cell(mouse_x, mouse_y)
    matrix[i][j] = "SAND"



init()
running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        process_mouse()
    dt = c.tick(max_frame_rate)
    time = time+dt
    evolve()
    render_screen()
    
    pygame.display.update()
    pass
