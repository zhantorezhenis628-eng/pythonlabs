import pygame
import sys
import os
from persistence import load_settings, save_settings, load_leaderboard, save_score
from ui import Button, TextInput
from racer import Player, Enemy, Obstacle, PowerUp, Coin, NitroStrip

# --- AUTO-FIX PATHING ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Initialization ---
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3: Racer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# --- Load Settings Early ---
settings = load_settings()

def update_settings_buttons():
    btn_sound.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"

# --- Asset Loading ---
def load_sound(name):
    path = os.path.join('assets', 'sounds', name)
    try:
        return pygame.mixer.Sound(path)
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: Could not load {name}. Error: {e}")
        return None

snd_crash = load_sound('crash.wav')
snd_powerup = load_sound('powerup.wav')
music_loaded = False
try:
    pygame.mixer.music.load(os.path.join('assets', 'sounds', 'bg_music.mp3'))
    music_loaded = True
except:
    print("Warning: bg_music.mp3 not found.")

# --- Global Variables & Groups ---
state = "MENU" # Set to "PLAY" to skip menu for testing
player_name = "Player"
score = 0
distance = 0
coins = 0
repair_txt = 0
FINISH_DISTANCE = 1200  # meters

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
nitro_strips = pygame.sprite.Group()
player = None

# --- Function Definitions (Must be BEFORE they are called) ---
def reset_game():
    global player, score, distance, coins, all_sprites, enemies, obstacles, powerups, coins_group, nitro_strips
    all_sprites.empty()
    enemies.empty()
    obstacles.empty()
    powerups.empty()
    coins_group.empty()
    nitro_strips.empty()
    player = Player(settings["car_color"])
    all_sprites.add(player)
    score = 0
    distance = 0
    coins = 0
    if music_loaded and settings["sound"]:
        pygame.mixer.music.play(-1)

