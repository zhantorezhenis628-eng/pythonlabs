import pygame
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Font for constants
pygame.font.init()

# Screen sizes
SW, SH = 600, 600  # playing area
WW, WH = 700, 700  # window size
BLOCK_SIZE = 40

# Fonts
FONT = pygame.font.SysFont("Arial", BLOCK_SIZE)
SMALL_FONT = pygame.font.SysFont("Arial", 20)

# States
MENU, GAME, GAME_OVER, LEADERBOARD, SETTINGS = range(5)

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
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

SETTINGS_FILE = 'settings.json'