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


def get_random_skin(cell_logic):
    return (random.random()*1000)%len(colors[cell_logic])

class Cell:
    def __init__(self, logic, skin = -1, grade = 0, velocity=0):
        self.logic = logic
        if skin == -1:
            self.skin = get_random_skin(logic)
        else:
            self.skin = skin
        self.grade = grade
        self.velocity = velocity

PLACEHOLDER = -1
PLACEHOLDER_CELL = Cell(PLACEHOLDER,0)
BLANK_CELL = Cell(BLANK,0)
INERT_CELL = Cell(INERT,0)
FIRE_CORE_CELL = Cell(FIRE,0,0)



def generate(logic, i, j):
    spread = get_spread()
    for I in range(-spread+1, spread):
        for J in range(-spread+1, spread):
            cell = Cell(logic)
            if logic in FLUIDS:
                cell.velocity =pick_one(1,-1)
            if logic in FLAMMABLES:
                cell.grade = HEAT_RESISTANCE[logic]
            if logic == ACID:
                cell.grade = ACID_STRENGTH
            elif logic == EMBER:
                cell.grade = EMBER_CAPACITY

            if logic == ROCK and (I+J+2*spread)%2 == 1:
                continue

            if random.random() < SPAWN_ODDS:
                insert_cell(i+I,j+J,cell)

def insert_cell(i,j,cell):
    active_locations.add((i,j))
    set_cell((i,j),cell)


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


def evolve(PAUSED):

    global steps
    steps = steps+ 1
    rand_water = cointoss() # decide which direction water moves this time
    m = {} # table to store all changes made in this evolution
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
    def place(t, cell):
        set_modify(t,m,cell)
        changes.add(t)
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
        al = list(active_locations)
        random.shuffle(al)
        for t in al:
            
            changes.add(t)
            if PAUSED:
                continue

            i, j = t
            cell = get_cell(t)
            down = (i+G,j)
            down_left = (i+G,j-1)
            down_right = (i+G,j+1)
            left = (i,j-1)
            right = (i,j+1)
            up = (i-G,j)
            up_right = (i-G,j+1)
            up_left = (i-G,j-1)
            
            neighbours = [up,up_left,up_right,left,right,down,down_left,down_right]
            neighbours_close = [up,down,left,right]

            def ignite(pos):
                fuel = get_cell(pos)
                if fuel.logic in FLAMMABLES and operable(pos):
                    replacements = {
                        WOOD: Cell(EMBER,grade=GENERATED_EMBER_CAPACITY),
                        ICE: Cell(WATER,velocity=pick_one(1,-1)),
                        OIL: FIRE_CORE_CELL,
                        ROCK: Cell(LAVA)
                    }
                    if fuel.grade <=0:
                        place(pos,replacements[fuel.logic])
                    else:
                        fuel.grade = fuel.grade-1


            if cell.logic == SAND and operable(t):
                if blank(down):
                    move(t,down)
                elif blank(down_left) and blank(down_right):
                    move(t,pick_one(down_left,down_right))
                elif blank(down_left):
                    move(t,down_left)
                elif blank(down_right):
                    move(t,down_right)
                elif get_cell(down).logic in FLUIDS:
                    swap(t,down)

            if cell.logic == EMBER and operable(t):
                if cell.grade <= 0:
                    delete(t)
                else:
                    cell.grade = cell.grade-1
                    if blank(down):
                        move(t,down)
                    elif blank(down_left) and blank(down_right):
                        move(t,pick_one(down_left,down_right))
                    elif blank(down_left):
                        move(t,down_left)
                    elif blank(down_right):
                        move(t,down_right)
                    elif get_cell(down).logic in FLUIDS:
                        swap(t,down)
                    if random.random() < EMBER_FLAMMABILITY_ODDS:
                        positions = []
                        for pos in neighbours_close:
                            if blank(pos):
                                positions.append(pos)
                        if len(positions) != 0:
                            place(random.choice(positions),FIRE_CORE_CELL)
                
            if cell.logic == OIL and operable(t):
                swappable_postions = [up,up_left,up_right]
                sp = []
                for pos in swappable_postions:
                    if operable(pos) and get_cell(pos).logic == WATER:
                        sp.append(pos)
                if len(sp)!=0:
                    swap(t,random.choice(sp))
                else:
                    sl = operable(left) and get_cell(left).logic == WATER
                    sr = operable(right) and get_cell(right).logic == WATER
                    if cell.velocity == 1 and sl:
                        swap(t,left)
                    elif cell.velocity == -1 and sr:
                        swap(t,right)
                    else:
                        if sl:
                            swap(t,left)
                            cell.velocity = 1
                        elif sr:
                            swap(t,right)
                            cell.velocity = -1

            if cell.logic == ACID and operable(t):
                if cell.grade == 0:
                    delete(t)
                else:
                    positions = []
                    for pos in neighbours_close:
                        if not get_cell(pos).logic in immune_acid and operable(pos):
                            positions.append(pos)
                    if len(positions) != 0:
                        delete(random.choice(positions))
                        cell.grade = cell.grade-1
            
            if cell.logic == LAVA and operable(t):
                for pos in neighbours_close:
                    if operable(pos) and get_cell(pos).logic == WATER:
                        place(t,Cell(ROCK))
                        delete(pos)
                        break
                if operable(t):
                    for pos in neighbours:
                        fuel = get_cell(pos)
                        if fuel.logic != ROCK:
                            ignite(pos)

            if cell.logic == WATER and operable(t):
                for pos in neighbours_close:
                    if get_cell(pos).logic == ICE:
                        if random.random() < FREEZE_ODDS:
                            place(t,Cell(ICE))

            if cell.logic in FLUIDS and operable(t):
                # check if splashing happens
                splash_positons = []
                side_flow_postions = []
                if random.random() < viscosity[cell.logic]:
                    side_flow_postions = [left,right]
                if random.random() < SPLASH_ODDS[cell.logic]:
                    splash_positons = [up,up_left,up_right]
                flowable_postions = [[down,down_left,down_right],splash_positons,side_flow_postions]
                
                pos = None # final position to move to
                fp = [] # free flowable positions
                
                # compute availability of free positons
                for pos_set in flowable_postions:
                    fp_end = []
                    for p in pos_set:
                        if blank(p):
                            fp_end.append(p)
                    fp.append(fp_end)

                # pick according to priority
                double_free = False
                for pos_set_free in fp:
                    if len(pos_set_free) != 0:
                        if left in pos_set_free and right in pos_set_free:
                            double_free = True
                        pos = random.choice(pos_set_free)
                        break

                # if position chosen is opposite velocity
                if pos == left and double_free and cell.velocity == -1:
                    pos = right
                elif pos == right and double_free and cell.velocity == 1:
                    pos = left

                # reassign velocity
                if pos == left:
                    cell.velocity = 1
                elif pos == right:
                    cell.velocity = -1

                if not pos == None:
                    move(t,pos)
            
            if cell.logic == ROCK and operable(t):
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
                    elif get_cell(down).logic in FLUIDS:
                        swap(t,down)


            if cell.logic == FIRE and operable(t):
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
                
                for pos in neighbours:
                    ignite(pos)       
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
        if log in {PLACEHOLDER,BLANK,INERT,ICE,WOOD}:
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