import pygame
from pygame.sprite import Sprite

class Projectile(Sprite):
    """Класс для управления снарядами, выпущенными из корабля."""

    def __init__(self, settings, display, ship):
        """Создание объекта снаряда в текущей позиции корабля."""
        super().__init__()
        self.display = display

        # Создание прямоугольника снаряда в (0, 0), затем установка правильной позиции.
        self.rect = pygame.Rect(0, 0, settings.projectile_width, settings.projectile_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Сохранение вещественного значения позиции снаряда.
        self.y = float(self.rect.y)

        self.color = settings.projectile_color
        self.speed = settings.projectile_speed

    def update(self):
        """Перемещение снаряда вверх по экрану."""
        # Обновление вещественной позиции снаряда.
        self.y -= self.speed
        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_projectile(self):
        """Отрисовка снаряда на экране."""
        pygame.draw.rect(self.display, self.color, self.rect)
