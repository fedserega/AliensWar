class GameStats:
    """Отслеживание статистики для игры."""

    def __init__(self, settings):
        """Инициализация статистики."""
        self.settings = settings
        self.reset_stats()

        # Начало игры в неактивном состоянии.
        self.game_active = False

        # Рекорд не должен сбрасываться.
        self.high_score = 0

    def reset_stats(self):
        """Инициализация изменяющейся статистики в течение игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
