
window = 0.5 # quick scaling
m = int(128 * window) # columns
n = int(256 * window) # rows
scale = 4 # number of pixels per automaton

max_frame_rate = 60

spread =1

def set_spread(s):
    global spread
    spread = s
    print(spread)
def get_spread():
    return spread

render_optimization = True

SPLASH_ODDS =0.2

SAND_SPAWN_ODDS = 0.5
WATER_SPAWN_ODDS = 0.5
ROCK_SPAWN_ODDS = 0.5
FIRE_SPAWN_ODDS = 0.5

# fire parameters:
up_correction = 10 # higher value skews flame upwards
side_correction = 0.5 # higher value makes the flame wider, larger and longer-lasting
LIMIT_GRADE_SCALE = 10  # higher value implies bigger flame
SKIN_TO_GRADE = 5 # higher value changes the gradient of the flame color

# rock parameters:
ROCK_AUX_LIMIT = 2      # limit 4
ROCK_PRIME_LIMIT = 2    # limit 3
# higher these numbers, harder the rock

WATER_FLUIDITY = 8 # range from 0 to infinity, water flows faster the higher this number is

BLANK = "BLANK"
SAND = "SAND"
WATER = "WATER"
ROCK = "ROCK"
FIRE = "FIRE"
INERT = "INERT"
PLACEHOLDER = "PLACEHOLDER"



colors = {
    BLANK: [(0,0,0)],
    SAND: [(246,215,176),(242,210,169),(236,204,162),(231,196,150),(225,191,146)],
    WATER: [(0,100,250)],
    ROCK: [(100,100,100),(125,125,125),(150,150,150)], 
    FIRE: [(255,255,255),(230,220,0),(200,180,0),(234,170,0),(169,67,30)],
    INERT: [(100,0,100),(150,30,150),(200,50,200)]
}

# debug flags
TALLY_DEBUG = True # presents running count of each element