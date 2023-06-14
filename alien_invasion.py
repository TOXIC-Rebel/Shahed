import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Class for managing game resources and behavior."""

    def __init__(self):
        """Initializes the game and creates game resources."""
        pygame.init()
        self.settings = Settings()

        # Fullscreen mode.
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Creating a class instance to store game statistics and results panel.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Creating a "Play" button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Starting the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Handles keyboard activity and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Launch a new game with Play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings.
            self.settings.initialize_dynamic_settings()
            # Reset statistic.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Clearing the lists of aliens and projectiles.
            self.aliens.empty()
            self.bullets.empty()

            # Creating a new fleet and placing the ship in the center.
            self._create_fleet()
            self.ship.center_ship()

            # Hides the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creating a new projectile and adding it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updates the positions of projectiles and destroys old projectiles."""
        # Updating the positions of projectiles.
        self.bullets.update()

        # Removing projectiles that have gone off-screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Handling collisions between projectiles and aliens."""
        # Upon detecting a hit, remove the projectile and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroying existing projectiles and creating a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increasing the level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Processing the collision between the ship and an alien."""
        if self.stats.ships_left > 1:
            # Decreasing ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clearing the lists of aliens and projectiles.
            self.aliens.empty()
            self.bullets.empty()

            # Creating a new fleet and placing the ship in the center.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Checks if the aliens have reached the bottom edge of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # The same thing happens as when colliding with the ship.
                self._ship_hit()
                break

    def _update_aliens(self):
        """Updates the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Checking collisions between aliens and the ship.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Checking if aliens have reached the bottom edge of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Creating an invasion fleet."""
        # Creating an alien and calculating the number of aliens in a row.
        # The interval between neighboring aliens is equal to the width of an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        """Determines the number of aliens in a row that fit on the screen."""
        available_spase_x = self.settings.screen_width - (4 * alien_width)
        number_aliens_x = available_spase_x // (2 * alien_width)

        """Determines the number of rows that fit on the screen."""
        ship_height = self.ship.rect.height
        available_spase_y = (self.settings.screen_height -
                             (5 * alien_height) - ship_height)
        number_rows = available_spase_y // (2 * alien_height)

        # Creating the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Creating an alien and placing it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Reacting to the alien reaching the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop fleet by 1 line and changing the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Updates the images on the screen and displays the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Displaying the score information.
        self.sb.show_score()

        # The Play button is displayed when the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Displaying the last rendered screen.
        pygame.display.flip()

if __name__ == '__main__':
    #Creating an instance and starting the game.
    ai = AlienInvasion()
    ai.run_game()




