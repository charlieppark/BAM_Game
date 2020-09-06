import pygame
import random
import sys
import cmath

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode(
    (screen_width, screen_height))  # set screen size

pygame.display.set_caption("바나나 알러지 원숭이")  # title of game


class button():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True


playButton = button(465, 500, 350, 40)

# FPS
clock = pygame.time.Clock()

# Loading Background Image
print_start_screen = pygame.image.load("D:\\CS\\Python\\BAM_game\\start.png")

start_screen = True
game_screen = False

background = pygame.image.load("D:\\CS\\Python\\BAM_game\\background.png")

# Loading Character
character = pygame.image.load("D:\\CS\\Python\\BAM_game\\monkey.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height

to_x = 0

character_speed = 0.2

# enemy
enemy = pygame.image.load("D:\\CS\\Python\\BAM_game\\banana.png")
enemy.set_colorkey(None)
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, 1280)
enemy_y_pos = 0
drop_speed = 5


# font
timer_font = pygame.font.Font(None, 400)
result_font = pygame.font.Font("D:\\CS\\Python\\BAM_game\\NotoSansD.ttf", 40)

time_check = False

dt = clock.tick(60)  # frame per second

while start_screen:

    for event in pygame.event.get():

        screen.blit(print_start_screen, (0, 0))

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.isOver(pos):
                start_screen = False
                time_check = True

    pygame.display.update()  # refresh screen to show background

total_time = 4

start_ticks = pygame.time.get_ticks()

while time_check:

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    timer = timer_font.render(
        str(int(total_time - elapsed_time)), True, (0, 0, 0))

    screen.blit(background, (0, 0))
    screen.blit(timer, (screen_width/2 - 100,
                        screen_height/2 - 150))

    if total_time - elapsed_time <= 0:
        time_check = False
        game_screen = True

    pygame.display.update()  # refresh screen to show background


count = 0

while game_screen:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x * dt

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    enemy_y_pos += drop_speed + count

    if enemy_y_pos > screen_height:
        enemy_x_pos = random.randint(
            int(character_x_pos - 250), int(character_x_pos + 250))
        if enemy_x_pos < 0:
            enemy_x_pos *= -1
        elif enemy_x_pos > 1280:
            enemy_x_pos -= 1280
        enemy_y_pos = 0
        if count < 15:
            count += 1

    # collision
    character_rect = character.get_rect()
    character_rect.left = character_x_pos  # 25 for correction value
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        game_screen = False

    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    pygame.display.update()  # refresh screen to show background


message = " bananas! Great!"

if count <= 1:
    message = " banana! Are You Kidding?"

banana_count = result_font.render(
    str(count) + message, True, (0, 0, 0))

screen.blit(banana_count, (character_x_pos - 100, character_y_pos - 100))
pygame.display.update()  # refresh screen to show background

pygame.time.delay(5000)  # delay before quit(ms)

# quit pygame
pygame.quit()
