import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Ball properties
BALL_RADIUS = 10

# Brick properties
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_PADDING = 5

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Function to create bricks for a level
def create_bricks(rows, cols):
    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick_x = col * (BRICK_WIDTH + BRICK_PADDING)
            brick_y = row * (BRICK_HEIGHT + BRICK_PADDING)
            brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    return bricks

# Game loop
def game_loop():
    level = 1
    running = True
    while running:
        # Initialize game objects for each level
        paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        ball_dx, ball_dy = 4 + level, -4 - level  # Ball speed increases with levels
        bricks = create_bricks(5 + level, 10)  # Increase rows with levels
        
        lives = 3
        score = 0

        while lives > 0:
            screen.fill(BLACK)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    lives = 0

            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.x -= PADDLE_SPEED
            if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.x += PADDLE_SPEED

            # Ball movement
            ball.x += ball_dx
            ball.y += ball_dy

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= WIDTH:
                ball_dx *= -1
            if ball.top <= 0:
                ball_dy *= -1

            # Ball collision with paddle
            if ball.colliderect(paddle):
                ball_dy *= -1

            # Ball collision with bricks
            for brick in bricks[:]:
                if ball.colliderect(brick):
                    bricks.remove(brick)
                    ball_dy *= -1
                    score += 10
                    break

            # Ball out of bounds
            if ball.top > HEIGHT:
                lives -= 1
                ball.x, ball.y = WIDTH // 2, HEIGHT // 2
                ball_dx, ball_dy = 4 + level, -4 - level

            # Draw paddle, ball, and bricks
            pygame.draw.rect(screen, BLUE, paddle)
            pygame.draw.ellipse(screen, RED, ball)
            for brick in bricks:
                pygame.draw.rect(screen, GREEN, brick)

            # Draw score and lives
            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 100, 10))
            screen.blit(level_text, (WIDTH // 2 - 50, 10))

            pygame.display.flip()

            # Check if all bricks are destroyed
            if not bricks:
                level += 1
                break

            clock.tick(60)

    pygame.quit()

# Run the game
game_loop()
