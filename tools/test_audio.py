"""Quick script to verify generated audio files play via pygame.mixer."""
import pygame
import time
import os

SOUND_DIR = os.path.join("..", "assets", "sounds")
STONE_MUSIC_FILE = os.path.join(SOUND_DIR, "stone_age_music.wav")
SPEAR_SFX_FILE = os.path.join(SOUND_DIR, "spear.wav")
HIT_SFX_FILE = os.path.join(SOUND_DIR, "hit.wav")

print("Initializing mixer...")
pygame.mixer.init(frequency=44100)
print("Loading sounds...")
try:
    pygame.mixer.music.load(STONE_MUSIC_FILE)
    print("Loaded music")
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Music load failed:", e)

try:
    spear = pygame.mixer.Sound(SPEAR_SFX_FILE)
    hit = pygame.mixer.Sound(HIT_SFX_FILE)
    print("Playing SFX...")
    spear.play()
    time.sleep(0.15)
    hit.play()
except Exception as e:
    print("SFX load/play failed:", e)

print("Letting music play for 2s...")
time.sleep(2)
print("Stopping music and quitting")
pygame.mixer.music.stop()
pygame.mixer.quit()
