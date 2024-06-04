import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Класс для отображения информации о счете."""

    def __init__(self, settings, display, stats):
        """Инициализация атрибутов для ведения счета."""
        self.display = display
        self.display_rect = display.get_rect()
        self.settings = settings
        self.stats = stats

        # Настройки шрифта для информации о счете.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка начальных изображений счета.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразование счета в изображение."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Отображение счета в верхнем правом углу экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.display_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразование рекорда в изображение."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        # Размещение рекорда в верхнем центре экрана.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.display_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразование уровня в изображение."""
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color, self.settings.bg_color
        )

        # Позиционирование уровня ниже счета.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Отображение оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.display)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Отображение счета на экране."""
        self.display.blit(self.score_image, self.score_rect)
        self.display.blit(self.high_score_image, self.high_score_rect)
        self.display.blit(self.level_image, self.level_rect)
        # Отображение кораблей.
        self.ships.draw(self.display)
