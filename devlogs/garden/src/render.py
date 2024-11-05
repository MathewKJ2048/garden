from cells import *
from conf import *

render = [None]*m
for i in range(m):
    render[i] = [colors[BLANK][0]]*n

def get_render(i,j):
    try:
        return render[i][j]
    except:
        return colors[BLANK][0]

def set_render(i,j,color):
    try:
        render[i][j] = color
    except:
        pass

def get_colors(to_paint):
    if not render_optimization:
        for i in range(m):
            for j in range(n):
                to_paint.add((i,j))
    for t in to_paint:
        i, j = t
        cell = get_cell(t)
        if not cell.logic in colors:
            continue
        color_list = colors[cell.logic]
        skin = int(cell.skin % len(color_list))
        set_render(i,j,color_list[skin])
    return to_paint