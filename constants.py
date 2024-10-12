WIDTH, HEIGHT = 1200, 600  # Window size
BODY_RADIUS = 20 # pixels

# Colors
BACKGROUND = (5, 5, 5)  # Color for background
BODY_COLOR = (255, 255, 255)  # Color for body
FORCE_LINE_COLOR = (255, 155, 50)
STARTING_FUEL_COLOR = (255, 255, 255)
ENDING_FUEL_COLOR = (255, 55, 55)


# Physics Constants
GRAVITY = 9.8
GROUND_FRICTION_COEF = 200000
BODY_MASS = 8000 # kg
TANK_SIZE = 150000 # liters
LOSS_OF_FUEL = 1000 / 60 # liters per frame per thruster [liter  /  ((per second) / 60 seconds)]


# Force of propulsion on body
PFORCE = 6 * (BODY_MASS + (TANK_SIZE * 0.8))

# Other
FORCE_LINE_WIDTH = 5
DRAW_FORCES = False
FPS = 60  # Frames per second
