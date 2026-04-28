import pygame
from collections import deque


# ─── Shape geometry ───────────────────────────────────────────────────────────

def get_rectangle(x1, y1, x2, y2):
    return (min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))


def get_circle(x1, y1, x2, y2):
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    r  = max(abs(x1 - x2), abs(y1 - y2)) // 2
    return cx, cy, r


def get_square(x1, y1, x2, y2):
    side = max(abs(x1 - x2), abs(y1 - y2))
    return (min(x1, x2), min(y1, y2), side, side)


def get_right_triangle(x1, y1, x2, y2):
    return [(x1, y1), (x1, y2), (x2, y2)]


def get_equilateral_triangle(x1, y1, x2, y2):
    x    = min(x1, x2)
    y    = min(y1, y2)
    side = max(abs(x1 - x2), abs(y1 - y2))
    return [(x, y + side), (x + side // 2, y), (x + side, y + side)]


def get_rhombus(x1, y1, x2, y2):
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    dx = abs(x1 - x2) // 2
    return [(cx, y1), (cx + dx, cy), (cx, y2), (cx - dx, cy)]


# ─── Flood fill ───────────────────────────────────────────────────────────────

def flood_fill(surface, x, y, new_color):
    """BFS flood fill: fills a contiguous region of the same colour with new_color."""
    w, h = surface.get_size()
    if not (0 <= x < w and 0 <= y < h):
        return

    target = surface.get_at((x, y))[:3]
    fill   = tuple(new_color[:3])
    if target == fill:
        return

    queue = deque([(x, y)])
    seen  = set()

    while queue:
        px, py = queue.popleft()
        if (px, py) in seen or not (0 <= px < w and 0 <= py < h):
            continue
        if surface.get_at((px, py))[:3] != target:
            continue
        seen.add((px, py))
        surface.set_at((px, py), fill)
        queue.extend([(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)])
