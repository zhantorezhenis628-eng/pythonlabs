import pygame
import random
import json
import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()

pygame.init()

SW, SH = 600, 600  # screen size(playing area)
WW, WH = 700, 700  # window size

BLOCK_SIZE = 40
FONT = pygame.font.SysFont("Arial", BLOCK_SIZE)
SMALL_FONT = pygame.font.SysFont("Arial", 20)

screen = pygame.display.set_mode((WW, WH))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# States
MENU = 0
GAME = 1
GAME_OVER = 2
LEADERBOARD = 3
SETTINGS = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 65, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 140, 0)
CYAN = (0, 255, 255)
# MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# Settings file
SETTINGS_FILE = 'settings.json'

# Default settings
default_settings = {
    'snake_color': [0, 255, 0],
    'grid_overlay': True,
    'sound': True
}

settings = default_settings.copy()

def load_settings():
    global settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings.update(json.load(f))

def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

load_settings()

def db_connect():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

def get_or_create_player(username):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()
    if not player:
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
    else:
        player_id = player[0]
    cur.close()
    conn.close()
    return player_id

def save_game_session(player_id, score, level_reached):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level_reached))
    conn.commit()
    cur.close()
    conn.close()

def get_top_scores():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    top_scores = cur.fetchall()
    cur.close()
    conn.close()
    return top_scores

