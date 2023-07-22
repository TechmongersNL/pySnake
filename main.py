import random
import pygame

# Colors
dark_green = (0, 51, 0)
green = (0, 204, 0)
dark_yellow = (204, 204, 0)
yellow = (255, 255, 0)
magenta = (255, 0, 127)
red = (153, 0, 0)

# Global Game Setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Codetrotters Snake Game Expedition')
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 30)
running = True
game_over = False
dt = 0


# Display a message (function)
def display_message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(message, [screen.get_width() / 3, screen.get_height() / 3])


def display_score(current_score):
    text = font_style.render("Score: %s Speed: %s" % (current_score, speed), True, green)
    screen.blit(text, [10, 10])


def spawn_food():
    return pygame.Vector2(random.randint(0, screen.get_width() - 10), random.randint(0, screen.get_height() - 10))


# Per-Game Setup
speed = 15
snake_head_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
food_position = None
xd = 0
yd = 0
score = 0
tail_length = 0
tail = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while game_over:
        screen.fill(red)
        display_message("Game Over! Press (Q)uit or (R)etry!", "white")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = False
                    running = False
                if event.key == pygame.K_r:
                    game_over = False

    # Reset the game
    speed = 10
    snake_head_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    xd = 0
    yd = 0
    score = 0
    tail_length = 0
    tail = []

    while running and not game_over:
        # Listen for arrow keys getting pressed by the player and set how
        # the X and Y coordinates should change (delta) as the snake is moving
        # in that direction.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    yd = -10
                    xd = 0
                if event.key == pygame.K_DOWN:
                    yd = +10
                    xd = 0
                if event.key == pygame.K_LEFT:
                    yd = 0
                    xd = -10
                if event.key == pygame.K_RIGHT:
                    yd = 0
                    xd = +10
                if event.key == pygame.K_q:
                    game_over = True
                    running = False

        # Update Tail
        tail.append(pygame.Vector2(snake_head_position.x + xd/speed, snake_head_position.y + yd/speed))
        if len(tail) > tail_length:
            tail.pop(0)

        # Change the snake head's position by applying the X and Y delta.
        snake_head_position.x += xd
        snake_head_position.y += yd

        if (snake_head_position.x < 0 or snake_head_position.x > screen.get_width() - 10 or
                snake_head_position.y < 0 or snake_head_position.y > screen.get_height() - 10):
            game_over = True

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(dark_green)

        display_score(score)

        # Welcome message
        if snake_head_position == pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2):
            display_message("START the game by using your arrow keys!", "white")

        # Spawn food
        if food_position is None:
            food_position = spawn_food()

        # Draw food
        food = pygame.draw.rect(screen, magenta, [food_position.x, food_position.y, 10, 10])

        # Draw head
        snake_head = pygame.draw.rect(screen, yellow, [snake_head_position.x, snake_head_position.y, 10, 10])

        # Draw tail
        for i, t in enumerate(tail):
            tail_color = dark_yellow
            if i % 2 == 0:
                tail_color = yellow

            part = pygame.draw.rect(screen, tail_color, [t.x, t.y, 10, 10])
            # Check if we ate our own tail!
            if tail_length > 1 and i < 1 and part.colliderect(snake_head):
                game_over = True

        # Eat food
        if food.colliderect(snake_head):
            tail_length += 1
            score += 1
            speed += 2
            food_position = spawn_food()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(speed)

pygame.quit()
