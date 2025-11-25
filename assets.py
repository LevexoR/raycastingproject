import os
import pygame

BASE_DIR = os.path.dirname(__file__)
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
MUSIC_DIR = os.path.join(BASE_DIR, "assets", "music")

def load_assets():
    assets = {}

    # --- Fonts ---
    sizes = [8, 16]
    font_files = [f for f in os.listdir(FONTS_DIR) if f.lower().endswith(".ttf")]
    for font_file in font_files:
        font_name = os.path.splitext(font_file)[0]
        font_path = os.path.join(FONTS_DIR, font_file)
        for size in sizes:
            key = f"font_{font_name}_{size}"
            assets[key] = pygame.font.Font(font_path, size)

    # --- Images ---
    menu_bg_path = os.path.join(IMAGES_DIR, "menu_bg.png")
    assets["menu_bg"] = pygame.image.load(menu_bg_path).convert()

    # --- Musique ---
    music_path = os.path.join(MUSIC_DIR, "background.mp3")
    assets["music_bg"] = music_path

    return assets