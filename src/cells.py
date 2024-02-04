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
PLACEHOLDER_CELL = Cell(PLACEHOLDER,0)

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
    return PLACEHOLDER_CELL
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

def set_mixed(i,j,name,type):
    active_locations.add((i,j))
    if type == 0:
        type = (random.random()*1000)
    set_cell((i,j),Cell(name,type))

def set_mono(i,j,cell):
    active_locations.add((i,j))
    set_cell((i,j),cell)

def evolve():
    rand_water = cointoss() # decide which direction water moves this time
    m = {} # table to store all changes amde in this evolution
    changes = set()
    for t in active_locations:
        if get_modify(t,m).logic != PLACEHOLDER:
            continue
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
            unconserved = {BLANK,FIRE}
            logic_now = get_cell(t).logic
            logic_next = get_modify(t,m).logic
            return logic_now in unconserved and logic_next == PLACEHOLDER or logic_next in unconserved
        def move(t_):
            set_modify(t_,m,cell)
            set_modify(t,m,BLANK_CELL)
            changes.add(t)
            changes.add(t_)
        def move_and_change(t_,nc): # move and put a changed copy
            set_modify(t_,m,nc)
            changes.add(t_)
            set_modify(t,m,BLANK_CELL)
            changes.add(t)
        def swap(t_): # swap cells between current and t_
            nc = get_cell(t_)
            set_modify(t,m,nc)
            set_modify(t_,m,cell)
            changes.add(t_)
            changes.add(t)
        
        if cell.logic == SAND:
            if blank(down):
                move(down)
            elif blank(down_left) and blank(down_right):
                move(pick_one(down_left,down_right))
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
            else: # water is no longer flowing
                pos = None
                if rand_water:
                    if blank(left):
                        pos = left
                else:
                    if blank(right):
                        pos = right
                if random.random() < SPLASH_ODDS and blank(up):
                        pos = up
                if pos != None:
                    move(pos)
        
        
        if cell.logic == ROCK:
            
            primary_supports = [left,right,up]
            auxiliary_supports = [up_left,up_right,down_left,down_right]
            ct_prime = 0
            ct_aux = 0
            for s in primary_supports:
                if get_cell(s).logic == ROCK:
                    ct_prime=ct_prime+1
            for s in auxiliary_supports:
                if get_cell(s).logic == ROCK:
                    ct_aux = ct_aux+1
            if ct_prime <= ROCK_PRIME_LIMIT and ct_aux <= ROCK_AUX_LIMIT:
                if blank(down):
                    move(down)
                elif get_cell(down).logic == WATER:
                    down_next_log = get_modify(t,down).logic
                    cell_next_log = get_modify(t,m).logic
                    if (down_next_log == PLACEHOLDER) and (cell_next_log == PLACEHOLDER):
                        swap(down)
        
        elif cell.logic == FIRE:
            limit = cell.grade/LIMIT_GRADE_SCALE  # lower grade implies more probability and lower limit
            cell_new = copy.deepcopy(cell)
            cell_new.grade = cell.grade+1
            cell_new.skin = int(cell_new.grade/SKIN_TO_GRADE)
            if (random.random()*up_correction > limit) and blank(up):
                move_and_change(up,cell_new)
            if random.random() > limit:
                if blank(up_left) and blank(up_right):
                    move_and_change(pick_one(up_left,up_right),cell_new)
                elif blank(up_left):
                    move_and_change(up_left,cell_new)
                elif blank(up_right):
                    move_and_change(up_right,cell_new)
            if random.random()*side_correction > limit:
                if blank(left) and blank(right):
                    move_and_change(pick_one(left,right),cell_new)
                elif blank(left):
                    move_and_change(left,cell_new)
                elif blank(right):
                    move_and_change(right,cell_new)
            set_modify(t,m,BLANK_CELL)
    for key in m:
        t = set_t(key)
        set_cell(t,m[key])
        if m[key].logic != BLANK:
            active_locations.add(t)
        else:
            active_locations.discard(t)
    return changes
    
            
    

def get_cell(t):
    assert type(t) == tuple
    i,j = t
    if 0 <= i and i < m and 0 <= j and j < n:
        return matrix[i][j]
    return PLACEHOLDER_CELL

def set_cell(t,cell):
    assert type(cell) == Cell
    assert type(t) == tuple
    assert type(t[0]) == int
    if get_cell(t) != PLACEHOLDER_CELL:
        i, j = t
        matrix[i][j] = cell
    return False

def cointoss():
    return random.random() < 0.5

def pick_one(a,b):
    if cointoss() < 0.5:
        return a
    return b