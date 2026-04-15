import pygame as pg
from clock import MickeysClock
 
pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("mickey mouse clock")
pg.display.set_icon(pg.image.load(r"icon.png"))
clock = pg.time.Clock()
 
bg_surf       = pg.image.load(r"mainclock.png")
leftarm_surf  = pg.image.load(r"leftarm.png")
rightarm_surf = pg.image.load(r"rightarm.png")
bg_rect = bg_surf.get_rect(center=(400, 400))
 
mickey = MickeysClock(screen, bg_rect.center, leftarm_surf, rightarm_surf)
 
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
 
    screen.blit(bg_surf, bg_rect)
    mickey.draw()
 
    pg.display.flip()
    clock.tick(60)