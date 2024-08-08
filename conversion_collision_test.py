import sys, random, time, math
random.seed(1)  # Make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util

## Conversion Factor
pixels_per_meter = 50  # 1 meter = 50 pixels

## Question Setup
floor_y_meters = 20  # The height of the ground in meters
ball_mass = 3  # Mass of the ball in kg
ball_y_meters = 1  # Initial height of the ball in meters
ball_x_meters = 2.4  # Initial x-position of the ball in meters

# Convert meters to pixels
floor_y_pixels = floor_y_meters * pixels_per_meter
ball_y_pixels = ball_y_meters * pixels_per_meter
ball_x_pixels = ball_x_meters * pixels_per_meter

# Set up the question and answer
question = f"If a ball of mass {ball_mass} kg is dropped from a height of {ball_y_meters} meters, how long is the ball in the air for? (in seconds, assume g=9.8 m/s²)"
correct_answer = "0.45"  # Calculate based on physics, t = sqrt(2h/g)

def calc_time_in_air(height, gravity):
    time = math.sqrt(2* height / gravity)
    print(height)
    print(gravity)
    print(time)

    return time


# To store the start time of each ball
ball_start_times = {}                   # based on overall time
ball_start_times_frames = {}            # based on frames

def add_ball(space):
    radius = 0.1 * pixels_per_meter  # Assuming the ball radius is 0.25 meters
    body = pymunk.Body()
    body.position = ball_x_pixels, ball_y_pixels
    shape = pymunk.Circle(body, radius)
    shape.mass = ball_mass
    shape.friction = 1
    space.add(body, shape)
    
    # Store the start time for this ball using its ID
    ball_start_times[id(shape)] = time.time()

    return shape

def add_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (300, floor_y_pixels)
    shape = pymunk.Segment(body, (-300, 0), (300, 0), 5)  # Creates a horizontal line (ground)
    shape.friction = 1
    space.add(body, shape)
    return shape

def draw_text(screen, text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def ball_hit_ground(arbiter, space, data):
    global correct_answer, user_input

    # This function is called when the ball hits the ground
    if arbiter.is_first_contact:
        print("Ball hit the ground!")
        
        # Retrieve the ball shape involved in the collision
        ball_shape = arbiter.shapes[0]  # This is the shape of the ball
        
        # Calculate how long the ball was in the air
        start_time = ball_start_times.get(id(ball_shape))
        if start_time is not None:
            air_time = time.time() - start_time
            print(f"The ball was in the air for {air_time:.2f} seconds")
        
       
        # Remove the ball from the space
        space.remove(ball_shape, ball_shape.body)

    return True  # Return True to allow the physics simulation to proceed

def main():
    global user_input
    pygame.init()

    calculated_answer = calc_time_in_air(floor_y_meters - ball_y_meters, gravity=9.8)
    screen = pygame.display.set_mode((1600, 1400))  # Increased width for the question
    pygame.display.set_caption("Physics Simulation with Question")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 9.8 * pixels_per_meter)  # Gravity in pixels/second^2 (9.8 m/s²)

    balls = []
    ground = add_ground(space)  # Add the ground to the simulation

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    font = pygame.font.Font(None, 36)  # Font for rendering text

    # Collision handler to detect when a ball hits the ground
    handler = space.add_collision_handler(0, 0)
    handler.begin = ball_hit_ground

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    if user_input == correct_answer:
                        print("Correct!")
                    else:
                        print("Incorrect. Try again.")
                else:
                    user_input += event.unicode  # Append new character

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        # Display the question and user input
        draw_text(screen, question, (610, 50), font)  # Adjust position for your layout
        #draw_text(screen, f"Answer: {user_input}", (610, 150), font)  # User input display

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()
