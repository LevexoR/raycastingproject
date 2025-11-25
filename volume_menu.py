import pygame

from config import save_config, load_config

class VolumeMenu:
    def __init__(self, logical_surface, assets, clock, fps, screen_width, screen_height):
        self.logical_surface = logical_surface
        self.assets = assets
        self.clock = clock
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_bg = assets["menu_bg"]

        self.config = load_config()
        self.volume = self.config.get("music_volume", 0.5)
        self.arrow_timer = 0


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.volume = min(1.0, self.volume + 0.1)
                    elif event.key == pygame.K_LEFT:
                        self.volume = max(0.0, self.volume - 0.1)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.config["music_volume"] = self.volume
                        save_config(self.config)
                        pygame.mixer.music.set_volume(self.volume)
                        return "back"


            self.logical_surface.blit(self.menu_bg, (0, 0))


            title_font = self.assets["font_PressStart2P_16"]
            title = title_font.render("Volume", False, (255, 255, 255))
            rect_title = title.get_rect(centerx=self.logical_surface.get_width() // 2, top=20)
            self.logical_surface.blit(title, rect_title)


            option_font = self.assets["font_PixelOperatorMonoHB8_8"]
            vol_text = f"{int(self.volume * 100)}%"
            surf = option_font.render(vol_text, False, (255, 0, 0))
            rect = surf.get_rect(centerx=self.logical_surface.get_width() // 2, centery=self.logical_surface.get_height() // 2)
            self.logical_surface.blit(surf, rect)


            hint = option_font.render("← → Adjust | Enter to save", False, (200, 200, 200))
            hint_rect = hint.get_rect(centerx=self.logical_surface.get_width() // 2, top=rect.bottom + 20)
            self.logical_surface.blit(hint, hint_rect)


            scaled_surface = pygame.transform.scale(self.logical_surface, (self.screen_width, self.screen_height))
            pygame.display.get_surface().blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)