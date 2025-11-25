import pygame
import math
from config import load_config

def key_name_to_pygame(key_name):
    """Convertit un nom de touche ('A', 'SPACE', etc.) en pygame constant."""
    try:
        return getattr(pygame, f"K_{key_name.lower()}")
    except AttributeError:
        print(f"Touche inconnue: {key_name}")
        return None

class Game:
    def __init__(self, logical_surface, assets, clock, fps, screen_width, screen_height):
        self.logical_surface = logical_surface
        self.assets = assets
        self.clock = clock
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height

        # === MAP ===
        self.map = [
            "########",
            "#......#",
            "#..##..#",
            "#......#",
            "########"
        ]
        self.tile_size = 64
        self.map_width = len(self.map[0])
        self.map_height = len(self.map)

        # === JOUEUR ===
        self.player_x = 3 * self.tile_size
        self.player_y = 3 * self.tile_size
        self.player_angle = 0
        self.player_speed = 2.5

        # === KEYBINDINGS ===
        config = load_config()
        keybindings = config.get("keybindings", {
            "move_left": "A",
            "move_right": "D",
            "forward": "W",
            "backward": "S"
        })
        
        self.keys = {action: key_name_to_pygame(key) for action, key in keybindings.items()}

    def run(self):
        running = True
        while running:
            # === ÉVÉNEMENTS ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

            # === INPUT ===
            keys_pressed = pygame.key.get_pressed()

            if self.keys.get("move_left") is not None and keys_pressed[self.keys["move_left"]]:
                self.player_angle -= 0.04
            if self.keys.get("move_right") is not None and keys_pressed[self.keys["move_right"]]:
                self.player_angle += 0.04
            if self.keys.get("move_forward") is not None and keys_pressed[self.keys["move_forward"]]:
                self.player_x += math.cos(self.player_angle) * self.player_speed
                self.player_y += math.sin(self.player_angle) * self.player_speed
            if self.keys.get("move_backwards") is not None and keys_pressed[self.keys["move_backwards"]]:
                self.player_x -= math.cos(self.player_angle) * self.player_speed
                self.player_y -= math.sin(self.player_angle) * self.player_speed

            # === RENDU ===
            self.logical_surface.fill((40, 40, 40))
            self.render_3d_view()
            self.render_minimap()

            # === UPSCALE + AFFICHAGE ===
            scaled_surface = pygame.transform.scale(
                self.logical_surface,
                (self.screen_width, self.screen_height)
            )
            pygame.display.get_surface().blit(scaled_surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(self.fps)

    def render_3d_view(self):
        num_rays = 160  # moitié de la largeur logique
        fov = 60 * (math.pi / 180)
        half_fov = fov / 2
        max_depth = 500
        ray_angle = self.player_angle - half_fov
        delta_angle = fov / num_rays
        screen_width = 320
        screen_height = 180
        slice_width = screen_width / num_rays

        for ray in range(num_rays):
            for depth in range(max_depth):
                target_x = self.player_x + math.cos(ray_angle) * depth
                target_y = self.player_y + math.sin(ray_angle) * depth

                map_x = int(target_x / self.tile_size)
                map_y = int(target_y / self.tile_size)

                if self.map[map_y][map_x] == "#":
                    # Correction du fisheye
                    depth *= math.cos(self.player_angle - ray_angle)
                    wall_height = 12000 / (depth + 0.0001)
                    
                    color = max(0, 255 - depth * 0.3)
                    pygame.draw.rect(
                        self.logical_surface,
                        (color, color, color),
                        (ray * slice_width, screen_height / 2 - wall_height / 2, slice_width + 1, wall_height)
                    )
                    break
            ray_angle += delta_angle

    def render_minimap(self):
        scale = 8
        offset_x = 5
        offset_y = 5

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    offset_x + x * scale,
                    offset_y + y * scale,
                    scale - 1,
                    scale - 1
                )
                color = (100, 100, 100) if cell == "#" else (30, 30, 30)
                pygame.draw.rect(self.logical_surface, color, rect)

        # Position du joueur sur la minimap
        px = offset_x + (self.player_x / self.tile_size) * scale
        py = offset_y + (self.player_y / self.tile_size) * scale
        pygame.draw.circle(self.logical_surface, (255, 255, 0), (int(px), int(py)), 2)

        # Direction du joueur
        line_x = px + math.cos(self.player_angle) * 10
        line_y = py + math.sin(self.player_angle) * 10
        pygame.draw.line(self.logical_surface, (255, 255, 0), (px, py), (line_x, line_y), 1)
