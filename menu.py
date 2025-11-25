import pygame

class Menu:
    def __init__(self, logical_surface, assets, clock, fps, screen_width, screen_height):
        self.logical_surface = logical_surface
        self.assets = assets
        self.clock = clock
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_bg = assets["menu_bg"]

        # Options du menu
        self.options = ["Start Game", "Settings", "Quit"]
        self.selected_index = 0
        self.arrow_timer = 0

    def run(self):
        running = True
        while running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.options[self.selected_index].lower().replace(" ", "_")
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)

            # Dessin du fond
            self.logical_surface.blit(self.menu_bg, (0, 0))

            # Titre
            title_font = self.assets["font_PressStart2P_16"]
            title = title_font.render("Pseudo3DTest", False, (255, 255, 255))
            text_rect_title = title.get_rect(centerx=self.logical_surface.get_width() // 2, top=20)
            self.logical_surface.blit(title, text_rect_title)

            # Options
            option_font = self.assets["font_PixelOperatorMonoHB8_8"]
            for i, option_text in enumerate(self.options):
                color = (255, 0, 0)
                option_surface = option_font.render(option_text, False, color)
                text_rect = option_surface.get_rect()
                text_rect.centerx = self.logical_surface.get_width() // 2
                text_rect.top = 90 + i * 20
                self.logical_surface.blit(option_surface, text_rect)

                # Flèche clignotante
                if i == self.selected_index:
                    self.arrow_timer += 1
                    if self.arrow_timer % 60 < 30:  # Clignote toutes les 30 frames
                        arrow_surface = option_font.render("→", False, (255, 255, 255))
                        arrow_rect = arrow_surface.get_rect()
                        arrow_rect.right = text_rect.left - 10
                        arrow_rect.centery = text_rect.centery
                        self.logical_surface.blit(arrow_surface, arrow_rect)

            # Upscale et affichage
            scaled_surface = pygame.transform.scale(self.logical_surface, (self.screen_width, self.screen_height))
            pygame.display.get_surface().blit(scaled_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(self.fps)