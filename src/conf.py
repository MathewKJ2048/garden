
window = 0.5
m = int(128 * window)
n = int(256 * window)
scale = 3
max_frame_rate = 120

spread =3

render_optimization = False

SPLASH_ODDS = 0.0

SAND_SPAWN_ODDS = 0.5
WATER_SPAWN_ODDS = 0.5
ROCK_SPAWN_ODDS = 0.1

# fire parameters:
up_correction = 10 # higher value skews flame upwards
side_correction = 0.5 # higher value makes the flame wider, larger and longer-lasting
LIMIT_GRADE_SCALE = 10  # higher value implies bigger flame
SKIN_TO_GRADE = 5 # higher value changes the gradient of the flame color

# rock parameters:
ROCK_AUX_LIMIT = 2      # limit 4
ROCK_PRIME_LIMIT = 2    # limit 3
# higher these numbers, harder the rock

BLANK = "BLANK"
SAND = "SAND"
WATER = "WATER"
ROCK = "ROCK"
FIRE = "FIRE"
PLACEHOLDER = "PLACEHOLDER"



colors = {
    BLANK: [(0,0,0)],
    SAND: [(246,215,176),(242,210,169),(236,204,162),(231,196,150),(225,191,146)],
    WATER: [(0,100,250)],
    ROCK: [(100,100,100),(125,125,125),(150,150,150)], 
    FIRE: [(255,255,255),(230,220,0),(200,180,0),(234,170,0),(169,67,30)]
}

# debug flags
TALLY_DEBUG = True # presents running count of each element