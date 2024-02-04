from cells import *
from conf import *

render = [None]*m
for i in range(m):
    render[i] = [None]*n



def get_colors():
    for i in range(m):
        for j in range(n):
            cell = matrix[i][j]
            color_list = colors[cell.logic]
            skin = int(cell.skin % len(color_list))
            render[i][j] = color_list[skin]