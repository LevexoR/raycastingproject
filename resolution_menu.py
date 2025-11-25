import pygame
from config import save_config, load_config

class ResolutionMenu:
    def __init__(self, logical_surface, assets, clock, fps, screen_width, screen_height):
        self.logical_surface = logical_surface
        self.assets = assets
        self.clock = clock
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_bg = assets["menu_bg"]

        self.resolutions = [(640, 360), (800, 450), (1280, 720), (1920, 1080)]
        self.selected_index = 0
        self.arrow_timer = 0
        self.config = load_config()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Update config
                        width, height = self.resolutions[self.selected_index]
                        self.config["screen_width"] = width
                        self.config["screen_height"] = height
                        save_config(self.config)
                        
                        # Update la fenêtre Pygame en direct
                        pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
                        self.screen_width = width
                        self.screen_height = height
                        

                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.resolutions)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.resolutions)
                    elif event.key == pygame.K_ESCAPE:
                        return "back"

            # --- Dessin ---
            self.logical_surface.blit(self.menu_bg, (0, 0))

            title_font = self.assets["font_PressStart2P_16"]
            title = title_font.render("Resolution", False, (255, 255, 255))
            title_rect = title.get_rect(centerx=self.logical_surface.get_width() // 2, top=20)
            self.logical_surface.blit(title, title_rect)

            option_font = self.assets["font_PixelOperatorMonoHB8_8"]
            for i, res in enumerate(self.resolutions):
                color = (255, 0, 0)
                text = f"{res[0]} x {res[1]}"
                surf = option_font.render(text, False, color)
                rect = surf.get_rect(centerx=self.logical_surface.get_width() // 2, top=90 + i * 20)
                self.logical_surface.blit(surf, rect)

                if i == self.selected_index:
                    self.arrow_timer += 1
                    if self.arrow_timer % 60 < 30:
                        arrow = option_font.render("→", False, (255, 255, 255))
                        arrow_rect = arrow.get_rect(right=rect.left - 10, centery=rect.centery)
                        self.logical_surface.blit(arrow, arrow_rect)

            # --- Upscale + affichage ---
            scaled_surface = pygame.transform.scale(self.logical_surface, (self.screen_width, self.screen_height))
            pygame.display.get_surface().blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)