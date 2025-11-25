import pygame
from config import save_config, load_config

class KeybindingsMenu:
    def __init__(self, logical_surface, assets, clock, fps, screen_width, screen_height):
        self.logical_surface = logical_surface
        self.assets = assets
        self.clock = clock
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_bg = assets["menu_bg"]

        self.config = load_config()
        self.keybindings = self.config.get("keybindings", {
            "move_left": "A",
            "move_right": "D",
            "move_forward": "W",
            "move_backwards": "S"
        })
        self.actions = list(self.keybindings.keys())
        self.selected_index = 0
        self.arrow_timer = 0
        self.waiting_input = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if self.waiting_input:
                        new_key = pygame.key.name(event.key).upper()
                        self.keybindings[self.actions[self.selected_index]] = new_key
                        self.config["keybindings"] = self.keybindings
                        save_config(self.config)
                        self.waiting_input = False
                    else:
                        if event.key == pygame.K_RETURN:
                            self.waiting_input = True
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.actions)
                        elif event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.actions)
                        elif event.key == pygame.K_ESCAPE:
                            return "back"

            self.logical_surface.blit(self.menu_bg, (0, 0))


            title_font = self.assets["font_PressStart2P_16"]
            title = title_font.render("Keybindings", False, (255, 255, 255))
            title_rect = title.get_rect(centerx=self.logical_surface.get_width() // 2, top=20)
            self.logical_surface.blit(title, title_rect)

            option_font = self.assets["font_PixelOperatorMonoHB8_8"]
            for i, action in enumerate(self.actions):
                key = self.keybindings[action]
                text = f"{action.upper()} : {key}"
                color = (255, 0, 0)
                surf = option_font.render(text, False, color)
                rect = surf.get_rect(centerx=self.logical_surface.get_width() // 2, top=90 + i * 20)
                self.logical_surface.blit(surf, rect)

                if i == self.selected_index:
                    self.arrow_timer += 1
                    if self.arrow_timer % 60 < 30:
                        arrow = option_font.render("→", False, (255, 255, 255))
                        arrow_rect = arrow.get_rect(right=rect.left - 10, centery=rect.centery)
                        self.logical_surface.blit(arrow, arrow_rect)

            if self.waiting_input:
                waiting = option_font.render("Press a key...", False, (255, 255, 0))
                rect = waiting.get_rect(centerx=self.logical_surface.get_width() // 2, top=200)
                self.logical_surface.blit(waiting, rect)

            scaled_surface = pygame.transform.scale(self.logical_surface, (self.screen_width, self.screen_height))
            pygame.display.get_surface().blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)