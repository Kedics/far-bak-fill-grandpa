import pygame
import random
import sys

pygame.init()

# Определение параметров экрана и цветов
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grandpa's Adventure")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Загрузка фонового изображения
background_image = pygame.image.load("fon.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка изображения дедушки
grandpa_image = pygame.image.load("grandpa.png")
scaled_width = 50
scaled_height = 50
grandpa_image = pygame.transform.scale(grandpa_image, (scaled_width, scaled_height))
grandpa_rect = grandpa_image.get_rect()
grandpa_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

# Создание изображения огня
fire_image = pygame.Surface((20, 20))
fire_image.fill(RED)
fires = []

# Скорость огня
fire_speed = 3

# Параметры прыжка
jumping = False
jump_count = 5
jump_vel = 1.5

# Флаги состояния игры
game_over = False
show_start_screen = True

# Шрифт и тексты для начального экрана и экрана смерти
font = pygame.font.SysFont(None, 36)
start_text = "Привет! Меня зовут Дедушка. Помогите мне избежать огня!"
death_text = "Вы проиграли! Нажмите R для перезапуска или Q для выхода."

# Прямоугольники кнопок
start_button_rect = pygame.Rect(300, 400, 200, 50)
quit_button_rect = pygame.Rect(300, 470, 200, 50)

# Уровень земли
GROUND_LEVEL = SCREEN_HEIGHT - scaled_height

# Загрузка аудиофайлов
pygame.mixer.music.load('main_menu_music.mp3')
game_music = pygame.mixer.Sound('game_music.wav')
death_sound = pygame.mixer.Sound('death_sound.wav')

# Функция для воспроизведения музыки главного меню
def play_main_menu_music():
    pygame.mixer.music.play(-1)  # -1 означает зацикленное воспроизведение

# Функция для воспроизведения музыки в игре
def play_game_music():
    pygame.mixer.music.stop()  # Остановим музыку главного меню, если она играет
    game_music.play(-1)

# Функция для воспроизведения звука смерти
def play_death_sound():
    pygame.mixer.music.stop()  # Остановим музыку, если она играет
    death_sound.play()

# Функция для остановки воспроизведения всех звуков
def stop_all_sounds():
    pygame.mixer.music.stop()
    game_music.stop()
    death_sound.stop()

# Функция сброса игры
def reset_game():
    global grandpa_rect, fires, game_over, jumping, jump_count
    grandpa_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    fires.clear()
    game_over = False
    jumping = False
    jump_count = 10  # Сброс счетчика прыжка

# Функция главного меню
def start_screen():
    global show_start_screen
    play_main_menu_music()  # Воспроизводим музыку главного меню
    while show_start_screen:
        SCREEN.fill(BLACK)
        text_surface = font.render(start_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text_surface, text_rect)

        # Рисуем кнопки
        pygame.draw.rect(SCREEN, WHITE, start_button_rect, 2)
        pygame.draw.rect(SCREEN, WHITE, quit_button_rect, 2)

        start_button_text = font.render("Начать игру", True, WHITE)
        start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_button_text, start_button_text_rect)

        quit_button_text = font.render("Выйти", True, WHITE)
        quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
        SCREEN.blit(quit_button_text, quit_button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_start_screen = False
                    play_game_music()  # Начинаем воспроизводить музыку игры
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    show_start_screen = False
                    play_game_music()  # Начинаем воспроизводить музыку игры
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

# Функция экрана смерти
def death_screen():
    global game_over
    play_death_sound()  # Воспроизводим звук смерти
    while game_over:
        SCREEN.fill(BLACK)
        text_surface = font.render(death_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text_surface, text_rect)

        # Рисуем кнопки
        pygame.draw.rect(SCREEN, WHITE, start_button_rect, 2)
        pygame.draw.rect(SCREEN, WHITE, quit_button_rect, 2)

        start_button_text = font.render("Перезапустить", True, WHITE)
        start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
        SCREEN.blit(start_button_text, start_button_text_rect)

        quit_button_text = font.render("Выйти", True, WHITE)
        quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
        SCREEN.blit(quit_button_text, quit_button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    reset_game()
                    play_game_music()  # Воспроизводим музыку игры после перезапуска
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    game_over = False
                    reset_game()
                    play_game_music()  # Воспроизводим музыку игры после перезапуска
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

# Основной игровой цикл
def game_loop():
    global jumping, jump_count, game_over

    clock = pygame.time.Clock()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            grandpa_rect.x -= 1
        if keys[pygame.K_d]:
            grandpa_rect.x += 1

        if keys[pygame.K_w] and not jumping:
            jumping = True

        if jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                grandpa_rect.y -= (jump_count ** 2) * 0.3 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = 10  # Сброс счетчика прыжка

        # Добавляем "невидимый пол", чтобы герой не проваливался ниже уровня земли
        if grandpa_rect.y > GROUND_LEVEL:
            grandpa_rect.y = GROUND_LEVEL

        if random.randint(0, 100) < 5:
            fire_rect = fire_image.get_rect(x=random.randint(0, SCREEN_WIDTH - 20), y=0)
            fires.append(fire_rect)

        for fire_rect in fires:
            fire_rect.y += fire_speed
            if fire_rect.colliderect(grandpa_rect):
                game_over = True
                death_screen()

        for fire_rect in fires[:]:
            if fire_rect.y > SCREEN_HEIGHT:
                fires.remove(fire_rect)

        SCREEN.blit(background_image, (0, 0))  # Отображаем фон только один раз перед отрисовкой объектов
        SCREEN.blit(grandpa_image, grandpa_rect)
        for fire_rect in fires:
            SCREEN.blit(fire_image, fire_rect)

        pygame.display.flip()
        clock.tick(60)

# Запуск главного меню и основного игрового цикла
start_screen()
game_loop()

pygame.quit()
