from cells import *

render = [None]*m
for i in range(m):
    render[i] = [None]*n

colors = {
    BLANK: [(0,0,0)],
    SAND: [(246,215,176),(242,210,169),(236,204,162),(231,196,150),(225,191,146)],
    WATER: [(0,100,250)],
    ROCK: [(100,100,100),(125,125,125),(150,150,150)], 
    FIRE: [(255,255,255),(230,220,0),(200,180,0),(234,170,0),(169,67,30)]
}

def get_colors():
    for i in range(m):
        for j in range(n):
            cell = matrix[i][j]
            color_list = colors[cell.logic]
            skin = int(cell.skin % len(color_list))
            render[i][j] = color_list[skin]