import pygame
import sys
import player  # our player.py file

# ── Setup ─────────────────────────────────────────────────────────
# Initialize pygame and create the window
pygame.init()
screen = pygame.display.set_mode((500, 250))
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

# Font used to draw text on screen
font = pygame.font.SysFont("Arial", 22)

# ── Helper ────────────────────────────────────────────────────────
def draw_text(text, y, color=(255, 255, 255)):
    """Draw a centered text line at a given y position."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(250, y))
    screen.blit(surface, rect)

# ── Main loop ─────────────────────────────────────────────────────
while True:

    # 1. Handle events (key presses, window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:       # P = Play
                player.play()
            elif event.key == pygame.K_s:     # S = Stop
                player.stop()
            elif event.key == pygame.K_n:     # N = Next track
                player.next_track()
            elif event.key == pygame.K_b:     # B = Back (previous)
                player.prev_track()
            elif event.key == pygame.K_q:     # Q = Quit
                pygame.quit()
                sys.exit()

    # 2. Draw the background
    screen.fill((30, 30, 30))

    # 3. Draw track info and status on screen
    draw_text("MUSIC PLAYER", 50, color=(100, 220, 100))
    draw_text(player.current_name(), 110)
    draw_text(player.status(), 150, color=(180, 180, 180))
    draw_text("P=Play  S=Stop  N=Next  B=Back  Q=Quit", 210, color=(120, 120, 120))

    # 4. Update the display
    pygame.display.flip()
    clock.tick(30)
