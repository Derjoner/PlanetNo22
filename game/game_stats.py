class GameStats:
    """Класс статистики"""

    def __init__(self, ai_game):
        """Инициализация статистики"""

        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        with open("game/highscore.txt", "r") as f:
            self.high_score = int(f.readline())

    def reset_stats(self):
        """Инициализация динамической статистики"""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1