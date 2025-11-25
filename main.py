import pygame
from assets import load_assets
from config import load_config
from settings import LOGICAL_WIDTH, LOGICAL_HEIGHT, FPS
from menu import Menu
from game import Game
from settings_menu import *
from resolution_menu import *
from keybindings_menu import *
from volume_menu import *
from language_menu import *

# --- Load config ---
config = load_config()
SCREEN_WIDTH = config.get("screen_width", 1280)
SCREEN_HEIGHT = config.get("screen_height", 720)
VOLUME = config.get("music_volume", 0.1)

# --- pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# --- Load assets ---
assets = load_assets()

# --- Lancer la musique en background ---
pygame.mixer.init()
pygame.mixer.music.load(assets["music_bg"])
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)  # boucle infinie

# --- Logical surface for pixel art ---
logical_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

# --- Main loop ---
running = True
while running:
    # Charge le menu principal dès le lancement du jeu
    menu = Menu(
        logical_surface,
        assets,
        clock,
        FPS,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )
    action = menu.run()

    # Si l'action pressée est settings, lancer le menu settings
    if action == "settings":
        settings_menu = SettingsMenu(
            logical_surface,
            assets,
            clock,
            FPS,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )

        settings_menu_action = settings_menu.run()
        if settings_menu_action == "quit":
            running = False
        if settings_menu_action == "resolution":
            resolution_menu = ResolutionMenu(
                logical_surface,
                assets,
                clock,
                FPS,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
            resolution_menu_action = resolution_menu.run()

            # Recharger la config après changement de paramètres
            config = load_config()
            SCREEN_WIDTH = config.get("screen_width", SCREEN_WIDTH)
            SCREEN_HEIGHT = config.get("screen_height", SCREEN_HEIGHT)

            # Re-créer la fenêtre Pygame avec la nouvelle taille
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
        
        if settings_menu_action == "keybindings":
            keybindings_menu = KeybindingsMenu(
                logical_surface,
                assets,
                clock,
                FPS,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
            keybindings_menu_action = keybindings_menu.run()
        if settings_menu_action == "volume":
            volume_menu = VolumeMenu(
                logical_surface,
                assets,
                clock,
                FPS,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
            volume_menu_action = volume_menu.run()

        if settings_menu_action == "language":
            language_menu = LanguageMenu(
                logical_surface,
                assets,
                clock,
                FPS,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
            language_menu_action = language_menu.run()

    if action == "start_game":
        game = Game(
            logical_surface,
            assets,
            clock,
            FPS,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )

        game_action = game.run()
        if game_action == "quit":
            running = False

    elif action == "quit":
        running = False
        
pygame.quit()