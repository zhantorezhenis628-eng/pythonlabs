
import pygame
 
 
class Ball:
    """
    A red circle that moves in 20-pixel steps.
    Ignores any move that would take it outside the screen boundaries.
    """
 
    RADIUS    = 25          # 50×50 bounding box
    COLOR     = (220, 50, 50)
    STEP      = 20          # pixels per key press
 
    def __init__(self, screen_width, screen_height):
        self.screen_w = screen_width
        self.screen_h = screen_height
 
        # Start in the center of the screen
        self.x = screen_width  // 2
        self.y = screen_height // 2
 
    # ── Movement ─────────────────────────────────────────────────
 
    def _within_bounds(self, new_x, new_y):
        """Return True if (new_x, new_y) keeps the ball fully inside the screen."""
        r = self.RADIUS
        return (
            r <= new_x <= self.screen_w - r and
            r <= new_y <= self.screen_h - r
        )
 
    def move_up(self):
        new_y = self.y - self.STEP
        if self._within_bounds(self.x, new_y):
            self.y = new_y
 
    def move_down(self):
        new_y = self.y + self.STEP
        if self._within_bounds(self.x, new_y):
            self.y = new_y
 
    def move_left(self):
        new_x = self.x - self.STEP
        if self._within_bounds(new_x, self.y):
            self.x = new_x
 
    def move_right(self):
        new_x = self.x + self.STEP
        if self._within_bounds(new_x, self.y):
            self.x = new_x
 
    # ── Drawing ──────────────────────────────────────────────────
 
    def draw(self, screen):
        """Draw the ball on the given surface."""
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.RADIUS)
        # Subtle darker outline for depth
        pygame.draw.circle(screen, (160, 30, 30), (self.x, self.y), self.RADIUS, 2)