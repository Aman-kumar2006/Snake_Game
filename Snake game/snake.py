import pygame
import time
import random
import os


pygame.init()


width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 SNAKE GAME")


background_color = (18, 18, 18)
snake_color = (0, 255, 140)
food_color = (255, 82, 82)
score_text_color = (220, 220, 220)
grid_color = (40, 40, 40)


block = 20
snake_speed = 15
font = pygame.font.SysFont("consolas", 24)


eat_sound = None
bg_music_loaded = False


if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

def get_high_score():
    with open("highscore.txt", "r") as f:
        return int(f.read())

def update_high_score(score):
    high = get_high_score()
    if score > high:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

def score_display(score, high):
    value = font.render(f"Score: {score}  High Score: {high}", True, score_text_color)
    win.blit(value, [10, 10])

def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(win, snake_color, [x[0], x[1], block, block], border_radius=4)

def draw_grid():
    for x in range(0, width, block):
        pygame.draw.line(win, grid_color, (x, 0), (x, height))
    for y in range(0, height, block):
        pygame.draw.line(win, grid_color, (0, y), (width, y))

def game_over_screen(score):
    update_high_score(score)
    win.fill(background_color)
    
    msg1 = font.render("💥 Game Over!", True, food_color)
    msg2 = font.render("Press [R] to Restart  |  [Q] to Quit", True, score_text_color)
    msg3 = font.render(f"Final Score: {score}", True, score_text_color)
    
    win.blit(msg1, [width // 2 - msg1.get_width() // 2, height // 2 - 60])
    win.blit(msg3, [width // 2 - msg3.get_width() // 2, height // 2 - 20])
    win.blit(msg2, [width // 2 - msg2.get_width() // 2, height // 2 + 30])
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    waiting = False

def game_loop():
    x, y = width // 2, height // 2
    dx, dy = 0, 0
    snake_list = []
    length = 1
    food_x = round(random.randrange(0, width - block) / 20.0) * 20.0
    food_y = round(random.randrange(0, height - block) / 20.0) * 20.0
    score = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -block, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = block, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -block
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, block

        if x >= width or x < 0 or y >= height or y < 0:
            game_over_screen(score)
            return

        x += dx
        y += dy
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over_screen(score)
                return

        win.fill(background_color)
        draw_grid()
        pygame.draw.rect(win, food_color, [food_x, food_y, block, block], border_radius=4)
        draw_snake(block, snake_list)
        score_display(score, get_high_score())
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block) / 20.0) * 20.0
            length += 1
            score += 10
           

        clock.tick(snake_speed)


while True:
    game_loop()
