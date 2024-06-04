import pygame.font

class Button:
    def __init__(self, settings, display, text):
        """Инициализация атрибутов кнопки."""
        self.display = display
        self.display_rect = display.get_rect()

        # Установка размеров и свойств кнопки.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Создание объекта rect кнопки и выравнивание его по центру.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.display_rect.center

        # Сообщение кнопки нужно подготовить только один раз.
        self.prep_msg(text)

    def prep_msg(self, text):
        """Преобразование текста в изображение и выравнивание текста по центру кнопки."""
        self.msg_image = self.font.render(text, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Отрисовка кнопки с текстом."""
        self.display.fill(self.button_color, self.rect)
        self.display.blit(self.msg_image, self.msg_image_rect)