def get_personal_best(player_id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    pb = cur.fetchone()[0]
    cur.close()
    conn.close()
    return pb or 0

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
        self.restart = False
        self.speed_boost_end = 0
        self.slow_motion_end = 0
        self.shield_active = False
        self.death_reason = ""
        self.growth_pending = 0  # Track pending growth segments

    def update(self):
        global apple, poison_apple, power_up, wall, golden_apple

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                if not self.shield_active:
                    self.dead = True
                    self.death_reason = "Self collision"
                else:
                    self.shield_active = False
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                if not self.shield_active:
                    self.dead = True
                    self.death_reason = "Hit the border"
                else:
                    self.shield_active = False

        # Check wall collision
        for barrier in wall.static_barriers + wall.barriers:
            if self.head.colliderect(barrier):
                if not self.shield_active:
                    self.dead = True
                    self.death_reason = "Collision with wall"
                else:
                    self.shield_active = False

        if self.dead and self.restart:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            self.restart = False
            self.speed_boost_end = 0
            self.slow_motion_end = 0
            self.shield_active = False
            self.death_reason = ""            
            apple = Apple()
            poison_apple = PoisonApple()
            power_up = PowerUp()
            wall = Wall()
            golden_apple = GoldenApple(self.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)

        if not self.dead:
            # Move head first
            self.head.x += self.xdir * BLOCK_SIZE
            self.head.y += self.ydir * BLOCK_SIZE
            
            # Handle body growth/shrinkage
            if self.growth_pending > 0:
                # Add new segment at old head position
                self.body.insert(0, pygame.Rect(self.head.x - self.xdir * BLOCK_SIZE, 
                                                self.head.y - self.ydir * BLOCK_SIZE, 
                                                BLOCK_SIZE, BLOCK_SIZE))
                self.growth_pending -= 1
            elif len(self.body) > 0:
                # Shift body forward
                for i in range(len(self.body) - 1, 0, -1):
                    self.body[i].x = self.body[i-1].x
                    self.body[i].y = self.body[i-1].y
                # Update first body segment to follow head
                self.body[0].x = self.head.x - self.xdir * BLOCK_SIZE
                self.body[0].y = self.head.y - self.ydir * BLOCK_SIZE

    def draw(self):
        pygame.draw.rect(screen, settings['snake_color'], self.head)
        for square in self.body:
            pygame.draw.rect(screen, [c//2 for c in settings['snake_color']], square)

class Apple:
    def __init__(self):
        self.spawn_apple()
        self.spawn_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def spawn_apple(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self, snake_body, barriers):
        if pygame.time.get_ticks() - self.spawn_time >= 5000:
            self.spawn_apple()
            self.spawn_time = pygame.time.get_ticks()
        while (self.x, self.y) in [(square.x, square.y) for square in snake_body] or \
              (self.x, self.y) in [(b.x, b.y) for b in barriers]:
            self.spawn_apple()
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, "red", self.rect)

class PoisonApple:
    def __init__(self):
        self.rect = None
        self.spawn_time = 0
        if random.random() < 0.3:  # 30% chance
            self.spawn_poison()

    def spawn_poison(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, snake_body, barriers):
        current_time = pygame.time.get_ticks()
        if self.rect and current_time - self.spawn_time > 8000:  # Despawn after 8s
            self.rect = None
        elif not self.rect and random.random() < 0.3:
            self.spawn_poison()
            while (self.x, self.y) in [(square.x, square.y) for square in snake_body] or \
                  (self.x, self.y) in [(b.x, b.y) for b in barriers]:
                self.spawn_poison()
        if self.rect:
            pygame.draw.rect(screen, PURPLE, self.rect)

class PowerUp:
    def __init__(self):
        self.rect = None
        self.type = None  # 'speed', 'slow', 'shield'
        self.spawn_time = 0

    def spawn_powerup(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.type = random.choice(['speed', 'slow', 'shield'])
        self.spawn_time = pygame.time.get_ticks()

    def update(self, snake_body, barriers):
        current_time = pygame.time.get_ticks()
        if self.rect and current_time - self.spawn_time > 8000:  # Despawn after 8s
            self.rect = None
        elif not self.rect and random.random() < 0.2:  # 20% chance
            self.spawn_powerup()
            while (self.x, self.y) in [(square.x, square.y) for square in snake_body] or \
                  (self.x, self.y) in [(b.x, b.y) for b in barriers]:
                self.spawn_powerup()
        if self.rect:
            color = ORANGE if self.type == 'speed' else CYAN if self.type == 'slow' else WHITE
            pygame.draw.rect(screen, color, self.rect)

class GoldenApple:
    def __init__(self, snake_body, apple_pos, barriers):
        self.spawn_time = pygame.time.get_ticks()
        self.golden_apple_rect = None
        if random.random() <= 0.1:
            self.spawn_golden_apple(snake_body, apple_pos, barriers)

    def spawn_golden_apple(self, snake_body, apple_pos, barriers):
        while True:
            self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
            if (self.x, self.y) not in apple_pos and \
               (self.x, self.y) not in [(square.x, square.y) for square in snake_body] and \
               (self.x, self.y) not in [(b.x, b.y) for b in barriers]:
                self.golden_apple_rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                break

    def update(self, snake_body, apple_pos, barriers):
        current_time = pygame.time.get_ticks()
        if self.golden_apple_rect is not None:
            if current_time - self.spawn_time >= 3000:
                self.golden_apple_rect = None
        else:
            if random.random() <= 0.1:
                self.spawn_golden_apple(snake_body, apple_pos, barriers)
                self.spawn_time = current_time
        if self.golden_apple_rect is not None:
            pygame.draw.rect(screen, "gold", self.golden_apple_rect)

class Wall:
    def __init__(self):
        self.barriers = []
        self.static_barriers = []

    def spawn_static_barriers(self, level, snake_body, snake_head):
        if level >= 3:
            num_barriers = level - 2  # Increase with level
            for _ in range(num_barriers):
                while True:
                    x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
                    y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
                    new_barrier = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    if new_barrier.collidelist(snake_body) == -1 and \
                       abs(snake_head.x - x) > 3 * BLOCK_SIZE or abs(snake_head.y - y) > 3 * BLOCK_SIZE:
                        # Check not trapping
                        # Simple check: ensure path exists, but for simplicity, just place randomly
                        self.static_barriers.append(new_barrier)
                        break

    def spawn_barrier(self, snake_body, apple_pos, snake_head_pos):
        while True:
            self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
            new_barrier = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            if new_barrier.collidelist(snake_body) == -1 and new_barrier.collidepoint(apple_pos) == False and \
               new_barrier.collidelist(self.static_barriers) == -1:
                if abs(snake_head_pos[0] - new_barrier.x) > 3 * BLOCK_SIZE or abs(snake_head_pos[1] - new_barrier.y) > 3 * BLOCK_SIZE:
                    self.barriers.append(new_barrier)
                    break

    def update(self, snake_body, apple_pos, snake_head_pos, eaten_fruits):
        level = eaten_fruits // 2
        if not self.static_barriers and level >= 3:
            self.spawn_static_barriers(level, snake_body, snake_head_pos)

        for barrier in self.static_barriers + self.barriers:
            pygame.draw.rect(screen, "blue", barrier)

        eaten_fruits = eaten_fruits // 2
        if eaten_fruits > len(self.barriers):
            for _ in range(eaten_fruits - len(self.barriers)):
                self.spawn_barrier(snake_body, apple_pos, snake_head_pos)
def drawGrid():
    if settings['grid_overlay']:
        for x in range(0, SW, BLOCK_SIZE):
            for y in range(0, SH, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, (60, 60, 60), rect, 1)

class Button:
    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        txt = SMALL_FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + (self.rect.width - txt.get_width()) // 2,
                          self.rect.y + (self.rect.height - txt.get_height()) // 2))

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.hovered

class TextInput:
    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        txt = self.text if self.text else self.placeholder
        color = BLACK if self.text else GRAY
        rendered = SMALL_FONT.render(txt, True, color)
        screen.blit(rendered, (self.rect.x + 5, self.rect.y + (self.rect.height - rendered.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            else:
                self.text += event.unicode
        return False

def draw_menu(username_input, buttons):
    screen.fill(BLACK)
    title = FONT.render("Snake Game", True, WHITE)
    screen.blit(title, (WW//2 - title.get_width()//2, 50))

    user_label = SMALL_FONT.render("Username:", True, WHITE)
    screen.blit(user_label, (WW//2 - 100, 150))
    username_input.draw(screen)

    for btn in buttons:
        btn.draw(screen)

def handle_menu(events, username_input, buttons):
    for event in events:
        if username_input.handle_event(event):
            pass
        for btn in buttons:
            if btn.is_clicked(event):
                return btn.text.lower()
    return None

def draw_game(snake, apple, poison_apple, power_up, wall, golden_apple, score, display_speed, level, personal_best):
    screen.fill(BLACK)
    drawGrid()
    wall.update(snake.body, (apple.x, apple.y), snake.head, eaten_fruits)
    apple.update(snake.body, wall.static_barriers + wall.barriers)
    poison_apple.update(snake.body, wall.static_barriers + wall.barriers)
    power_up.update(snake.body, wall.static_barriers + wall.barriers)
    golden_apple.update(snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)
    snake.draw()

    # Stats
    pygame.draw.rect(screen, (42, 42, 42), [0, SH, WW, WH - SH])
    scoretxt = FONT.render(f"Score: {score}", True, WHITE)
    speedtxt = FONT.render(f"Speed: {display_speed:.1f}", True, WHITE)
    leveltxt = FONT.render(f"Level: {level}", True, WHITE)
    pbtxt = FONT.render(f"PB: {personal_best}", True, WHITE)
    screen.blit(scoretxt, (20, 620))
    screen.blit(speedtxt, (20, 660))
    screen.blit(leveltxt, (480, 620))
    screen.blit(pbtxt, (480, 660))

def draw_game_over(score, level, personal_best, death_reason, buttons):
    screen.fill(BLACK)
    endtxt = FONT.render(f"Game Over", True, RED)
    scoretxt = FONT.render(f"Score: {score}", True, WHITE)
    leveltxt = FONT.render(f"Level: {level}", True, WHITE)
    pbtxt = FONT.render(f"Personal Best: {personal_best}", True, WHITE)
    deathtxt = SMALL_FONT.render(f"Reason: {death_reason}", True, GOLD)
    screen.blit(endtxt, (WW//2 - endtxt.get_width()//2, 200))
    screen.blit(scoretxt, (WW//2 - scoretxt.get_width()//2, 250))
    screen.blit(leveltxt, (WW//2 - leveltxt.get_width()//2, 300))
    screen.blit(pbtxt, (WW//2 - pbtxt.get_width()//2, 350))
    screen.blit(deathtxt, (WW//2 - deathtxt.get_width()//2, 400))
    for btn in buttons:
        btn.draw(screen)

def handle_game_over(events, buttons):
    for event in events:
        for btn in buttons:
            if btn.is_clicked(event):
                return btn.text.lower()
    return None

def draw_leaderboard(top_scores, back_btn):
    screen.fill(BLACK)
    title = FONT.render("Leaderboard", True, WHITE)
    screen.blit(title, (WW//2 - title.get_width()//2, 50))

    y = 120
    header = SMALL_FONT.render("Rank  Username  Score  Level  Date", True, WHITE)
    screen.blit(header, (50, y))
    y += 30
    for i, (user, sc, lv, dt) in enumerate(top_scores, 1):
        txt = SMALL_FONT.render(f"{i}      {user}      {sc}      {lv}      {dt.strftime('%Y-%m-%d')}", True, WHITE)
        screen.blit(txt, (50, y))
        y += 25

    back_btn.draw(screen)

def handle_leaderboard(events, back_btn):
    for event in events:
        if back_btn.is_clicked(event):
            return "back"
    return None

def draw_settings(grid_toggle, sound_toggle, color_input, save_btn):
    screen.fill(BLACK)
    title = FONT.render("Settings", True, WHITE)
    screen.blit(title, (WW//2 - title.get_width()//2, 50))

    grid_label = SMALL_FONT.render("Grid Overlay:", True, WHITE)
    screen.blit(grid_label, (100, 150))
    grid_toggle.draw(screen)

    sound_label = SMALL_FONT.render("Sound:", True, WHITE)
    screen.blit(sound_label, (100, 200))
    sound_toggle.draw(screen)

    color_label = SMALL_FONT.render("Snake Color (R,G,B):", True, WHITE)
    screen.blit(color_label, (100, 250))
    color_input.draw(screen)

    save_btn.draw(screen)

def handle_settings(events, grid_toggle, sound_toggle, color_input, save_btn):
    for event in events:
        if color_input.handle_event(event):
            pass
        if grid_toggle.is_clicked(event):
            settings['grid_overlay'] = not settings['grid_overlay']
            grid_toggle.text = "Grid On" if settings['grid_overlay'] else "Grid Off"
        if sound_toggle.is_clicked(event):
            settings['sound'] = not settings['sound']
            sound_toggle.text = "Sound On" if settings['sound'] else "Sound Off"
        if save_btn.is_clicked(event):
            try:
                r, g, b = map(int, color_input.text.split(','))
                settings['snake_color'] = [r, g, b]
            except:
                pass
            save_settings()
            return "save"
    return None

    return None

# Initialize game variables
score = speed = eaten_fruits = 0
level = 0
personal_best = 0
player_id = None
username = ""

# Initialize objects
snake = Snake()
apple = Apple()
poison_apple = PoisonApple()
power_up = PowerUp()
wall = Wall()
golden_apple = GoldenApple(snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)

# UI elements
username_input = TextInput(WW//2 - 50, 170, 200, 30, "Enter username")
menu_buttons = [
    Button(WW//2 - 50, 250, 100, 40, "Play"),
    Button(WW//2 - 50, 300, 100, 40, "Leaderboard"),
    Button(WW//2 - 50, 350, 100, 40, "Settings"),
    Button(WW//2 - 50, 400, 100, 40, "Quit")
]
game_over_buttons = [
    Button(WW//2 - 100, 450, 80, 40, "Retry"),
    Button(WW//2 + 20, 450, 80, 40, "Main Menu")
]
back_btn = Button(WW//2 - 50, 600, 100, 40, "Back")
grid_toggle = Button(300, 140, 100, 40, "Toggle Grid")
sound_toggle = Button(300, 190, 100, 40, "Toggle Sound")
color_input = TextInput(300, 240, 150, 30, "0,255,0")
save_btn = Button(WW//2 - 50, 350, 100, 40, "Save & Back")

state = MENU
done = False

while not done:
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            done = True

    if state == MENU:
        for btn in menu_buttons:
            btn.update(mouse_pos)
        action = handle_menu(events, username_input, menu_buttons)
        if action == "play":
            if username_input.text:
                username = username_input.text
                player_id = get_or_create_player(username)
                personal_best = get_personal_best(player_id)
                state = GAME
                # Reset game
                score = speed = eaten_fruits = level = 0
                snake = Snake()
                apple = Apple()
                poison_apple = PoisonApple()
                power_up = PowerUp()
                wall = Wall()
                golden_apple = GoldenApple(snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)
        elif action == "leaderboard":
            top_scores = get_top_scores()
            state = LEADERBOARD
        elif action == "settings":
            color_input.text = ','.join(map(str, settings['snake_color']))
            state = SETTINGS
        elif action == "quit":
            done = True
        draw_menu(username_input, menu_buttons)

    elif state == GAME:
        # Handle keys
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and snake.ydir != -1:
                    snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pygame.K_UP and snake.ydir != 1:
                    snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pygame.K_RIGHT and snake.xdir != -1:
                    snake.ydir = 0
                    snake.xdir = 1
                elif event.key == pygame.K_LEFT and snake.xdir != 1:
                    snake.ydir = 0
                    snake.xdir = -1

        snake.update()

        # Check collisions
        if snake.head.colliderect(apple.rect):
            snake.growth_pending += 1
            apple = Apple()
            eaten_fruits += 1
            score += 1
            level = eaten_fruits // 2
            if len(snake.body) % 5 == 0:
                speed += 0.5

        if golden_apple.golden_apple_rect and snake.head.colliderect(golden_apple.golden_apple_rect):
            snake.growth_pending += 1
            golden_apple = GoldenApple(snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)
            eaten_fruits += 1
            score += 3
            level = eaten_fruits // 2
            if len(snake.body) % 5 == 0:
                speed += 0.5

        if poison_apple.rect and snake.head.colliderect(poison_apple.rect):
            for _ in range(2):
                if snake.body:
                    snake.body.pop()
            if len(snake.body) < 1:
                snake.dead = True
                snake.death_reason = "Ate poison food"
            poison_apple.rect = None

        if power_up.rect and snake.head.colliderect(power_up.rect):
            current_time = pygame.time.get_ticks()
            if power_up.type == 'speed':
                snake.speed_boost_end = current_time + 5000
            elif power_up.type == 'slow':
                snake.slow_motion_end = current_time + 5000
            elif power_up.type == 'shield':
                snake.shield_active = True
            power_up.rect = None

        # Update power-ups
        current_time = pygame.time.get_ticks()
        if snake.speed_boost_end > current_time:
            game_speed = (5 + speed) * 1.5
        elif snake.slow_motion_end > current_time:
            game_speed = (5 + speed) * 0.5
        else:
            game_speed = 5 + speed

        if snake.dead:
            save_game_session(player_id, score, level)
            state = GAME_OVER

        draw_game(snake, apple, poison_apple, power_up, wall, golden_apple, score, game_speed, level, personal_best)
        clock.tick(game_speed)

    elif state == GAME_OVER:
        for btn in game_over_buttons:
            btn.update(mouse_pos)
        action = handle_game_over(events, game_over_buttons)
        if action == "retry":
            state = GAME
            score = speed = eaten_fruits = level = 0
            snake = Snake()
            apple = Apple()
            poison_apple = PoisonApple()
            power_up = PowerUp()
            wall = Wall()
            golden_apple = GoldenApple(snake.body, (apple.x, apple.y), wall.static_barriers + wall.barriers)
        elif action == "main menu":
            state = MENU
        draw_game_over(score, level, personal_best, snake.death_reason, game_over_buttons)

    elif state == LEADERBOARD:
        back_btn.update(mouse_pos)
        action = handle_leaderboard(events, back_btn)
        if action == "back":
            state = MENU
        draw_leaderboard(top_scores, back_btn)

    elif state == SETTINGS:
        grid_toggle.text = "Grid On" if settings['grid_overlay'] else "Grid Off"
        sound_toggle.text = "Sound On" if settings['sound'] else "Sound Off"
        color_input.text = ','.join(map(str, settings['snake_color']))
        grid_toggle.update(mouse_pos)
        sound_toggle.update(mouse_pos)
        save_btn.update(mouse_pos)
        action = handle_settings(events, grid_toggle, sound_toggle, color_input, save_btn)
        if action == "save":
            state = MENU
        draw_settings(grid_toggle, sound_toggle, color_input, save_btn)

    pygame.display.update()

pygame.quit()
