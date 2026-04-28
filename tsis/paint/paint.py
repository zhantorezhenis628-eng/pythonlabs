import pygame
import datetime

# Note: Ensure tools.py is in the same directory for imports to work
from tools import (get_rectangle, get_circle, get_square,
                    get_right_triangle, get_equilateral_triangle,
                    get_rhombus, flood_fill)

# ─── Constants ────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 800, 700
MENU_H         = 115          
FPS            = 60

BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)
BLUE   = (  0,   0, 255)
BROWN  = (156,  42,  42)
PURPLE = (128,   0, 128)
PINK   = (255, 192, 203)
GREEN  = (  0, 255,   0)
WHITE  = (255, 255, 255)

PALETTE      = [BLACK, RED, YELLOW, BLUE, BROWN, PURPLE, PINK, GREEN]
BRUSH_SIZES  = [2, 5, 10]  # Small, Medium, Large
BRUSH_LABELS = ['S', 'M', 'L']

# Tool IDs
RECT=0; CIRCLE=1; SQUARE=2; RTRI=3; EQTRI=4
RHOMBUS=5; PENCIL=6; LINE=7; FILL=8; TEXT=9

# ─── Pygame setup ─────────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Paint - [1,2,3] or [Up/Down] for Brush Size')
clock  = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))   
canvas.fill(WHITE)

font_ui   = pygame.font.SysFont('arial', 12, bold=True)
font_text = pygame.font.SysFont('arial', 22)

# Load clear icon - wrapped in try/except in case asset is missing
try:
    clear_icon = pygame.image.load(r"assets/clear.png")
    clear_icon = pygame.transform.scale(clear_icon, (38, 38))
except:
    clear_icon = pygame.Surface((38, 38))
    clear_icon.fill((200, 0, 0))

# ─── Toolbar geometry ─────────────────────────────────────────────────────────
_B, _G = 44, 3 
TOOL_RECTS = {}
for _row, _tools in enumerate([[RECT, CIRCLE, SQUARE, RTRI, EQTRI],
                                [RHOMBUS, PENCIL, LINE, FILL, TEXT]]):
    for _col, _tid in enumerate(_tools):
        TOOL_RECTS[_tid] = pygame.Rect(5 + _col * (_B + _G),
                                        5 + _row * (_B + 20), _B, _B)

_BRX        = 5 + 5 * (_B + _G) + 8      
BRUSH_RECTS = [pygame.Rect(_BRX + i * (_B + _G), 5, _B, _B) for i in range(3)]

SWATCH_RECT = pygame.Rect(400, 5, 60, 108)   
CLEAR_RECT  = pygame.Rect(475, 38, 38, 38)   

COLOR_RECTS = []
for _i in range(8):
    _r, _c = divmod(_i, 4)
    COLOR_RECTS.append(pygame.Rect(635 + _c * 37, 8 + _r * 57, 34, 34))

# ─── Drawing helper ───────────────────────────────────────────────────────────
def draw_shape(surface, tid, clr, thick, ax1, ay1, ax2, ay2):
    if ax1 == ax2 and ay1 == ay2:
        return
    if tid == RECT:
        pygame.draw.rect(surface, clr, get_rectangle(ax1, ay1, ax2, ay2), thick)
    elif tid == CIRCLE:
        cx, cy, r = get_circle(ax1, ay1, ax2, ay2)
        if r > 0:
            pygame.draw.circle(surface, clr, (cx, cy), r, thick)
    elif tid == SQUARE:
        pygame.draw.rect(surface, clr, get_square(ax1, ay1, ax2, ay2), thick)
    elif tid == RTRI:
        pygame.draw.polygon(surface, clr, get_right_triangle(ax1, ay1, ax2, ay2), thick)
    elif tid == EQTRI:
        pygame.draw.polygon(surface, clr, get_equilateral_triangle(ax1, ay1, ax2, ay2), thick)
    elif tid == RHOMBUS:
        pygame.draw.polygon(surface, clr, get_rhombus(ax1, ay1, ax2, ay2), thick)
    elif tid == LINE:
        pygame.draw.line(surface, clr, (ax1, ay1), (ax2, ay2), thick)

# ─── Toolbar rendering ────────────────────────────────────────────────────────
def _tool_icon(tid, cx, cy):
    if tid == RECT:
        pygame.draw.rect(screen, BLACK, (cx - 14, cy - 9, 28, 18), 2)
    elif tid == CIRCLE:
        pygame.draw.circle(screen, BLACK, (cx, cy), 16, 2)
    elif tid == SQUARE:
        pygame.draw.rect(screen, BLACK, (cx - 13, cy - 13, 26, 26), 2)
    elif tid == RTRI:
        pygame.draw.polygon(screen, BLACK,
                            [(cx - 13, cy + 12), (cx - 13, cy - 12), (cx + 13, cy + 12)], 2)
    elif tid == EQTRI:
        pygame.draw.polygon(screen, BLACK,
                            [(cx, cy - 13), (cx - 13, cy + 12), (cx + 13, cy + 12)], 2)
    elif tid == RHOMBUS:
        pygame.draw.polygon(screen, BLACK,
                            [(cx, cy - 14), (cx + 13, cy), (cx, cy + 14), (cx - 13, cy)], 2)
    elif tid == LINE:
        pygame.draw.line(screen, BLACK, (cx - 13, cy + 11), (cx + 13, cy - 11), 2)
    else:
        label = {PENCIL: 'PEN', FILL: 'FILL', TEXT: 'TEXT'}[tid]
        s = font_ui.render(label, True, BLACK)
        screen.blit(s, s.get_rect(center=(cx, cy)))

