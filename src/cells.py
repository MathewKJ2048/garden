import random
import copy
from conf import *



class Cell:
    def __init__(self, logic, skin):
        self.logic = logic
        self.skin = skin
        self.grade = 0

BLANK_CELL = Cell(BLANK,0)
WATER_CELL = Cell(WATER,0)
FIRE_CORE_CELL = Cell(FIRE,0)
WALL_CELL = Cell(None,0)

time = 0

matrix = [None]*m
for i in range(m):
    matrix[i] = [None]*n

active_locations = set()


def init():
    global m
    global n
    global matrix
    
    
    for i in range(m):
        for j in range(n):
            matrix[i][j] = Cell(BLANK,0)

def set_sand(i,j,type):
    active_locations.add((i,j))
    if type == 0:
        type = (random.random()*1000)
    set_cell((i,j),Cell(SAND,type))

def set_rock(i,j,type):
    active_locations.add((i,j))
    if type == 0:
        type = (random.random()*1000)
    set_cell((i,j),Cell(ROCK,type))

def set_water(i,j):
    active_locations.add((i,j))
    set_cell((i,j),WATER_CELL)

def set_fire(i,j):
    active_locations.add((i,j))
    set_cell((i,j),FIRE_CORE_CELL)

def set_blank(i,j):
    active_locations.discard((i,j))
    set_cell((i,j),BLANK_CELL)

def evolve():
    rand_water = cointoss()
    next_water = set()
    to_modify = set()
    print(len(active_locations))
    for t in active_locations:
        i, j = t

        down = (i+1,j)
        down_left = (i+1,j-1)
        down_right = (i+1,j+1)
        left = (i,j-1)
        right = (i,j+1)
        up = (i-1,j)
        up_right = (i-1,j+1)
        up_left = (i-1,j+1)

        blank_down = get_cell(down).logic == BLANK
        blank_down_right = get_cell(down_right).logic == BLANK
        blank_down_left = get_cell(down_left).logic == BLANK
        blank_left = get_cell(left).logic == BLANK
        blank_right = get_cell(right).logic == BLANK
        blank_up = get_cell(up).logic == BLANK
        blank_up_right = get_cell(up_right) == BLANK
        blank_up_left = get_cell(up_left) == BLANK

        cell = get_cell(t)
        if cell.logic == SAND:
            if blank_down or blank_down_right or blank_down_left:
                to_modify.add((t,BLANK_CELL))
            if blank_down:
                to_modify.add((down,cell))
            elif blank_down_left and blank_down_right:
                if random.random() > 0.5:
                    to_modify.add((down_left,cell))
                else:
                    to_modify.add((down_right,cell))
            elif blank_down_left:
                to_modify.add((down_left,cell))
            elif blank_down_right:
                to_modify.add((down_right,cell))
        elif cell.logic == WATER:
            positions = []
            if blank_down and not down in next_water:
                positions.append(down)
            if blank_down_left and not down_left in next_water:
                positions.append(down_left)
            if blank_down_right and not down_right in next_water:
                positions.append(down_right)
            if len(positions) != 0:
                pos = random.choice(positions)
                to_modify.add((pos,cell))
                next_water.add(pos)
                to_modify.add((t,BLANK_CELL))
            else: # water is no longer flowing
                pos = None
                if  rand_water:
                    if blank_left and not left in next_water:
                        pos = left
                else:
                    if blank_right and not right in next_water:
                        pos = right
                if random.random() < SPLASH_ODDS and blank_up and not up in next_water:
                        pos = up
                if pos != None:
                    to_modify.add((pos,cell))
                    to_modify.add((t,BLANK_CELL))
                    next_water.add(pos)
        elif cell.logic == ROCK:
            if blank_down or get_cell(down).logic == WATER:
                to_modify.add((t,BLANK_CELL))
                to_modify.add((down,cell))
        elif cell.logic == FIRE:
            to_modify.add((t,BLANK_CELL))
            limit = cell.grade/LIMIT_GRADE_SCALE  # lower grade implies more probability and lower limit
            cell_new = copy.deepcopy(cell)
            cell_new.grade = cell.grade+1
            cell_new.skin = int(cell_new.grade/SKIN_TO_GRADE)
            if cell_new.grade <= grade_limit or True:
                if random.random()*up_correction > limit:
                    to_modify.add((up,cell_new))
                if random.random() > limit:
                    if cointoss():
                        to_modify.add((up_right,cell_new))
                    else:
                        to_modify.add((up_left,cell_new))
                
                if random.random()*side_correction > limit:
                    if cointoss():
                        to_modify.add((left,cell_new))
                    else:
                        to_modify.add((right,cell_new))

    for x in to_modify:
        t, cell = x
        if cell.logic == BLANK:
            set_cell(t, cell)
            active_locations.discard(t)
    for x in to_modify:
        t, cell = x
        if cell.logic != BLANK:
            set_cell(t, cell)
            active_locations.add(t)
    
            
    

def get_cell(t):
    assert type(t) == tuple
    i,j = t
    if 0 <= i and i < m and 0 <= j and j < n:
        return matrix[i][j]
    return WALL_CELL

def set_cell(t,cell):
    assert type(cell) == Cell
    assert type(t) == tuple
    assert type(t[0]) == int
    if get_cell(t) != WALL_CELL:
        i, j = t
        matrix[i][j] = cell
    return False

def cointoss():
    return random.random() < 0.5