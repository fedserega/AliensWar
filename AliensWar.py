import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def start_game():
    """Инициализация игры, настроек и экрана."""
    pygame.init()
    settings = Settings()
    display = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Space Defense")

    # Создание кнопки "Играть".
    play_button = Button(settings, display, "Играть")

    # Создание экземпляра для хранения статистики игры и табло.
    stats = GameStats(settings)
    scoreboard = Scoreboard(settings, display, stats)

    # Установка фонового цвета.
    bg_color = (230, 230, 230)

    # Создание корабля, группы пуль и группы врагов.
    ship = Ship(settings, display)
    bullets = Group()
    enemies = Group()

    # Создание группы врагов.
    gf.create_fleet(settings, display, ship, enemies)

    # Запуск основного цикла игры.
    while True:
        gf.check_events(settings, display, stats, scoreboard, play_button, ship, enemies, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, display, stats, scoreboard, ship, enemies, bullets)
            gf.update_enemies(settings, display, stats, scoreboard, ship, enemies, bullets)

        gf.update_screen(settings, display, stats, scoreboard, ship, enemies, bullets, play_button)

start_game()
