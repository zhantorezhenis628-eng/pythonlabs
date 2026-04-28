import pygame
import random
import os

LANES = [200, 300, 400] 
SPEED_BASE = 5

def load_image(name, width, height):
    path = os.path.join('assets', 'images', name)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except FileNotFoundError:
        surf = pygame.Surface((width, height))
        surf.fill((255, 0, 255)) 
        return surf

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        filename = f"player_{color_name}.png"
        self.image = load_image(filename, 40, 70)
        self.rect = self.image.get_rect(center=(300, 500))
        self.speed = 6
        self.shield_active = False
        self.nitro_active = False
        self.powerup_timer = 0
        self.crashes_allowed = 0
        

    def update(self):
        keys = pygame.key.get_pressed()
        current_speed = self.speed * 3 if self.nitro_active else self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.right < 450:
            self.rect.x += current_speed

        if (self.nitro_active or self.shield_active) and pygame.time.get_ticks() > self.powerup_timer:
            self.nitro_active = False
            self.shield_active = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        super().__init__()
        self.image = load_image("enemy.png", 40, 70)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        
        # Base speed with difficulty multiplier
        base_speed = SPEED_BASE + 2
        if difficulty == "easy":
            self.speed = int(base_speed * 0.8)
        elif difficulty == "normal":
            self.speed = base_speed
        elif difficulty == "hard":
            self.speed = int(base_speed * 1.3)
        else:
            self.speed = base_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["barrier", "oil_slick", "pothole", "speed_bump"])
        if self.type == "barrier":
            self.image = load_image("obstacle.png", 40, 40)
        elif self.type == "oil_slick":
            self.image = load_image("obstacle.png", 60, 20)  # Wider, flatter
            self.image.fill((0, 0, 100, 128))  # Dark blue tint
        elif self.type == "pothole":
            self.image = load_image("obstacle.png", 30, 30)
            self.image.fill((50, 50, 50, 128))  # Dark gray
        elif self.type == "speed_bump":
            self.image = load_image("obstacle.png", 80, 15)  # Long, thin
            self.image.fill((150, 150, 150, 128))  # Light gray
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        img_name = self.type.lower() + ".png"
        self.image = load_image(img_name, 30, 30)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("Coin.png", 25, 25)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))
        self.value = 10

    def update(self):
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()

class NitroStrip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300, 30))  # Wide strip across road
        self.image.fill((255, 165, 0))  # Orange color
        self.rect = self.image.get_rect(center=(300, -50))

    def update(self):
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()