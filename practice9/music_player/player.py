import pygame
import os

# Initialize the mixer so we can play audio
pygame.mixer.init()

# Scan the current folder for audio files and store their names in a list
tracks = []
for filename in os.listdir("."):
    if filename.endswith((".mp3", ".wav", ".ogg")):
        tracks.append(filename)
tracks.sort()  # alphabetical order

# Keep track of which song is currently selected
current_index = 0


def play():
    """Load and play the current track."""
    if not tracks:
        return
    pygame.mixer.music.load(tracks[current_index])
    pygame.mixer.music.play()


def stop():
    """Stop playback."""
    pygame.mixer.music.stop()


def next_track():
    """Move to the next track and play it."""
    global current_index
    stop()
    current_index = (current_index + 1) % len(tracks)  # wrap around to 0 at the end
    play()


def prev_track():
    """Move to the previous track and play it."""
    global current_index
    stop()
    current_index = (current_index - 1) % len(tracks)  # wrap around to last at the start
    play()


def current_name():
    """Return the name of the current track, or a message if none found."""
    if not tracks:
        return "No tracks found"
    return tracks[current_index]


def status():
    """Return whether music is currently playing or stopped."""
    if pygame.mixer.music.get_busy():
        return "Playing"
    return "Stopped"
