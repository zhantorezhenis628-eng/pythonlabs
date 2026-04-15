
import pygame as pg
from datetime import datetime as dt
 
 
class MickeysClock:
    def __init__(self, screen, center, leftarm_surf, rightarm_surf):
        self.screen = screen
        self.center = center
        self.leftarm_surf  = leftarm_surf   # seconds
        self.rightarm_surf = rightarm_surf  # minutes
 
    def draw(self):
        current_time = dt.now().time()
 
        seconds_angle = -(current_time.second * 6)
        minutes_angle = -(current_time.minute * 6)
 
        rotated_left  = pg.transform.rotate(self.leftarm_surf,  seconds_angle)
        rotated_right = pg.transform.rotate(self.rightarm_surf, minutes_angle)
 
        left_rect  = rotated_left.get_rect(center=self.center)
        right_rect = rotated_right.get_rect(center=self.center)
 
        self.screen.blit(rotated_left,  left_rect)
        self.screen.blit(rotated_right, right_rect)
