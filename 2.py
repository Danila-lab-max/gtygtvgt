import time
import pygame
import random
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def draw(screen, score, speed):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 30)
    text = font.render("Score:" + score, True, (100, 255, 100))
    screen.blit(text, (0, 0))
    text1 = font.render("Speed:" + speed, True, (100, 255, 100))
    screen.blit(text1, (0, 60))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не загрузилось:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50

clock = pygame.time.Clock()


def start_screen():
    intro_text = ["Правила:",
                  "Нужно",
                  "передвигать машину",
                  "клавишами,",
                  "не врезаясь в другие машины.",
                  "W - увелечение скорости, S - уменьшение."]

    fon = pygame.transform.scale(load_image('p.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 40
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    pygame.init()
    pygame.display.set_caption('Шарики')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    running = True
    screen2 = pygame.Surface(screen.get_size())
    x1, y1 = 0, 0
    drawing = False  # режим рисования выключен
    v = 100
    v_show = 60
    list = []
    list1 = []
    y_go = -1
    x_go = -1
    cor_x = 250
    cor_y = 400
    point = 0
    point1 = 0
    clock = pygame.time.Clock()
    while running:
        ver = random.choice([1] + [0] * 100)
        if point // 100 != point1 // 100:
            print(point // 100)
        point1 = point
        point += 5
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if cor_x <= 390:
                        cor_x += 10
                if event.key == pygame.K_LEFT:
                    if cor_x >= 190:
                        cor_x -= 10
                if event.key == pygame.K_w:
                    v += 10
                    v_show += 1
                if event.key == pygame.K_s:
                    v -= 10
                    v_show -= 1
                else:
                    break
        if ver == 1:
            tim = 0
            drawing = True
            x1, y1 = random.randint(190, 390), 0
            list1.append([-1, -1])
            list.append([x1, y1])
        draw(screen, str(point // 100), str(v_show))
        surf1 = pygame.image.load('road.jpg')
        surf = pygame.transform.scale(surf1, (300, 501))
        rect = surf.get_rect(
            bottomright=(400, 501))
        screen.blit(surf, rect)
        surf1 = pygame.image.load('car_pygame.png')
        surf = pygame.transform.scale(surf1, (80, 100))
        rect = surf.get_rect(
            bottomright=(cor_x, cor_y))
        screen.blit(surf, rect)
        screen2.blit(screen, (0, 0))
        # рисуем на экране сохранённое на втором холсте
        screen.blit(screen2, (0, 0))
        s = v * clock.tick() / 1000  # и, если надо, текущий прямоугольник
        for i in range(len(list)):
            if point // 100 != point1 // 100:
                print(point // 100)
            point1 = point
            point += 1
            surf1 = pygame.image.load('3 (2).png')
            surf = pygame.transform.scale(surf1, (80, 100))
            rect = surf.get_rect(
                bottomright=(list[i][0], list[i][1]))
            screen.blit(surf, rect)
            # list[i][0] += s / list1[i][0]
            list[i][1] -= s / list1[i][1]
            if list[i][0] == cor_x or list[i][1] == cor_y:
                point = 0
        l = list.copy()
        list = []
        for i in l:
            if i[1] >= 501:
                continue
            else:
                list.append(i)
            if -30 <= i[0] - cor_x <= 30 and -30 <= i[1] - cor_y <= 30:
                point = 0
        screen2.blit(screen, (0, 0))
        pygame.display.flip()

