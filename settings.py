class Settings():
    """Class for storing all game settings."""

    def __init__(self):
        """Initializes the static game settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 0, 60)
        # Ship settings.
        #self.ship_speed = 1.5
        self.ship_limit = 3
        # Projectile parameters.
        #self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (174, 174, 174)
        self.bullet_allowed = 3
        # Alian's settings.
        #self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # Game speed increase rate.
        self.speedup_scale = 1.1
        # Rate of increase in alien cost.
        self.score_scale = 1.5

        # Calling dynamic settings
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Sets up the settings that are modified during gameplay."""
        self.ship_speed = 1.5
        self.bullet_speed = 10.0
        self.alien_speed = 0.7

        # fleet_direction = 1 represents rightward movement; & -1 - leftward.
        self.fleet_direction = 1

        # Score counting
        self.alien_points = 50

    def increase_speed(self):
        """Increases the settings for alien speed and cost."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
