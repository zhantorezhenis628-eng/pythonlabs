import pygame
import json
import os
from config import *
from db import *
from game import *

# Initialize
pygame.init()
screen = pygame.display.set_mode((WW, WH))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# --- Load/Save Settings ---
settings = {'snake_color': [0, 255, 0], 'grid_overlay': True, 'sound': True}

def load_settings():
    global settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings.update(json.load(f))

def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def drawGrid():
    if settings['grid_overlay']:
        for x in range(0, SW, BLOCK_SIZE):
            for y in range(0, SH, BLOCK_SIZE):
                pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

load_settings()

# --- Initialize Global Objects ---
snake = None
apple = None
poison_apple = None
power_up = None
wall = None
golden_apple = None

score = 0
speed = 0
eaten_fruits = 0
level = 0
personal_best = 0
player_id = None

# UI elements
username_input = TextInput(WW//2 - 100, 170, 200, 30, "Enter username")
menu_buttons = [
    Button(WW//2 - 50, 250, 100, 40, "Play"),
    Button(WW//2 - 50, 300, 100, 40, "Leaderboard"),
    Button(WW//2 - 50, 350, 100, 40, "Settings"),
    Button(WW//2 - 50, 400, 100, 40, "Quit")
]

state = MENU
done = False

# --- Main Game Loop ---
while not done:
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    
    # 1. Event Handling
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        
        # Handle Text Input in Menu or Settings
        if state == MENU or state == SETTINGS:
            username_input.handle_event(event)

        # Handle Snake Movement
        if state == GAME and snake is not None and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.ydir != 1:
                snake.ydir, snake.xdir = -1, 0
            elif event.key == pygame.K_DOWN and snake.ydir != -1:
                snake.ydir, snake.xdir = 1, 0
            elif event.key == pygame.K_LEFT and snake.xdir != 1:
                snake.ydir, snake.xdir = 0, -1
            elif event.key == pygame.K_RIGHT and snake.xdir != -1:
                snake.ydir, snake.xdir = 0, 1

        # Handle Menu Clicks
        if state == MENU:
            for btn in menu_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(event):
                    if btn.text == "Play":
                        # CRITICAL: Only start if username is not empty
                        if username_input.text.strip():
                            player_id = get_or_create_player(username_input.text.strip())
                            personal_best = get_personal_best(player_id)
                            
                            # Create objects to START the game
                            snake = Snake()
                            apple = Apple()
                            wall = Wall()
                            poison_apple = PoisonApple()
                            power_up = PowerUp()
                            golden_apple = GoldenApple(snake.body, (apple.x, apple.y), [])
                            
                            score = speed = eaten_fruits = level = 0
                            state = GAME
                        else:
                            print("Please enter a username first!")
                            
                    elif btn.text == "Quit":
                        done = True

    # 2. Logic & Drawing
    screen.fill(BLACK)

    if state == MENU:
        title = FONT.render("Snake Game", True, WHITE)
        screen.blit(title, (WW//2 - title.get_width()//2, 50))
        username_input.draw(screen)
        for btn in menu_buttons:
            btn.draw(screen)

    elif state == GAME and snake is not None:
        # Update Game Logic
        snake.update(wall)
        
        # Collision: Apple
        if snake.head.colliderect(apple.rect):
            snake.growth_pending += 1
            apple = Apple()
            eaten_fruits += 1
            score += 1
            level = eaten_fruits // 2
            if len(snake.body) % 5 == 0: speed += 0.5

        # Collision: Golden Apple
        if golden_apple.golden_apple_rect and snake.head.colliderect(golden_apple.golden_apple_rect):
            snake.growth_pending += 1
            golden_apple = GoldenApple(snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)
            score += 3
            eaten_fruits += 1
            level = eaten_fruits // 2

        # Check for Game Over
        if snake.dead:
            save_game_session(player_id, score, level)
            state = GAME_OVER

        # Draw Game
        drawGrid()
        wall.update(screen, snake.body, (apple.x, apple.y), snake.head, eaten_fruits)
        apple.update(screen, snake.body, wall.static_barriers + wall.barriers)
        poison_apple.update(screen, snake.body, wall.static_barriers + wall.barriers)
        power_up.update(screen, snake.body, wall.static_barriers + wall.barriers)
        golden_apple.update(screen, snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)
        snake.draw(screen, settings['snake_color'])

        # Speed calculation
        now = pygame.time.get_ticks()
        if now < snake.speed_boost_end: game_speed = (5 + speed) * 1.5
        elif now < snake.slow_motion_end: game_speed = (5 + speed) * 0.5
        else: game_speed = 5 + speed
        
        clock.tick(game_speed)

    elif state == GAME_OVER:
        # Re-use buttons for Retry/Menu
        pass # Add your Game Over drawing here

    pygame.display.update()

pygame.quit()