def draw_hud():
    screen.blit(font.render(f"Score: {int(score)}", True, (255,255,255)), (10, 10))
    screen.blit(font.render(f"Dist: {int(distance)}m", True, (255,255,255)), (10, 40))
    screen.blit(font.render(f"Coins: {coins}", True, (255,215,0)), (10, 70))
    remaining = max(0, FINISH_DISTANCE - int(distance))
    if remaining < 100:
        color = (255, 255, 0) if remaining > 50 else (255, 0, 0)  # Yellow then red as approaching finish
        screen.blit(font.render(f"FINISH: {remaining}m", True, color), (10, 100))
    else:
        screen.blit(font.render(f"Goal: {remaining}m", True, (255,255,255)), (10, 100))
    if player and player.nitro_active:
        time_left = (player.powerup_timer - pygame.time.get_ticks()) // 1000
        screen.blit(font.render(f"NITRO: {max(0, time_left)}s", True, (0, 255, 255)), (10, 130))
    if player and player.shield_active:
        screen.blit(font.render("SHIELD ACTIVE", True, (255, 215, 0)), (10, 130))
    def draw_hud():
    # ... (other code) ...
    
    # Show Repairs (crashes_allowed)
        repair_txt= f"REPAIRS: {player.crashes_allowed}"
        repair_color = (0, 255, 0) if player.crashes_allowed > 0 else (255, 0, 0)
        screen.blit(font.render(repair_txt, True, repair_color), (10, 100))

    if player.nitro_active:
        # Blinking Cyan text for "SUPER SPEED"
        if (pygame.time.get_ticks() // 100) % 2 == 0:
            screen.blit(font.render("!!! NITRO BOOST !!!", True, (0, 255, 255)), (200, 500))

# --- UI Setup ---
btn_play = Button(200, 150, 200, 50, "Play")
btn_board = Button(200, 220, 200, 50, "Leaderboard")
btn_settings = Button(200, 290, 200, 50, "Settings")
btn_quit = Button(200, 360, 200, 50, "Quit")
btn_back = Button(200, 500, 200, 50, "Back")
btn_retry = Button(200, 350, 200, 50, "Retry")
btn_menu = Button(200, 420, 200, 50, "Main Menu")
name_input = TextInput(200, 250, 200, 40)

# --- Settings UI ---
btn_sound = Button(200, 150, 200, 50, "Sound: ON")
btn_color_red = Button(150, 220, 100, 40, "Red")
btn_color_blue = Button(260, 220, 100, 40, "Blue")
btn_color_green = Button(370, 220, 100, 40, "Green")
btn_diff_easy = Button(150, 280, 100, 40, "Easy")
btn_diff_normal = Button(260, 280, 100, 40, "Normal")
btn_diff_hard = Button(370, 280, 100, 40, "Hard")

update_settings_buttons()

# --- Spawn Events ---
SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_OBSTACLE = pygame.USEREVENT + 2
SPAWN_POWERUP = pygame.USEREVENT + 3
SPAWN_COIN = pygame.USEREVENT + 4
SPAWN_NITRO_STRIP = pygame.USEREVENT + 5
pygame.time.set_timer(SPAWN_ENEMY, 1500)
pygame.time.set_timer(SPAWN_OBSTACLE, 2500)
pygame.time.set_timer(SPAWN_POWERUP, 6000)
pygame.time.set_timer(SPAWN_COIN, 3000)
pygame.time.set_timer(SPAWN_NITRO_STRIP, 8000)

# Initial call if you want to skip the menu
if state == "PLAY":
    reset_game()

# --- Main Loop ---
running = True
while running:
    screen.fill((50, 150, 50)) 
    pygame.draw.rect(screen, (40, 40, 40), (150, 0, 300, 600)) 
    
    # Scrolling road lines
    for y in range(0, 600, 40):
        pygame.draw.rect(screen, (255, 255, 255), (245, (y + int(distance * 10)) % 600, 10, 20))
        pygame.draw.rect(screen, (255, 255, 255), (345, (y + int(distance * 10)) % 600, 10, 20))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        if state == "MENU":
            if btn_play.is_clicked(event): state = "NAME_INPUT"
            if btn_board.is_clicked(event): state = "LEADERBOARD"
            if btn_settings.is_clicked(event): 
                update_settings_buttons()
                state = "SETTINGS"
            if btn_quit.is_clicked(event): running = False
        
        elif state == "NAME_INPUT":
            name_input.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player_name = name_input.text if name_input.text else "Player"
                reset_game()
                state = "PLAY"

        elif state == "PLAY":
            # Dynamic difficulty scaling based on distance
            difficulty_multiplier = 1.0
            if distance > 300: difficulty_multiplier = 1.2
            if distance > 600: difficulty_multiplier = 1.4
            if distance > 900: difficulty_multiplier = 1.6


            all_sprites.update()
                    
                    # Base speed plus score-based difficulty
            base_move_speed = 0.1 + (score // 500 * 0.02)
                    
                    # NITRO BOOST: If active, world moves 3x faster!
            if player.nitro_active:
                        move_multiplier = 3.0
                        score += 0.5  # More points for going fast
            else:
                        move_multiplier = 1.0

            distance += base_move_speed * move_multiplier
            score += 0.2 + (coins * 0.01)
            
            if event.type == SPAWN_ENEMY:
                e = Enemy(settings["difficulty"])
                e.speed = int(e.speed * difficulty_multiplier)
                if not pygame.sprite.spritecollideany(e, enemies) and not pygame.sprite.spritecollideany(e, obstacles):
                    all_sprites.add(e)
                    enemies.add(e)
            
            if event.type == SPAWN_OBSTACLE:
                o = Obstacle()
                if not pygame.sprite.spritecollideany(o, enemies) and not pygame.sprite.spritecollideany(o, obstacles):
                    all_sprites.add(o)
                    obstacles.add(o)
            
            if event.type == SPAWN_POWERUP:
                p = PowerUp()
                if not pygame.sprite.spritecollideany(p, enemies) and not pygame.sprite.spritecollideany(p, obstacles):
                    all_sprites.add(p)
                    powerups.add(p)
            
            if event.type == SPAWN_COIN:
                c = Coin()
                if not pygame.sprite.spritecollideany(c, enemies) and not pygame.sprite.spritecollideany(c, obstacles) and not pygame.sprite.spritecollideany(c, powerups):
                    all_sprites.add(c)
                    coins_group.add(c)
            
            if event.type == SPAWN_NITRO_STRIP:
                ns = NitroStrip()
                all_sprites.add(ns)
                nitro_strips.add(ns)

        elif state == "LEADERBOARD":
            if btn_back.is_clicked(event): state = "MENU"
        
        elif state == "SETTINGS":
            if btn_back.is_clicked(event): state = "MENU"
            if btn_sound.is_clicked(event):
                settings["sound"] = not settings["sound"]
                btn_sound.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
                save_settings(settings)
                if settings["sound"] and music_loaded:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            if btn_color_red.is_clicked(event):
                settings["car_color"] = "red"
                save_settings(settings)
            if btn_color_blue.is_clicked(event):
                settings["car_color"] = "blue"
                save_settings(settings)
            if btn_color_green.is_clicked(event):
                settings["car_color"] = "green"
                save_settings(settings)
            if btn_diff_easy.is_clicked(event):
                settings["difficulty"] = "easy"
                save_settings(settings)
            if btn_diff_normal.is_clicked(event):
                settings["difficulty"] = "normal"
                save_settings(settings)
            if btn_diff_hard.is_clicked(event):
                settings["difficulty"] = "hard"
                save_settings(settings)

        elif state == "GAMEOVER":
            if btn_retry.is_clicked(event):
                reset_game()
                state = "PLAY"
            if btn_menu.is_clicked(event): state = "MENU"

    # --- Render State ---
    if state == "MENU":
        btn_play.draw(screen)
        btn_board.draw(screen)
        btn_settings.draw(screen)
        btn_quit.draw(screen)
    elif state == "NAME_INPUT":
        screen.blit(font.render("Enter Name & Press Enter:", True, (255,255,255)), (150, 200))
        name_input.draw(screen)
    elif state == "PLAY":
        all_sprites.update()
        speed_boost = score // 500
        distance += (0.1 + (speed_boost * 0.02))
        score += 0.2 + (coins * 0.01)  # Base score + coin bonus
        if player.nitro_active:
            score += 1  # Extra points for nitro
        
        # Check finish line
        if distance >= FINISH_DISTANCE:
            pygame.mixer.music.stop()
            save_score(player_name, int(score), int(distance))
            state = "GAMEOVER"
        
        # Collisions
        if not player.shield_active:
            if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
                if settings["sound"] and snd_crash: snd_crash.play()
                if player.crashes_allowed > 0:
                    player.crashes_allowed -= 1
                    player.shield_active = True
                    player.powerup_timer = pygame.time.get_ticks() + 2000
                else:
                    pygame.mixer.music.stop()
                    save_score(player_name, int(score), int(distance))
                    state = "GAMEOVER"
        
        # Powerups
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if settings["sound"] and snd_powerup: snd_powerup.play()
            if hit.type == "Nitro":
                player.nitro_active, player.shield_active = True, False
                player.powerup_timer = pygame.time.get_ticks() + 4000
            elif hit.type == "Shield":
                player.shield_active, player.nitro_active = True, False
                player.powerup_timer = pygame.time.get_ticks() + 4000
            elif hit.type == "Repair": player.crashes_allowed = 1
        
        # Coin collection
        coin_hits = pygame.sprite.spritecollide(player, coins_group, True)
        for coin in coin_hits:
            coins += 1
            score += coin.value
            if settings["sound"]:
                try:
                    coin_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'GetCoin.mp3'))
                    coin_sound.play()
                except:
                    pass  # Sound not critical
        
        # Nitro strip collision
        if pygame.sprite.spritecollideany(player, nitro_strips):
            if not player.nitro_active:
                player.nitro_active = True
                player.shield_active = False
                player.powerup_timer = pygame.time.get_ticks() + 2000  # Shorter nitro from strips
        
        all_sprites.draw(screen)
        draw_hud()
    elif state == "LEADERBOARD":
        screen.fill((30, 30, 30))
        board = load_leaderboard()
        screen.blit(font.render("Top 10 Scores", True, (255,255,255)), (200, 20))
        for i, entry in enumerate(board):
            txt = f"{i+1}. {entry['name']} - {entry['score']} pts, {entry['distance']}m"
            screen.blit(font.render(txt, True, (255,255,255)), (50, 60 + i*30))
        btn_back.draw(screen)
    elif state == "SETTINGS":
        screen.fill((30, 30, 30))
        screen.blit(font.render("Settings", True, (255,255,255)), (250, 50))
        screen.blit(font.render("Sound:", True, (255,255,255)), (50, 160))
        screen.blit(font.render("Car Color:", True, (255,255,255)), (50, 230))
        screen.blit(font.render("Difficulty:", True, (255,255,255)), (50, 290))
        btn_sound.draw(screen)
        btn_color_red.draw(screen)
        btn_color_blue.draw(screen)
        btn_color_green.draw(screen)
        btn_diff_easy.draw(screen)
        btn_diff_normal.draw(screen)
        btn_diff_hard.draw(screen)
        btn_back.draw(screen)
    elif state == "GAMEOVER":
        screen.fill((0, 0, 0))
        screen.blit(font.render("GAME OVER!", True, (255, 0, 0)), (220, 150))
        screen.blit(font.render(f"Score: {int(score)} points", True, (255,255,255)), (180, 200))
        screen.blit(font.render(f"Distance: {int(distance)} meters", True, (255,255,255)), (180, 230))
        screen.blit(font.render(f"Coins Collected: {coins}", True, (255,215,0)), (180, 260))
        if distance >= FINISH_DISTANCE:
            screen.blit(font.render("🏁 FINISH LINE REACHED! 🏁", True, (0, 255, 0)), (150, 290))
        btn_retry.draw(screen)
        btn_menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()