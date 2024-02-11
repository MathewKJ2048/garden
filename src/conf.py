PLACEHOLDER = -1 # cells which make up the area outside the visible region
# 0 avoided since it is used for error detection
SAND = 1    
WATER = 2  
ROCK = 3
FIRE = 4
ACID = 5
EMBER = 6
INERT = 7
WOOD = 8
OIL = 9
ICE = 10
LAVA = 12
BLANK = 11

DEAD_GRASS = 13
SEED = 14
GROWER_GRASS =15
BODY_GRASS = 16

GROWER_LIGHTNING = 17
BODY_LIGHTNING = 18
LIGHTNING = {GROWER_LIGHTNING,BODY_LIGHTNING}


names = {
    BLANK: "BLANK",
    SAND: "SAND",
    WATER: "WATER",
    ROCK: "ROCK",
    FIRE: "FIRE",
    ACID: "ACID",
    EMBER: "EMBER",
    INERT: "INERT",
    WOOD: "WOOD",
    OIL: "OIL",
    ICE: "ICE",
    LAVA: "LAVA",
    SEED: "SEED",
    GROWER_GRASS: "GROWER GRASS",
    BODY_GRASS: "BODY GRASS",
    DEAD_GRASS: "DEAD GRASS",
    GROWER_LIGHTNING: "GROWER LIGHTNING",
    BODY_LIGHTNING: "BODY LIGHTNING"
}

window = 0.5 # quick scaling
m = int(128 * window) # columns
n = int(256 * window) # rows
scale = 5 # number of pixels per automaton

max_frame_rate = 60

spread =1

def set_spread(s):
    global spread
    spread = s
def get_spread():
    return spread

render_optimization = True

SPAWN_ODDS = 0.5


# fire parameters:
up_correction = 10 # higher value skews flame upwards
side_correction = 0.5 # higher value makes the flame wider, larger and longer-lasting
LIMIT_GRADE_SCALE = 10  # higher value implies bigger flame
SKIN_TO_GRADE = 5 # higher value changes the gradient of the flame color

# rock parameters:
ROCK_AUX_LIMIT = 2      # limit 4
ROCK_PRIME_LIMIT = 2    # limit 3
# higher these numbers, harder the rock

ACID_CAPACITY = 3 # higher value -> consumes more before disappearing
ACID_ACTION_ODDS = 0.1 # higher value -> more likely to consume cells
immune_acid = {INERT,ACID,BLANK,PLACEHOLDER}

EMBER_CAPACITY = 50 # time the ember lasts for
EMBER_FLAMMABILITY_ODDS = 0.5 # higher value -> ignites more often
GENERATED_EMBER_CAPACITY = 5 # how long embers generated from wood lasts


FREEZE_ODDS = 0.01

unconserved = {BLANK,FIRE}
def set_unconserved(list_cells):
    for x in list_cells:
        unconserved.add(x)
set_unconserved(LIGHTNING)


FLUIDS = [WATER,OIL,ACID,LAVA]
viscosity = {
    WATER: 1,
    OIL: 1,
    ACID: 1,
    LAVA: 0.1
}
SPLASH_ODDS = {
    WATER: 0.2,
    OIL: 0.2,
    ACID: 0.2,
    LAVA: 0.05
}

ORGANIC_MATERIAL = [SEED,GROWER_GRASS,BODY_GRASS,DEAD_GRASS] # treated equivalent to wood 
FLAMMABLES = [OIL,WOOD,ICE,ROCK]

HEAT_RESISTANCE = {
    WOOD: 5,
    OIL: 0,
    ICE: 10,
    ROCK: 20
}

LIGHTNING_LIFETIME = 16


colors = {
    BLANK: [(0,0,0)],
    SAND: [(245,215,175),(240,210,170),(235,200,160),(230,195,150),(225,190,150)],
    WATER: [(0,100,250)],
    ROCK: [(200,200,200),(125,125,125),(150,150,150)], 
    FIRE: [(250,250,250),(230,220,0),(200,180,0),(234,170,0),(169,67,30)],
    INERT: [(100,0,90),(150,30,150),(200,50,200)],
    ACID: [(100,255,0)],
    EMBER: [(150,0,0),(160,0,0),(170,0,0)],
    WOOD: [(140,70,20),(165, 91, 83),(91, 39, 11)],
    OIL: [(100,100,100)],
    ICE: [(219, 241, 253),(200, 220, 230),(210, 230, 240),(100,230,230)],
    LAVA: [(250,0,0)],

    # lightning
    GROWER_LIGHTNING : [(255,255,255)],

    # organics
    SEED: [(150,80,30)],
    GROWER_GRASS: [(0,100,0),(40,120,0),(0,50,10)],
    DEAD_GRASS: [(100,100,0),(90,110,0),(110,90,0)]
}
inheritances = {
    BODY_GRASS: GROWER_GRASS,
    BODY_LIGHTNING: GROWER_LIGHTNING
}
for x in inheritances:
    colors[x] = colors[inheritances[x]]

GRASS_HEIGHT = 12
GRASS_GROWTH_RATE = 0.1
WATER_ABSORPTION_ODDS = 0.01

CONTROLS = {
    "b" : BLANK,
    "s" : SAND,
    "w" : WATER,
    "r" : ROCK,
    "f" : FIRE,
    "v" : INERT,
    "a" : ACID,
    "e": EMBER,
    "q": WOOD,
    "o": OIL,
    "i": ICE,
    "m": SEED,
    "l": LAVA,
    'e': GROWER_LIGHTNING
}