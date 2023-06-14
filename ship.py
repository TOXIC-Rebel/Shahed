import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Ship control class."""

    def __init__(self, ai_game):
        """Initializes the ship and sets its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loads the ship image and obtains the rectangle.
        self.image = pygame.image.load('images/Bandera_small.png')
        self.rect = self.image.get_rect()

        # Each new ship appears at the bottom edge of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Save the floating-point coordinate of the ship's center.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates the position of the ship taking into account the flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Updating the rect attribute based on self.x.
        self.rect.x = self.x


    def blitme(self):
        """Drawing the ship at the current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Placing the ship at the center of the bottom side."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)