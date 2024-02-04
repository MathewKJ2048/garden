m = 128
n = 360
scale = 3
max_frame_rate = 120

spread =3

SPLASH_ODDS = 0.1

SAND_SPAWN_ODDS = 0.5
WATER_SPAWN_ODDS = 0.5
ROCK_SPAWN_ODDS = 0.9

# fire parameters:
up_correction = 10 # higher value skews flame upwards
side_correction = 0.5 # higher value makes the flame wider, larger and longer-lasting
LIMIT_GRADE_SCALE = 10  # higher value implies bigger flame
SKIN_TO_GRADE = 5 # higher value changes the gradient of the flame color

BLANK = "BLANK"
SAND = "SAND"
WATER = "WATER"
ROCK = "ROCK"
FIRE = "FIRE"



colors = {
    BLANK: [(0,0,0)],
    SAND: [(246,215,176),(242,210,169),(236,204,162),(231,196,150),(225,191,146)],
    WATER: [(0,100,250)],
    ROCK: [(100,100,100),(125,125,125),(150,150,150)], 
    FIRE: [(255,255,255),(230,220,0),(200,180,0),(234,170,0),(169,67,30)]
}