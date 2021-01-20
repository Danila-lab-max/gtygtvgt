import time
import pygame
import random
import os
import sys
from pygame.locals import *
import sqlite3

con = sqlite3.connect("Pygame.sqlite")
cur = con.cursor()
names = cur.execute("""SELECT name FROM users""").fetchall()
result = cur.execute("""SELECT * FROM users""").fetchall()
result.sort(key=lambda x: x[1])
result.reverse()
print(result)

pygame.init()
screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
name_user = str()


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    global name_user
                    name_user = self.text
                    screen.fill("blue")
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_boxes = [input_box1]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((255, 255, 255))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def finish_screen(score, score0):
    if int(score) > int(score0):
        score0 = score
    intro_text = ["Конец!!!",
                  "Ваш результат - " + str(score),
                  "Лучший результат - " + str(score0)]

    fon = pygame.transform.scale(load_image('p.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 40
    if int(score) >= int(score0):
        result = cur.execute("""UPDATE users
                    SET score = ?
                    WHERE name = ?""", (score, name_user)).fetchall()
        con.commit()
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
                if event.key == K_d:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def draw(screen, score, speed):
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


def add_pictures():
    surf1 = pygame.image.load('desert.jpg')
    surf = pygame.transform.scale(surf1, (501, 501))
    rect = surf.get_rect(
        bottomright=(501, 501))
    screen.blit(surf, rect)
    draw(screen, str(int(point // 100)), str(v_show))
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
    screen.blit(screen2, (0, 0))


pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50

clock = pygame.time.Clock()


def start_screen():
    intro_text = ["Правила: Нужно передвигать машину",
                  "клавишами, не врезаясь в другие машины."]

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
    main()
    pygame.quit()
    pygame.init()
    score0 = 0
    print(names)
    if (name_user,) not in names:
        score0 = 0
        result = cur.execute("""INSERT INTO users VALUES (?, ?)""", (name_user, 0)).fetchall()
        con.commit()
    else:
        for i in result:
            if name_user in i:
                score0 = i[1]
                print(score0)
                break
    pygame.display.set_caption('Машинки')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    running = True
    screen2 = pygame.Surface(screen.get_size())
    x1, y1 = 0, 0
    drawing = False
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
    delta_point = 1
    surf1 = pygame.image.load('desert.jpg')
    surf = pygame.transform.scale(surf1, (100, 501))
    rect = surf.get_rect(
        bottomright=(400, 501))
    screen.blit(surf, rect)
    clock = pygame.time.Clock()
    while running:
        ver = random.choice([1] + [0] * 100)
        point1 = point
        point += delta_point
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                    delta_point += 0.1
                if event.key == pygame.K_s:
                    if v_show == 50:
                        delta_point = 0
                    else:
                        delta_point -= 0.1
                    if v_show > 50:
                        v -= 10
                        v_show -= 1
                else:
                    break
        if ver == 1:
            tim = 0
            drawing = True
            x1, y1 = random.randint(190, 390), 0
            for i in list:
                if not (x1 <= i[0] - 100 or x1 >= i[0] + 100):
                    drawing = False
                    break
            if drawing:
                list1.append([-1, -1])
                list.append([x1, y1])
        add_pictures()
        s = v * clock.tick() / 1000
        for i in range(len(list)):
            point1 = point
            point += delta_point
            surf1 = pygame.image.load('3 (2).png')
            surf = pygame.transform.scale(surf1, (80, 100))
            rect = surf.get_rect(
                bottomright=(list[i][0], list[i][1]))
            screen.blit(surf, rect)
            list[i][1] -= s / list1[i][1]
        l = list.copy()
        list = []
        for i in l:
            if i[1] >= 501:
                continue
            else:
                list.append(i)
            if -30 <= i[0] - cor_x <= 30 and -30 <= i[1] - cor_y <= 30:
                l.clear()
                list.clear()
                v_show = 60
                v = 100
                cor_x = 250
                cor_y = 400
                finish_screen(str(int(point // 100)), score0)
                point = 0
                point1 = 0
                delta_point = 1
        screen2.blit(screen, (0, 0))
        pygame.display.flip()
