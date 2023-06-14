class GameStats():
    """Tracking statistics for the game."""

    def __init__(self, ai_game):
        """Initializing the statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Game starts in an inactive state.
        self.game_active = False
        # The high score should not be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initializes the game statistics that change during gameplay."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1