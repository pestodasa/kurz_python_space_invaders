"""
Wormy (a Nibbles clone)
By Al Sweigart al@inventwithpython.com
http://inventwithpython.com/pygame
Released under a "Simplified BSD" license
Modifications by Valdemar Svabensky valdemar@mail.muni.cz
"""

import sys, random, pygame
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Window height must be a multiple of cell size.'
NUM_CELLS_X = WINDOWWIDTH // CELLSIZE
NUM_CELLS_Y = WINDOWHEIGHT // CELLSIZE

BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)


def main():
    """Infinitely run the game."""
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    show_start_screen()
    while True:
        run_game()
        loser_screen()


def terminate():
    """Exit the program."""
    pygame.quit()
    sys.exit()


def was_key_pressed():
    """Exit game on QUIT event, or return True if key was pressed."""
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return False
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return True


def wait_for_key_pressed():
    """Wait for a player to press any key."""
    msg_surface = BASICFONT.render('Press a key to play.', True, GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(msg_surface, msg_rect)
    pygame.display.update()

    pygame.time.wait(500)  # Prevent player pressing a key too soon
    was_key_pressed()  # Clear any previous key presses in the event queue
    while True:
        if was_key_pressed():
            pygame.event.get()  # Clear event queue
            return


def show_start_screen():
    """Show a welcome screen at the first start of the game."""
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    wait_for_key_pressed()


def show_game_over_screen():
    """Show a game over screen when the player loses."""
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    wait_for_key_pressed()


def loser_screen ():
    loser_font = pygame. font.Font ('freesansbold.ttf',180)
    loser_surface = loser_font.render("Loser",True, GREEN)
    loser_rect = loser_surface.get_rect()
    loser_rect. center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.blit(loser_surface,loser_rect)
    wait_for_key_pressed()
    



    


def get_new_snake():
    """Set a random start point for a new snake and return its coordinates."""
    head_x = random.randint(5, NUM_CELLS_X - 6)  # Don't go too close the edge
    head_y = random.randint(5, NUM_CELLS_Y - 6)  # Don't go too close the edge
    snake = [(head_x, head_y), (head_x - 1, head_y), (head_x - 2, head_y)]
    direction = 'right'
    return (snake, direction)


def get_random_location():
    """Return a random cell on the game plan."""
    return (random.randint(0, NUM_CELLS_X - 1), random.randint(0, NUM_CELLS_Y - 1))


def run_game():
    """Main game logic. Return on game over."""
    snake, direction = get_new_snake()
    apple = get_random_location()
    while True:  # Main game loop
        for event in pygame.event.get():  # Event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a) and direction != 'right':
                    direction = 'left'
                elif event.key in (K_RIGHT, K_d) and direction != 'left':
                    direction = 'right'
                elif event.key in (K_UP, K_w) and direction != 'down':
                    direction = 'up'
                elif event.key in (K_DOWN, K_s) and direction != 'up':
                    direction = 'down'
                elif event.key == K_ESCAPE:
                    terminate()

        head_x, head_y = snake[0][0], snake[0][1]
        if head_x in (-1, NUM_CELLS_X) or head_y in (-1, NUM_CELLS_Y):
            return  # Game over, snake hit the edge
        for (body_x, body_y) in snake[1:]:
            if body_x == head_x and body_y == head_y:
                return  # Game over, snake hit itself

        if head_x == apple[0] and head_y == apple[1]:  # Apple was eaten
            apple = get_random_location()
        else:  # Simulate movement by removing the snake's tail
            del snake[-1]

        # Add a new segment in the direction the snake is moving
        if direction == 'up':
            new_head = (head_x, head_y - 1)
        elif direction == 'down':
            new_head = (head_x, head_y + 1)
        elif direction == 'left':
            new_head = (head_x - 1, head_y)
        elif direction == 'right':
            new_head = (head_x + 1, head_y)
        snake.insert(0, new_head)

        draw_game_state(snake, apple)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_game_state(snake, apple):
    """Draw the contents on the screen."""

    # Draw grid
    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

    # Draw snake
    for body_part in snake:
        x = body_part[0] * CELLSIZE
        y = body_part[1] * CELLSIZE
        outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
        pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)

    # Draw apple
    x = apple[0] * CELLSIZE
    y = apple[1] * CELLSIZE
    apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, apple_rect)

    # Draw score
    score_surface = BASICFONT.render('Score: ' + str(len(snake) - 3), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surface, score_rect)


if __name__ == '__main__':
    main()
