import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """Класс, представляющий одного врага в группе."""

    def __init__(self, settings, display):
        """Инициализация врага и установка его начальной позиции."""
        super().__init__()
        self.display = display
        self.settings = settings

        # Загрузка изображения врага и назначение атрибута rect.
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()

        # Начало каждого нового врага вблизи верхнего левого угла экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции врага.
        self.x = float(self.rect.x)

    def is_at_edge(self):
        """Возвращает True, если враг на краю экрана."""
        screen_rect = self.display.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def move(self):
        """Перемещение врага вправо или влево."""
        self.x += self.settings.enemy_speed * self.settings.group_direction
        self.rect.x = self.x

    def draw(self):
        """Отображение врага в текущей позиции."""
        self.display.blit(self.image, self.rect)
