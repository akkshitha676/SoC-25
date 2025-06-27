import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
GRAY  = (200, 200, 200)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Arial', 25)
big_font = pygame.font.SysFont('Arial', 40)

# Helper functions
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

def draw_text(text, font, color, center):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)

def draw_button(text, rect, hover):
    color = GRAY if hover else WHITE
    pygame.draw.rect(screen, color, rect)
    draw_text(text, font, BLACK, rect.center)

def game_loop():
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)
    food = (random.randint(0, WIDTH//CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT//CELL_SIZE - 1) * CELL_SIZE)
    score = 0

    running = True
    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # Check collisions
        if (new_head in snake[1:] or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            return score  # End the game

        # Check food
        if new_head == food:
            score += 1
            food = (random.randint(0, WIDTH//CELL_SIZE - 1) * CELL_SIZE,
                    random.randint(0, HEIGHT//CELL_SIZE - 1) * CELL_SIZE)
        else:
            snake.pop()

        # Draw everything
        draw_snake(snake)
        draw_food(food)
        draw_text(f"Score: {score}", font, WHITE, (60, 20))

        pygame.display.update()
        clock.tick(FPS)

def start_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Snake Game", big_font, GREEN, (WIDTH // 2, HEIGHT // 4))

        start_btn = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 40)
        hover = start_btn.collidepoint(pygame.mouse.get_pos())
        draw_button("Start", start_btn, hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                return

        pygame.display.update()
        clock.tick(60)

def game_over_menu(score):
    while True:
        screen.fill(BLACK)
        draw_text("Game Over", big_font, RED, (WIDTH // 2, HEIGHT // 4))
        draw_text(f"Score: {score}", font, WHITE, (WIDTH // 2, HEIGHT // 2 - 40))

        restart_btn = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 20, 120, 40)
        hover = restart_btn.collidepoint(pygame.mouse.get_pos())
        draw_button("Restart", restart_btn, hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                return

        pygame.display.update()
        clock.tick(60)

# Main game loop
while True:
    start_menu()
    score = game_loop()
    game_over_menu(score)
