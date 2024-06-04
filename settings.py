class Settings:
    """Класс для хранения всех настроек игры."""

    def __init__(self):
        """Инициализация статических настроек игры."""
        # Настройки экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки корабля.
        self.ship_limit = 3

        # Настройки пули.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройки пришельцев.
        self.fleet_drop_speed = 10

        # Скорость увеличения сложности игры.
        self.speedup_scale = 1.1
        # Увеличение очков за пришельца.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализация настроек, изменяющихся в течение игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.3

        # Очки за пришельца.
        self.alien_points = 50

        # Направление движения флота. 1 - вправо, -1 - влево.
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличение скорости и очков за пришельцев."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
