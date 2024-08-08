import sys, random
random.seed(1)  # Make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util

## Question Setup 

floor_y = 0
ball_mass = 3
ball_y = 50
ball_x = 120

# Set up the question and answer
question = f"If a ball of mass {ball_mass} is dropped from a height of {ball_y - floor_y}, how long is the ball in the air for? (in Newtons, assume g=9.8 m/s²)"
correct_answer = "3.2"  # The answer for mass = 3 kg and g = 9.8 m/s²
user_input = ""

def add_ball(space):
    
    radius = 25
    body = pymunk.Body()
    
    body.position = ball_x, ball_y
    shape = pymunk.Circle(body, radius)
    shape.mass = ball_mass
    shape.friction = 1
    space.add(body, shape)
    return shape

def draw_text(screen, text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def main():
    global user_input
    pygame.init()
    screen = pygame.display.set_mode((1600, 600))  # Increased width for the question
    pygame.display.set_caption("Physics Simulation with Question")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 900.0)

    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    font = pygame.font.Font(None, 36)  # Font for rendering text

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
                    user_input = ""  # Reset input after pressing Enter
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
        draw_text(screen, f"Answer: {user_input}", (610, 150), font)  # User input display

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()