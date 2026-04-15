
"""
Moving Ball Game
-----------------
Control a red ball with the arrow keys.
Each key press moves the ball 20 pixels.
The ball cannot leave the screen boundaries.
 
Controls:
  ↑ ↓ ← →  – Move ball
  ESC       – Quit
"""
 
import pygame
import sys
from ball import Ball
 
 
# ── Window settings ──────────────────────────────────────────────
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600
FPS           = 60
TITLE         = "Moving Ball Game"
 
# ── Colors ───────────────────────────────────────────────────────
BG_COLOR    = (245, 245, 245)    # White / near-white background
TEXT_COLOR  = (80, 80, 80)
 
 
def draw_instructions(screen, font):
    """Render a small instruction hint at the bottom of the screen."""
    text = "Arrow keys to move  |  ESC to quit"
    surf = font.render(text, True, TEXT_COLOR)
    rect = surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
    screen.blit(surf, rect)
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
 
    font = pygame.font.SysFont("segoeui", 16)
 
    # Create ball starting at center
    ball = Ball(WINDOW_WIDTH, WINDOW_HEIGHT)
 
    # ── Main loop ────────────────────────────────────────────────
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move_up()
                elif event.key == pygame.K_DOWN:
                    ball.move_down()
                elif event.key == pygame.K_LEFT:
                    ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    ball.move_right()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
 
        # ── Draw ─────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        ball.draw(screen)
        draw_instructions(screen, font)
        pygame.display.flip()
 
        clock.tick(FPS)
 
 
if __name__ == "__main__":
    main()