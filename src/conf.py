
window = 1 # quick scaling
m = int(128 * window) # columns
n = int(256 * window) # rows
scale = 4 # number of pixels per automaton

max_frame_rate = 60

spread =1

def set_spread(s):
    global spread
    spread = s
def get_spread():
    return spread

render_optimization = True

SPLASH_ODDS = 0.2  # odds of fluid jumping randomly, increasing this too much interferes with viscosity

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

ACID_STRENGTH = 3 # higher value -> consumes more before disappearing

EMBER_LASTING = 100 # time the ember lasts for
EMBER_FLAMMABILITY_ODDS = 0.1 # higher value -> ignites more often

EMBER_CAPACITY = EMBER_LASTING*EMBER_FLAMMABILITY_ODDS

FREEZE_ODDS = 0.1

BLANK = "BLANK"
SAND = "SAND"
WATER = "WATER"
ROCK = "ROCK"
FIRE = "FIRE"
ACID = "ACID"
EMBER = "EMBER"
INERT = "INERT"
WOOD = "WOOD"
OIL = "OIL"
ICE = "ICE"
PLACEHOLDER = "PLACEHOLDER"

FLUIDS = [WATER,OIL,ACID]

colors = {
    BLANK: [(0,0,0)],
    SAND: [(246,215,176),(242,210,169),(236,204,162),(231,196,150),(225,191,146)],
    WATER: [(0,100,250)],
    ROCK: [(200,200,200),(125,125,125),(150,150,150)], 
    FIRE: [(250,250,250),(230,220,0),(200,180,0),(234,170,0),(169,67,30)],
    INERT: [(100,0,100),(150,30,150),(200,50,200)],
    ACID: [(100,255,0)],
    EMBER: [(150,0,0),(160,0,0),(170,0,0)],
    WOOD: [(140,70,20),(165, 91, 83),(91, 39, 11)],
    OIL: [(100,100,100)],
    ICE: [(219, 241, 253),(200, 220, 230),(210, 230, 240),(100,230,230)]
}

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
    "o":OIL,
    "i":ICE
}