def draw_toolbar():
    pygame.draw.rect(screen, (210, 210, 210), (0, 0, WIDTH, MENU_H))
    pygame.draw.line(screen, (140, 140, 140), (0, MENU_H - 1), (WIDTH, MENU_H - 1), 2)

    for tid, rect in TOOL_RECTS.items():
        bg = (100, 170, 255) if tid == tool else WHITE
        pygame.draw.rect(screen, bg, rect, border_radius=5)
        pygame.draw.rect(screen, (120, 120, 120), rect, 1, border_radius=5)
        _tool_icon(tid, rect.centerx, rect.centery)

    # Brush size buttons 
    for i, (rect, lbl) in enumerate(zip(BRUSH_RECTS, BRUSH_LABELS)):
        bg = (100, 170, 255) if i == brush else WHITE
        pygame.draw.rect(screen, bg, rect, border_radius=5)
        pygame.draw.rect(screen, (120, 120, 120), rect, 1, border_radius=5)
        
        # Draw a preview dot that scales with the brush index
        preview_radius = [3, 6, 12][i] 
        pygame.draw.circle(screen, BLACK, (rect.centerx, rect.centery - 4), preview_radius)
        
        s = font_ui.render(lbl, True, BLACK)
        screen.blit(s, s.get_rect(center=(rect.centerx, rect.bottom - 7)))

    pygame.draw.rect(screen, color, SWATCH_RECT, border_radius=6)
    pygame.draw.rect(screen, (60, 60, 60), SWATCH_RECT, 2, border_radius=6)
    screen.blit(clear_icon, CLEAR_RECT.topleft)

    for rect, c in zip(COLOR_RECTS, PALETTE):
        pygame.draw.rect(screen, c, rect)
        if c == color:
            pygame.draw.rect(screen, WHITE, rect, 3)
        pygame.draw.rect(screen, (80, 80, 80), rect, 1)

def save_canvas():
    ts  = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fn  = f'canvas_{ts}.png'
    sub = canvas.subsurface(pygame.Rect(0, MENU_H, WIDTH, HEIGHT - MENU_H))
    pygame.image.save(sub, fn)

# ─── Application state ────────────────────────────────────────────────────────
tool  = PENCIL
color = BLACK
brush = 1   # 0=S(2px), 1=M(5px), 2=L(10px)

drawing  = False
x1 = y1 = x2 = y2 = 0
prev_pos = None 

text_active = False
text_pos    = (0, 0)
text_buf    = ''

# ─── Main loop ────────────────────────────────────────────────────────────────
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # ── Keyboard Logic ───────────────────────────────────────────────────
        elif event.type == pygame.KEYDOWN:
            if text_active:
                if event.key == pygame.K_RETURN:
                    canvas.blit(font_text.render(text_buf, True, color), text_pos)
                    text_active, text_buf = False, ''
                elif event.key == pygame.K_ESCAPE:
                    text_active, text_buf = False, ''
                elif event.key == pygame.K_BACKSPACE:
                    text_buf = text_buf[:-1]
                elif event.unicode.isprintable():
                    text_buf += event.unicode
            else:
                if event.key == pygame.K_ESCAPE:
                    done = True
                # Direct Selection
                elif event.key == pygame.K_1: brush = 0
                elif event.key == pygame.K_2: brush = 1
                elif event.key == pygame.K_3: brush = 2
                
                # Up/Down Switching
                elif event.key == pygame.K_UP:
                    brush = min(len(BRUSH_SIZES) - 1, brush + 1)
                elif event.key == pygame.K_DOWN:
                    brush = max(0, brush - 1)
                    
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

        # ── Mouse Press ──────────────────────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if text_active:
                if text_buf:
                    canvas.blit(font_text.render(text_buf, True, color), text_pos)
                text_active, text_buf = False, ''

            for tid, rect in TOOL_RECTS.items():
                if rect.collidepoint(pos): tool = tid
            for i, rect in enumerate(BRUSH_RECTS):
                if rect.collidepoint(pos): brush = i
            for i, rect in enumerate(COLOR_RECTS):
                if rect.collidepoint(pos): color = PALETTE[i]
            if CLEAR_RECT.collidepoint(pos):
                canvas.fill(WHITE)

            if pos[1] > MENU_H:
                if tool == TEXT:
                    text_active, text_pos, text_buf = True, pos, ''
                elif tool == FILL:
                    flood_fill(canvas, pos[0], pos[1], color)
                else:
                    drawing = True
                    x1, y1 = pos
                    x2, y2 = pos
                    prev_pos = pos if tool == PENCIL else None

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and tool != PENCIL:
                draw_shape(canvas, tool, color, BRUSH_SIZES[brush], x1, y1, x2, y2)
            drawing = False
            prev_pos = None

        elif event.type == pygame.MOUSEMOTION and drawing:
            pos = event.pos
            if tool == PENCIL and prev_pos:
                pygame.draw.line(canvas, color, prev_pos, pos, BRUSH_SIZES[brush])
                prev_pos = pos
            else:
                x2, y2 = pos

    # ── Render ────────────────────────────────────────────────────────────────
    screen.blit(canvas, (0, 0))
    if drawing and tool != PENCIL:
        draw_shape(screen, tool, color, BRUSH_SIZES[brush], x1, y1, x2, y2)
    if text_active:
        screen.blit(font_text.render(text_buf + '|', True, color), text_pos)

    draw_toolbar()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()