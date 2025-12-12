import pygame
import math
from config import load_config

def key_name_to_pygame(key_name):
    """Convertit un nom de touche du fichier config en touche pygame."""
    try:
        return getattr(pygame, f"K_{key_name.lower()}")
    except AttributeError:
        print(f"Touche inconnue: {key_name}")
        return None

# Table de trigonométrie précalculée (résolution 0.1 degré)
TRIGO_TABLE_SIZE = 3600
TRIGO_SIN = [0] * TRIGO_TABLE_SIZE
TRIGO_COS = [0] * TRIGO_TABLE_SIZE

def build_trigo_table():
    """Construit les tables de sinus et cosinus."""
    for i in range(TRIGO_TABLE_SIZE):
        angle = (i / 10) * (math.pi / 180)
        TRIGO_SIN[i] = math.sin(angle)
        TRIGO_COS[i] = math.cos(angle)

def fast_sin(angle_rad):
    """Retourne sin(angle) via la table."""
    index = int((angle_rad * 180 / math.pi) * 10) % TRIGO_TABLE_SIZE
    return TRIGO_SIN[index]

def fast_cos(angle_rad):
    """Retourne cos(angle) via la table."""
    index = int((angle_rad * 180 / math.pi) * 10) % TRIGO_TABLE_SIZE
    return TRIGO_COS[index]

build_trigo_table()


class Game:
    def __init__(self, logical_surface, assets, clock, fps, screen_width, screen_height):
        self.logical_surface = logical_surface
        self.assets = assets
        self.clock = clock
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Carte du jeu
        self.map = [
            "########",
            "#......#",
            "#..##..#",
            "#......#",
            "########"
        ]
        self.tile_size = 64

        # Position et direction du joueur
        self.player_x = 3 * self.tile_size
        self.player_y = 3 * self.tile_size
        self.player_angle = 0
        self.player_speed = 4

        # Chargement des touches depuis le fichier config
        config = load_config()
        keybindings = config.get("keybindings", {
            "move_left": "A",
            "move_right": "D",
            "forward": "W",
            "backward": "S"
        })
        
        self.keys = {action: key_name_to_pygame(key) for action, key in keybindings.items()}

    def run(self):
        """Boucle principale du jeu."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

            keys_pressed = pygame.key.get_pressed()

            # Gestion des mouvements du joueur
            if self.keys.get("move_left") and keys_pressed[self.keys["move_left"]]:
                self.player_angle -= 0.06
            if self.keys.get("move_right") and keys_pressed[self.keys["move_right"]]:
                self.player_angle += 0.06
            if self.keys.get("move_forward") and keys_pressed[self.keys["move_forward"]]:
                self.player_x += fast_cos(self.player_angle) * self.player_speed
                self.player_y += fast_sin(self.player_angle) * self.player_speed
            if self.keys.get("move_backwards") and keys_pressed[self.keys["move_backwards"]]:
                self.player_x -= fast_cos(self.player_angle) * self.player_speed
                self.player_y -= fast_sin(self.player_angle) * self.player_speed

            # Efface l'écran
            self.logical_surface.fill((40, 40, 40))

            # Rendu de la scène 3D
            self.render_3d_view()

            # Affichage de la minimap
            self.render_minimap()

            # Mise à l'échelle de l'image finale
            scaled = pygame.transform.scale(self.logical_surface, (self.screen_width, self.screen_height))
            pygame.display.get_surface().blit(scaled, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)

    def cast_ray(self, angle):
        """Effectue le raycasting avec DDA et retourne la distance du mur."""
        ray_dir_x = fast_cos(angle)
        ray_dir_y = fast_sin(angle)

        # Position du joueur en cases
        map_x = int(self.player_x / self.tile_size)
        map_y = int(self.player_y / self.tile_size)

        # Distance pour traverser une case en X ou Y
        delta_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else 1e30
        delta_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else 1e30

        # Position exacte dans la case
        px = self.player_x / self.tile_size
        py = self.player_y / self.tile_size

        # Détermination du sens et distance initiale à parcourir
        if ray_dir_x < 0:
            step_x = -1
            side_dist_x = (px - map_x) * delta_x
        else:
            step_x = 1
            side_dist_x = ((map_x + 1) - px) * delta_x

        if ray_dir_y < 0:
            step_y = -1
            side_dist_y = (py - map_y) * delta_y
        else:
            step_y = 1
            side_dist_y = ((map_y + 1) - py) * delta_y

        hit = False
        side = 0

        # Boucle DDA : avance dans la grille jusqu'à rencontrer un mur
        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_y
                map_y += step_y
                side = 1

            if self.map[map_y][map_x] == "#":
                hit = True

        # Distance trouvée dans la grille
        distance = side_dist_x - delta_x if side == 0 else side_dist_y - delta_y

        # Conversion en pixels
        return distance * self.tile_size

    def render_3d_view(self):
        """Dessine la vue 3D à partir du raycasting."""
        num_rays = 160
        fov = 60 * (math.pi / 180)
        half_fov = fov / 2

        ray_angle = self.player_angle - half_fov
        delta_angle = fov / num_rays

        screen_width = 320
        screen_height = 180
        slice_width = screen_width / num_rays

        for ray in range(num_rays):
            distance = self.cast_ray(ray_angle)

            # Correction du fisheye
            distance *= fast_cos(self.player_angle - ray_angle)

            # Calcul de la hauteur du mur
            wall_height = 12000 / (distance + 0.0001)

            # Couleur basée sur la distance
            color = max(0, 255 - distance * 0.3)

            pygame.draw.rect(
                self.logical_surface,
                (color, color, color),
                (ray * slice_width, screen_height/2 - wall_height/2, slice_width+1, wall_height)
            )

            ray_angle += delta_angle

    def render_minimap(self):
        """Affiche la carte en vue du dessus."""
        scale = 8
        offset_x = 5
        offset_y = 5

        # Affichage des cases
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(offset_x + x*scale, offset_y + y*scale, scale-1, scale-1)
                color = (100,100,100) if cell == "#" else (30,30,30)
                pygame.draw.rect(self.logical_surface, color, rect)

        # Position du joueur
        px = offset_x + (self.player_x / self.tile_size) * scale
        py = offset_y + (self.player_y / self.tile_size) * scale
        pygame.draw.circle(self.logical_surface, (255,255,0), (int(px), int(py)), 2)

        # Direction du joueur
        line_x = px + fast_cos(self.player_angle) * 10
        line_y = py + fast_sin(self.player_angle) * 10
        pygame.draw.line(self.logical_surface, (255,255,0), (px, py), (line_x, line_y), 1)