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

def set_t(key):
    nums = key.split()
    return (int(nums[0]),int(nums[1]))
def set_key(t):
    i,j = t
    return str(i)+" "+str(j)
def get_modify(t,table): 
    key = set_key(t)
    if key in table:
        return table[key]
    return None
def get_predict(t,table):
    p = get_modify(t,table)
    if p == None:
        return get_cell(t)
    return p
def set_modify(t,table,cell):
    key = set_key(t)
    table[key] = cell

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
    rand_water = cointoss() # decide which direction water moves this time
    m = {} # table to store all changes amde in this evolution
    changes = set()
    print(str(len(active_locations)))
    for t in active_locations:
        i, j = t
        cell = get_cell(t)
        down = (i+1,j)
        down_left = (i+1,j-1)
        down_right = (i+1,j+1)
        left = (i,j-1)
        right = (i,j+1)
        up = (i-1,j)
        up_right = (i-1,j+1)
        up_left = (i-1,j+1)
        def blank(t):
            return get_predict(t,m).logic == BLANK
        def delete():
            set_modify(t,m,BLANK_CELL)
            changes.add(t)
        def move(t_):
            set_modify(t_,m,cell)
            changes.add(t_)
        def move_and_change(t_,nc):
            set_modify(t_,m,nc)
            changes.add(t_)

        
        
        if cell.logic == SAND:
            if blank(down) or blank(down_right) or blank(down_left):
                delete()
            if blank(down):
                move(down)
            elif blank(down_left) and blank(down_right):
                if cointoss():
                    move(down_left)
                else:
                    move(down_right)
            elif blank(down_left):
                move(down_left)
            elif blank(down_right):
                move(down_right)
        
        elif cell.logic == WATER:
            positions = []
            if blank(down):
                positions.append(down)
            if blank(down_left):
                positions.append(down_left)
            if blank(down_right):
                positions.append(down_right)
            if len(positions) != 0:
                move(random.choice(positions))
                delete()
            else: # water is no longer flowing
                pos = None
                if  rand_water:
                    if blank(left):
                        pos = left
                else:
                    if blank(right):
                        pos = right
                if random.random() < SPLASH_ODDS and blank(up):
                        pos = up
                if pos != None:
                    move(pos)
                    delete()

        elif cell.logic == ROCK:
            if blank(down):
                delete()
                move(down)
        
        elif cell.logic == FIRE:
            delete()
            limit = cell.grade/LIMIT_GRADE_SCALE  # lower grade implies more probability and lower limit
            cell_new = copy.deepcopy(cell)
            cell_new.grade = cell.grade+1
            cell_new.skin = int(cell_new.grade/SKIN_TO_GRADE)
            if random.random()*up_correction > limit:
                move_and_change(up,cell_new)
            if random.random() > limit:
                if cointoss():
                    move_and_change(up_left,cell_new)
                else:
                    move_and_change(up_right,cell_new)
            
            if random.random()*side_correction > limit:
                if cointoss():
                    move_and_change(left,cell_new)
                else:
                    move_and_change(right,cell_new)
    for key in m:
        t = set_t(key)
        set_cell(t,m[key])
        if m[key].logic != BLANK:
            active_locations.add(t)
        else:
            active_locations.discard(t)
    print("render:"+str(len(changes)))
    return changes
    
            
    

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