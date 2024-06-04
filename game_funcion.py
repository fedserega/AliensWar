import sys
from time import sleep

import pygame

from projectile import Projectile
from enemy import Enemy

def handle_keydown(event, settings, display, ship, projectiles):
    """Обработка нажатий клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        shoot_projectile(settings, display, ship, projectiles)
    elif event.key == pygame.K_q:
        sys.exit()

def handle_keyup(event, ship):
    """Обработка отпускания клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def handle_events(settings, display, stats, scoreboard, play_button, ship, enemies, projectiles):
    """Обработка событий клавиатуры и мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event, settings, display, ship, projectiles)
        elif event.type == pygame.KEYUP:
            handle_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, display, stats, scoreboard, play_button, ship, enemies, projectiles, mouse_x, mouse_y)

def check_play_button(settings, display, stats, scoreboard, play_button, ship, enemies, projectiles, mouse_x, mouse_y):
    """Запуск новой игры при нажатии кнопки 'Играть'."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс настроек игры.
        settings.initialize_dynamic_settings()

        # Скрыть курсор мыши.
        pygame.mouse.set_visible(False)

        # Сброс статистики игры.
        stats.reset_stats()
        stats.game_active = True

        # Сброс изображений табло.
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # Очистить списки врагов и снарядов.
        enemies.empty()
        projectiles.empty()

        # Создать новый флот и центрировать корабль.
        create_fleet(settings, display, ship, enemies)
        ship.center_ship()

def shoot_projectile(settings, display, ship, projectiles):
    """Выпуск снаряда, если лимит не достигнут."""
    if len(projectiles) < settings.projectiles_allowed:
        new_projectile = Projectile(settings, display, ship)
        projectiles.add(new_projectile)

def refresh_screen(settings, display, stats, scoreboard, ship, enemies, projectiles, play_button):
    """Обновить изображения на экране и переключиться на новый экран."""
    display.fill(settings.bg_color)

    # Перерисовать все снаряды.
    for projectile in projectiles.sprites():
        projectile.draw_projectile()
    ship.draw()
    enemies.draw(display)

    # Отобразить информацию о счете.
    scoreboard.show_score()

    # Отобразить кнопку 'Играть', если игра не активна.
    if not stats.game_active:
        play_button.draw_button()

    # Сделать последний нарисованный экран видимым.
    pygame.display.flip()

def update_projectiles(settings, display, stats, scoreboard, ship, enemies, projectiles):
    """Обновить позиции снарядов и удалить старые снаряды."""
    projectiles.update()

    # Удалить снаряды, которые вышли за пределы экрана.
    for projectile in projectiles.copy():
        if projectile.rect.bottom <= 0:
            projectiles.remove(projectile)

    check_projectile_enemy_collisions(settings, display, stats, scoreboard, ship, enemies, projectiles)

def check_high_score(stats, scoreboard):
    """Проверить, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()

def check_projectile_enemy_collisions(settings, display, stats, scoreboard, ship, enemies, projectiles):
    """Обработка столкновений снарядов с врагами."""
    collisions = pygame.sprite.groupcollide(projectiles, enemies, True, True)

    if collisions:
        for enemies in collisions.values():
            stats.score += settings.enemy_points * len(enemies)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(enemies) == 0:
        # Если весь флот уничтожен, начать новый уровень.
        projectiles.empty()
        settings.increase_speed()

        # Увеличить уровень.
        stats.level += 1
        scoreboard.prep_level()

        create_fleet(settings, display, ship, enemies)

def check_fleet_edges(settings, enemies):
    """Реагировать на достижение флотом края экрана."""
    for enemy in enemies.sprites():
        if enemy.is_at_edge():
            change_fleet_direction(settings, enemies)
            break

def change_fleet_direction(settings, enemies):
    """Опустить весь флот и изменить направление движения."""
    for enemy in enemies.sprites():
        enemy.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def ship_hit(settings, display, stats, scoreboard, ship, enemies, projectiles):
    """Обработка столкновения корабля с врагом."""
    if stats.ships_left > 0:
        # Уменьшить ships_left.
        stats.ships_left -= 1

        # Обновить табло.
        scoreboard.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Очистить списки врагов и снарядов.
    enemies.empty()
    projectiles.empty()

    # Создать новый флот и центрировать корабль.
    create_fleet(settings, display, ship, enemies)
    ship.center_ship()

    # Пауза.
    sleep(0.5)

def check_enemies_bottom(settings, display, stats, scoreboard, ship, enemies, projectiles):
    """Проверить, достигли ли враги нижней части экрана."""
    display_rect = display.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= display_rect.bottom:
            # Обработать это как столкновение корабля с врагом.
            ship_hit(settings, display, stats, scoreboard, ship, enemies, projectiles)
            break

def update_enemies(settings, display, stats, scoreboard, ship, enemies, projectiles):
    """
    Проверить, достиг ли флот края экрана,
    затем обновить позиции всех врагов во флоте.
    """
    check_fleet_edges(settings, enemies)
    enemies.update()

    # Проверить столкновения врагов с кораблем.
    if pygame.sprite.spritecollideany(ship, enemies):
        ship_hit(settings, display, stats, scoreboard, ship, enemies, projectiles)

    # Проверить, достигли ли враги нижней части экрана.
    check_enemies_bottom(settings, display, stats, scoreboard, ship, enemies, projectiles)

def get_number_enemies_x(settings, enemy_width):
    """Определить количество врагов в ряду."""
    available_space_x = settings.screen_width - 2 * enemy_width
    number_enemies_x = int(available_space_x / (2 * enemy_width))
    return number_enemies_x

def get_number_rows(settings, ship_height, enemy_height):
    """Определить количество рядов врагов, помещающихся на экране."""
    available_space_y = settings.screen_height - (3 * enemy_height) - ship_height
    number_rows = int(available_space_y / (2 * enemy_height))
    return number_rows

def create_enemy(settings, display, enemies, enemy_number, row_number):
    """Создать врага и разместить его в ряду."""
    enemy = Enemy(settings, display)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)

def create_fleet(settings, display, ship, enemies):
    """Создать полный флот врагов."""
    # Создать врага и найти количество врагов в ряду.
    enemy = Enemy(settings, display)
    number_enemies_x = get_number_enemies_x(settings, enemy.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, enemy.rect.height)

    # Создать флот врагов.
    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(settings, display, enemies, enemy_number, row_number)
