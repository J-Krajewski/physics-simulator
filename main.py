from FallingBodyQuestion import FallingBodyQuestion
from Question import Question

example_question = FallingBodyQuestion(5,2)

example_question.generate_values(True)

example_question.calculate_time()

example_question.choose_unknown()

print(example_question.get_question_text())




import sys, random, time, math
import pygame
import pymunk
import pymunk.pygame_util

## Conversion Factor
pixels_per_meter = 10  # 1 meter = 50 pixels

EARTH_GRAVITY = 9.80665


## Question Setup
floor_y_meters = example_question.get_floor_y()  # The height of the ground in meters
ball_mass = 3  # Mass of the ball in kg
ball_y_meters = example_question.get_ball_y()  # Initial height of the ball in meters
ball_x_meters = example_question.get_ball_x() # Initial x-position of the ball in meters

# Convert meters to pixels
floor_y_pixels = floor_y_meters * pixels_per_meter
ball_y_pixels = ball_y_meters * pixels_per_meter
ball_x_pixels = ball_x_meters * pixels_per_meter

# Set up the question and answer
question = example_question.get_question_text()
correct_answer = "0.45"  # Calculate based on physics, t = sqrt(2h/g)

def calc_time_in_air(height, gravity):
    time_in_air = math.sqrt(2 * height / gravity)
    print(time_in_air)
    return time_in_air

# To store the start time of each ball
ball_start_times = {}  # based on overall time

def add_ball(space):
    radius = 1 * pixels_per_meter  # Assuming the ball radius is 0.1 meters
    body = pymunk.Body()
    body.position = ball_x_pixels, ball_y_pixels
    shape = pymunk.Circle(body, radius)
    shape.mass = ball_mass
    shape.friction = 1
    space.add(body, shape)
    
    # Store the start time for this ball using its ID
    ball_alive = True
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
    global correct_answer, user_input, ball_is_alive

    # This function is called when the ball hits the ground
    if arbiter.is_first_contact:
        print("Ball hit the ground!")
        
        # Retrieve the ball shape involved in the collision
        ball_shape = arbiter.shapes[0]  # This is the shape of the ball
        
        # Calculate how long the ball was in the air
        start_time = ball_start_times.get(id(ball_shape))
        if start_time is not None:
            air_time = time.time() - start_time
            print(f"The ball was in the air for {air_time:.3f} seconds - error of {calculated_answer - air_time:.3f}")
        
        # Remove the ball from the space
        space.remove(ball_shape, ball_shape.body)
        ball_is_alive = False
        

    return True  # Return True to allow the physics simulation to proceed

def main():
    global user_input
    pygame.init()

    global calculated_answer
    calculated_answer = calc_time_in_air(floor_y_meters - ball_y_meters, gravity=EARTH_GRAVITY)
    
    
    screen = pygame.display.set_mode((800, 600))  # Adjusted height for the question
    pygame.display.set_caption("Physics Simulation with Question")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, EARTH_GRAVITY * pixels_per_meter)  # Gravity in pixels/second² (9.8 m/s²)

    balls = []
    ground = add_ground(space)  # Add the ground to the simulation

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    font = pygame.font.Font(None, 18)  # Font for rendering text
    
    ball_is_alive = False
    # Collision handler to detect when a ball hits the ground
    handler = space.add_collision_handler(0, 0)
    handler.begin = ball_hit_ground

    previous_time = pygame.time.get_ticks()
    ticks_to_next_ball = 10
    

    


    while True:
        if not ball_is_alive:
            ball_shape = add_ball(space)
            balls.append(ball_shape)
            ball_is_alive = True
        else:
            ball_is_alive = False


        current_time = pygame.time.get_ticks()
        delta_time = (current_time - previous_time) / 1000.0  # Convert milliseconds to seconds
        previous_time = current_time

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

        #ticks_to_next_ball -= 1
        #if ticks_to_next_ball <= 0 :
        #    ticks_to_next_ball = 25
        #    ball_shape = add_ball(space)
        #    balls.append(ball_shape)

        # Step the physics simulation with delta time
        space.step(delta_time)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        # Display the question and user input
        draw_text(screen, question, (0, 10), font)  # Adjust position for your layout
        #draw_text(screen, f"Answer: {user_input}", (610, 150), font)  # User input display

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()



