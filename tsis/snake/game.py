import pygame
import random
from config import *

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
        self.growth_pending = 0 

    def update(self, wall):
        # Check self and border collision
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                if not self.shield_active:
                    self.dead = True
                    self.death_reason = "Self collision"
                else: self.shield_active = False
        
        if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
            if not self.shield_active:
                self.dead = True
                self.death_reason = "Hit the border"
            else: self.shield_active = False

        # Check wall collision
        for barrier in wall.static_barriers + wall.barriers:
            if self.head.colliderect(barrier):
                if not self.shield_active:
                    self.dead = True
                    self.death_reason = "Collision with wall"
                else: self.shield_active = False

        if not self.dead:
            # Move head
            self.head.x += self.xdir * BLOCK_SIZE
            self.head.y += self.ydir * BLOCK_SIZE
            
            # Handle growth exactly like original
            if self.growth_pending > 0:
                self.body.insert(0, pygame.Rect(self.head.x - self.xdir * BLOCK_SIZE, 
                                                self.head.y - self.ydir * BLOCK_SIZE, 
                                                BLOCK_SIZE, BLOCK_SIZE))
                self.growth_pending -= 1
            elif len(self.body) > 0:
                for i in range(len(self.body) - 1, 0, -1):
                    self.body[i].x = self.body[i-1].x
                    self.body[i].y = self.body[i-1].y
                self.body[0].x = self.head.x - self.xdir * BLOCK_SIZE
                self.body[0].y = self.head.y - self.ydir * BLOCK_SIZE

    def draw(self, screen, snake_color):
        pygame.draw.rect(screen, snake_color, self.head)
        for square in self.body:
            pygame.draw.rect(screen, [c//2 for c in snake_color], square)

class Apple:
    def __init__(self):
        self.spawn_apple()
        self.spawn_time = pygame.time.get_ticks()

    def spawn_apple(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self, screen, snake_body, barriers):
        if pygame.time.get_ticks() - self.spawn_time >= 5000:
            self.spawn_apple()
            self.spawn_time = pygame.time.get_ticks()
        while (self.x, self.y) in [(s.x, s.y) for s in snake_body] or \
              (self.x, self.y) in [(b.x, b.y) for b in barriers]:
            self.spawn_apple()
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, "red", self.rect)

class PoisonApple:
    def __init__(self):
        self.rect = None
        self.spawn_time = 0
        if random.random() < 0.3: self.spawn_poison()

    def spawn_poison(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, screen, snake_body, barriers):
        current_time = pygame.time.get_ticks()
        if self.rect and current_time - self.spawn_time > 8000:
            self.rect = None
        elif not self.rect and random.random() < 0.3:
            self.spawn_poison()
            while (self.x, self.y) in [(s.x, s.y) for s in snake_body] or \
                  (self.x, self.y) in [(b.x, b.y) for b in barriers]:
                self.spawn_poison()
        if self.rect:
            pygame.draw.rect(screen, PURPLE, self.rect)

class PowerUp:
    def __init__(self):
        self.rect = None
        self.type = None
        self.spawn_time = 0

    def spawn_powerup(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.type = random.choice(['speed', 'slow', 'shield'])
        self.spawn_time = pygame.time.get_ticks()

    def update(self, screen, snake_body, barriers):
        current_time = pygame.time.get_ticks()
        if self.rect and current_time - self.spawn_time > 8000:
            self.rect = None
        elif not self.rect and random.random() < 0.2:
            self.spawn_powerup()
        if self.rect:
            color = ORANGE if self.type == 'speed' else CYAN if self.type == 'slow' else WHITE
            pygame.draw.rect(screen, color, self.rect)

class GoldenApple:
    def __init__(self, snake_body, apple_pos, barriers):
        self.spawn_time = pygame.time.get_ticks()
        self.golden_apple_rect = None
        if random.random() <= 0.1: self.spawn_golden_apple(snake_body, apple_pos, barriers)

    def spawn_golden_apple(self, snake_body, apple_pos, barriers):
        while True:
            self.x = int(random.randint(0, SW-BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SH-BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            if (self.x, self.y) != apple_pos and \
               (self.x, self.y) not in [(s.x, s.y) for s in snake_body] and \
               (self.x, self.y) not in [(b.x, b.y) for b in barriers]:
                self.golden_apple_rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                break

    def update(self, screen, snake_body, apple_pos, barriers):
        current_time = pygame.time.get_ticks()
        if self.golden_apple_rect:
            if current_time - self.spawn_time >= 3000:
                self.golden_apple_rect = None
        else:
            if random.random() <= 0.1:
                self.spawn_golden_apple(snake_body, apple_pos, barriers)
                self.spawn_time = current_time
        if self.golden_apple_rect:
            pygame.draw.rect(screen, GOLD, self.golden_apple_rect)

class Wall:
    def __init__(self):
        self.barriers = []
        self.static_barriers = []

    def spawn_static_barriers(self, level, snake_body, snake_head):
        if level >= 3:
            num_barriers = level - 2
            for _ in range(num_barriers):
                while True:
                    x = int(random.randint(0, SW-BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                    y = int(random.randint(0, SH-BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                    new_barrier = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    if new_barrier.collidelist(snake_body) == -1 and \
                       abs(snake_head.x - x) > 3 * BLOCK_SIZE:
                        self.static_barriers.append(new_barrier)
                        break

    def spawn_barrier(self, snake_body, apple_pos, snake_head_pos):
        while True:
            x = int(random.randint(0, SW-BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            y = int(random.randint(0, SH-BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            new_barrier = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if new_barrier.collidelist(snake_body) == -1 and not new_barrier.collidepoint(apple_pos):
                if abs(snake_head_pos[0] - x) > 3 * BLOCK_SIZE:
                    self.barriers.append(new_barrier)
                    break

    def update(self, screen, snake_body, apple_pos, snake_head_pos, eaten_fruits):
        level = eaten_fruits // 2
        if not self.static_barriers and level >= 3:
            self.spawn_static_barriers(level, snake_body, snake_head_pos)
        
        for barrier in self.static_barriers + self.barriers:
            pygame.draw.rect(screen, BLUE, barrier)

        target_barriers = eaten_fruits // 2
        if target_barriers > len(self.barriers):
            for _ in range(target_barriers - len(self.barriers)):
                self.spawn_barrier(snake_body, apple_pos, (snake_head_pos.x, snake_head_pos.y))

# (Keep Button and TextInput classes here from previous version)

# Bottom of game.py

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
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

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
        screen.blit(rendered, (self.rect.x + 5, self.rect.centery - rendered.get_height()//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 50: # The fix for your DB truncation error
                self.text += event.unicode