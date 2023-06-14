import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for managing projectiles fired by the ship."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Creating a projectile at position (0,0) and assigning the correct position.
        self.rect = pygame.Rect (0, 0, self.settings.bullet_width,
                                 self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # The position of the projectile is stored in floating-point format.
        self.y = float(self.rect.y)

    def update(self):
        """Moves the projectile upwards on the screen."""
        # Updating the position of the projectile in floating-point format.
        self.y -= self.settings.bullet_speed
        # Updating the position of the rectangle.
        self.rect.y = self.y

    def draw_bullet(self):
        """Displaying the projectile on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)