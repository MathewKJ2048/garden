import random
import copy
from conf import *

G = 1 # direction of gravity

steps = 0

def get_step():
    return steps

def invert_gravity():
    global G
    G = -G

class Cell:
    def __init__(self, logic, skin, grade = 0, velocity=0):
        self.logic = logic
        self.skin = skin
        self.grade = grade
        self.velocity = velocity



BLANK_CELL = Cell(BLANK,0)
WATER_CELL = Cell(WATER,0)
FIRE_CORE_CELL = Cell(FIRE,0)
PLACEHOLDER_CELL = Cell(PLACEHOLDER,0)
INERT_CELL = Cell(INERT,0)
ACID_CELL = Cell(ACID,0,ACID_STRENGTH)


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
    try:
        i, j = t
        assert(i>=0 and j>=0 and i<m and j<n)
        return table[set_key(t)]
    except:
        return PLACEHOLDER_CELL
def set_modify(t,table,cell):
    try:
        i,j = t
        assert(i>=0 and j>=0 and i<m and j<n)
        key = set_key(t)
        table[key] = cell
    except:
        pass

def init():
    global m
    global n
    global matrix
    for i in range(m):
        for j in range(n):
            matrix[i][j] = Cell(BLANK,0)


def insert_cell(i,j,cell):
    active_locations.add((i,j))
    set_cell((i,j),cell)

def evolve():

    global steps
    steps = steps+ 1
    rand_water = cointoss() # decide which direction water moves this time
    m = {} # table to store all changes amde in this evolution
    changes = set()

    def blank(t):
        unconserved = {BLANK,FIRE}
        logic_now = get_cell(t).logic
        logic_next = get_modify(t,m).logic
        return logic_now in unconserved and logic_next == PLACEHOLDER or logic_next in unconserved
    def move(t,t_):
        set_modify(t_,m,get_cell(t))
        delete(t)
        changes.add(t_)
    def move_and_change(t,t_,nc): # move and put a changed copy
        set_modify(t_,m,nc)
        changes.add(t_)
        delete(t)
    def swap(t,t_): # swap cells between current and t_
        if get_modify(t,t_).logic == PLACEHOLDER:
            set_modify(t,m,get_cell(t_))
            set_modify(t_,m,get_cell(t))
            changes.add(t_)
    def operable(t):
        return get_modify(t,m).logic == PLACEHOLDER
    def delete(t):
        set_modify(t,m,BLANK_CELL)

    def process():
        for t in active_locations:
            changes.add(t)
            i, j = t
            cell = get_cell(t)
            down = (i+G,j)
            down_left = (i+G,j-1)
            down_right = (i+G,j+1)
            left = (i,j-1)
            right = (i,j+1)
            up = (i-G,j)
            up_right = (i-G,j+1)
            up_left = (i-G,j+1)
            
            if cell.logic == SAND and operable(t):
                if blank(down):
                    move(t,down)
                elif blank(down_left) and blank(down_right):
                    move(t,pick_one(down_left,down_right))
                elif blank(down_left):
                    move(t,down_left)
                elif blank(down_right):
                    move(t,down_right)
                elif get_cell(down).logic == WATER:
                    swap(t,down)
                
            elif cell.logic == WATER and operable(t):
                positions = []
                if blank(down):
                    positions.append(down)
                if blank(down_left):
                    positions.append(down_left)
                if blank(down_right):
                    positions.append(down_right)
                if len(positions) != 0:
                    move(t,random.choice(positions))
                elif blank(up) and random.random() < SPLASH_ODDS:
                    move(t,up)
                else: # water is no longer flowing
                    bl = blank(left)
                    br = blank(right)
                    # move in given velocity, if blocked then invert velocity
                    if cell.velocity == 1:
                        if bl:
                            move(t,left)
                        elif br:
                            move(t,right)
                            cell.velocity = -1
                    else:
                        if br:
                            move(t,right)
                        elif bl:
                            move(t,left)
                            cell.velocity = 1
                    pass

            elif cell.logic == ACID and operable(t):
                if cell.grade == 0:
                    delete(t)
                else:
                    immune = {INERT,ACID,BLANK}
                    action_directions = {up,down,left,right}
                    positions = []
                    for pos in action_directions:
                        if not get_cell(pos).logic in immune and operable(pos):
                            positions.append(pos)
                    if len(positions) != 0:
                        delete(random.choice(positions))
                        cell.grade = cell.grade-1
                    else:
                        positions = []
                        if blank(down):
                            positions.append(down)
                        if blank(down_left):
                            positions.append(down_left)
                        if blank(down_right):
                            positions.append(down_right)
                        if len(positions) != 0:
                            move(t,random.choice(positions))
                        elif blank(up) and random.random() < SPLASH_ODDS:
                            move(t,up)
                        else: # acid is no longer flowing
                            bl = blank(left)
                            br = blank(right)
                            # move in given velocity, if blocked then invert velocity
                            if cell.velocity == 1:
                                if bl:
                                    move(t,left)
                                elif br:
                                    move(t,right)
                                    cell.velocity = -1
                            else:
                                if br:
                                    move(t,right)
                                elif bl:
                                    move(t,left)
                                    cell.velocity = 1
            
            elif cell.logic == ROCK and operable(t):
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
                        move(t,down)
                    elif get_cell(down).logic == WATER:
                        swap(t,down)
            
            elif cell.logic == FIRE and operable(t):
                limit = cell.grade/LIMIT_GRADE_SCALE  # lower grade implies more probability and lower limit
                cell_new = copy.deepcopy(cell)
                cell_new.grade = cell.grade+1
                cell_new.skin = int(cell_new.grade/SKIN_TO_GRADE)
                if (random.random()*up_correction > limit) and blank(up):
                    move_and_change(t,up,cell_new)
                if random.random() > limit:
                    if blank(up_left) and blank(up_right):
                        move_and_change(t,pick_one(up_left,up_right),cell_new)
                    elif blank(up_left):
                        move_and_change(t,up_left,cell_new)
                    elif blank(up_right):
                        move_and_change(t,up_right,cell_new)
                if random.random()*side_correction > limit:
                    if blank(left) and blank(right):
                        move_and_change(t,pick_one(left,right),cell_new)
                    elif blank(left):
                        move_and_change(t,left,cell_new)
                    elif blank(right):
                        move_and_change(t,right,cell_new)
                delete(t)

        for key in m:
            t = set_t(key)
            set_cell(t,m[key])
            active_locations.add(t)

        m.clear()
        

    process()

    to_deactivate = set()
    for t in active_locations:
        log = get_cell(t).logic
        if log in {PLACEHOLDER,BLANK,INERT}:
            to_deactivate.add(t)
    
    active_locations.difference_update(to_deactivate)

    return changes
    
    

def get_cell(t):
    try:
        i, j = t
        assert(i>=0 and j>=0 and i<m and j<n)
        return matrix[i][j]
    except:
        return INERT_CELL

def set_cell(t,cell):
    try:
        i, j = t
        assert(i>=0 and j>=0 and i<m and j<n)
        matrix[i][j] = cell
    except:
        pass

def cointoss():
    return random.random() < 0.5

def pick_one(a,b):
    if cointoss() < 0.5:
        return a
    return b