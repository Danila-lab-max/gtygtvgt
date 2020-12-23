import time
import pygame
import random

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Шарики')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    running = True
    screen2 = pygame.Surface(screen.get_size())
    x1, y1 = 0, 0
    drawing = False  # режим рисования выключен
    v = 100
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
                    cor_x += 10
                if event.key == pygame.K_LEFT:
                    cor_x -= 10
                if event.key == pygame.K_w:
                    v += 10
                if event.key == pygame.K_s:
                    v -= 10
                else:
                    break
        if ver == 1:
            tim = 0
            drawing = True
            x1, y1 = random.randint(80, 421), 0
            list1.append([-1, -1])
            list.append([x1, y1])
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
