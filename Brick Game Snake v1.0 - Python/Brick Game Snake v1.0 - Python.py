#====================================================================================================
#====================================================================================================
# Program : Python - Brick Game Snake v1.0
# By      : Suprovo Basak
# Date    : 30-May-2023
#====================================================================================================
#====================================================================================================

import pygame
import numpy
import random

#====================================================================================================

pygame.mixer.init(channels = 1, allowedchanges = 0)
pygame.init()
window_resolution = (340,340)
window = pygame.display.set_mode(window_resolution)
pygame.display.set_caption("Python - Brick Game Snake v1.0")
try:
    icon = pygame.image.load("Icon.png") #Resolution 32x32
    pygame.display.set_icon(icon)
except:
    pass

#====================================================================================================

violet = (102, 45, 145)
indigo = (0, 0, 255)
blue = ( 0, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
orange = (242, 101, 34)
red = ( 255, 0, 0)
white = (255, 255, 255)
grey = (127, 127, 127)
black = (0, 0, 0)

colors = (violet, indigo, blue, green, yellow, orange, red)

#--------------------------------------------------

background_color = (230, 230, 230)
border_color = (205, 205, 205)
python_blue = (68, 125, 175)
python_yellow = (255, 216, 69)
food_color = None

#==================================================

bricks = [[0] * 10 for i in range(20)]

#==================================================

snake = [[4, 11], [4, 10], [4, 9]]

#====================================================================================================

def gen_tone(frequency, amplitude = 1, duration = 0.5, decay = -8):
    time = numpy.arange(0, duration, 1 / 44100)
    return amplitude * numpy.exp(decay * time) * numpy.sin(2 * numpy.pi * frequency * time)

#==================================================

def spawn_food():
    space = []
    for y in range(20):
        for x in range(10):
            if ([x, y] not in snake):
                space.append([x, y])
    food = random.choice(space)
    bricks[food[1]][food[0]] = 1

#==================================================

def random_color_except(color):
    valid_colors = []
    for i in colors:
        if (i != color):
            valid_colors.append(i)
    return random.choice(valid_colors)

#--------------------------------------------------

def dark_color(color, darkness = 0.5):
    return (int(color[0] * darkness), int(color[1] * darkness), int(color[2] * darkness))

#==================================================

def draw_brick(surface, point_xy, color):
    if (-1 < point_xy[0] and point_xy[0] < 10 and -1 < point_xy[1] and point_xy[1] < 20):
        pygame.draw.rect(surface, black, (point_xy[0] * 15 + 20, point_xy[1] * 15 + 20, 16, 16))
        pygame.draw.rect(surface, color, (point_xy[0] * 15 + 21, point_xy[1] * 15 + 21, 14, 14))
        pygame.draw.line(window, white, [point_xy[0] * 15 + 23, point_xy[1] * 15 + 22], [point_xy[0] * 15 + 33, point_xy[1] * 15 + 22])
        pygame.draw.line(window, white, [point_xy[0] * 15 + 33, point_xy[1] * 15 + 23], [point_xy[0] * 15 + 33, point_xy[1] * 15 + 32])
        pygame.draw.line(window, dark_color(color), [point_xy[0] * 15 + 22, point_xy[1] * 15 + 23], [point_xy[0] * 15 + 22, point_xy[1] * 15 + 32])
        pygame.draw.line(window, dark_color(color), [point_xy[0] * 15 + 22, point_xy[1] * 15 + 33], [point_xy[0] * 15 + 32, point_xy[1] * 15 + 33])

#--------------------------------------------------

def draw_blinking_brick(surface, point_xy, color, frame_count):
    if (-1 < point_xy[0] and point_xy[0] < 10 and -1 < point_xy[1] and point_xy[1] < 20):
        if (frame_count % 6 > 0 and frame_count % 6 <= 3):
            draw_brick(surface, point_xy, color)
        elif (frame_count % 6 > 3 or frame_count % 6 == 0):
            draw_brick(surface, point_xy, white)

#--------------------------------------------------

def write_text(surface, text, centre_xy, angle = 0, size = 18, bold = False, underline = False, fg_color = black, bg_color = None):
    font = pygame.font.SysFont("arial", size)
    font.set_bold(bold)
    font.set_underline(underline)
    image = font.render(text, True, fg_color, bg_color).convert_alpha()
    image = pygame.transform.rotate(image, angle)
    surface.blit(image, (centre_xy[0] - image.get_width() // 2, centre_xy[1] - image.get_height() // 2))

#--------------------------------------------------

def canvas_render(surface, frame_count, score, game_over, won):
    surface.fill(background_color)
    surface.fill(border_color, [18, 18, 155, 305])
    surface.fill(white, [20, 20, 151, 301])
    surface.fill(border_color, [219, 105, 74, 74])
    surface.fill(white, [221, 107, 70, 70])
    write_text(surface, "Brick Game", (256, 28), size = 24, underline = True)
    write_text(surface, "Score :", (243, 90))
    write_text(surface, str(score), (256, 140), size = 24, bold = True)
    if (game_over == True):
        write_text(surface, "Game Over", (255, 242), size = 24, fg_color = red)
    if (won == True):
        write_text(surface, "Winner", (255, 242), size = 24, fg_color = indigo)
    write_text(surface, "By : Suprovo Basak.", (256, 310))
    for y in range(20):
        for x in range(10):
            if (bricks[y][x] == 1):
                draw_brick(surface, (x, y), food_color)
            elif (bricks[y][x] == 2):
                if (game_over == False):
                    draw_blinking_brick(surface, (x, y), python_blue, frame_count)
                else:
                    draw_brick(surface, (x, y), python_blue)
            elif (bricks[y][x] == 3):
                draw_brick(surface, (x, y), python_yellow)

#====================================================================================================
#====================================================================================================

def main():
    global snake, food_color
    program_running = True
    key_input = 0
    move_direction = 0
    game_speed = 5
    game_over = False
    won = False
    no_food = True
    highest = 197
    score = 0
    score_sound = gen_tone(880, 4096).astype(numpy.int16)
    game_over_sound = numpy.append(gen_tone(440, 4096, 0.1), gen_tone(220, 4096, 0.4)).astype(numpy.int16)
    won_sound = numpy.append(gen_tone(880, 4096), gen_tone(1760, 4096)).astype(numpy.int16)
    frame_count = 0
    fps = 30
    main_clock = pygame.time.Clock()
    while (program_running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                program_running = False
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_RIGHT):
                    key_input = 1
                elif (event.key == pygame.K_UP):
                    key_input = 2
                elif (event.key == pygame.K_LEFT):
                    key_input = 3
                elif (event.key == pygame.K_DOWN):
                    key_input = 4
        if (frame_count % (fps / game_speed) == 0):
            if (move_direction == 0):
                if (key_input != 4):
                    move_direction = key_input
            elif (key_input == 1 and move_direction != 3):
                move_direction = key_input
            elif (key_input == 2 and move_direction != 4):
                move_direction = key_input
            elif (key_input == 3 and move_direction != 1):
                move_direction = key_input
            elif (key_input == 4 and move_direction != 2):
                move_direction = key_input
            if (game_over == False and won == False):
                if (move_direction == 1 and (snake[-1][0] == 9 or bricks[snake[-1][1]][snake[-1][0] + 1] == 3) or
                    move_direction == 2 and (snake[-1][1] == 0 or bricks[snake[-1][1] - 1][snake[-1][0]] == 3) or
                    move_direction == 3 and (snake[-1][0] == 0 or bricks[snake[-1][1]][snake[-1][0] - 1] == 3) or
                    move_direction == 4 and (snake[-1][1] == 19 or bricks[snake[-1][1] + 1][snake[-1][0]] == 3)):
                    game_over = True
                    pygame.mixer.Sound(game_over_sound).play()
        if(won == False and score == highest):
            won = True
            pygame.mixer.Sound(won_sound).play()
        if (game_over == False and won == False):
            if (no_food == True):
                food_color = random_color_except(food_color)
                spawn_food()
                no_food = False
            if (frame_count % (fps / game_speed) == 0 and move_direction != 0):
                if (move_direction == 1 and bricks[snake[-1][1]][snake[-1][0] + 1] == 1):
                    snake.append([snake[-1][0] + 1, snake[-1][1]])
                    no_food = True
                    score += 1
                    pygame.mixer.Sound(score_sound).play()
                elif (move_direction == 2 and bricks[snake[-1][1] - 1][snake[-1][0]] == 1):
                    snake.append([snake[-1][0], snake[-1][1] - 1])
                    no_food = True
                    score += 1
                    pygame.mixer.Sound(score_sound).play()
                elif (move_direction == 3 and bricks[snake[-1][1]][snake[-1][0] - 1] == 1):
                    snake.append([snake[-1][0] - 1, snake[-1][1]])
                    no_food = True
                    score += 1
                    pygame.mixer.Sound(score_sound).play()
                elif (move_direction == 4 and bricks[snake[-1][1] + 1][snake[-1][0]] == 1):
                    snake.append([snake[-1][0], snake[-1][1] + 1])
                    no_food = True
                    score += 1
                    pygame.mixer.Sound(score_sound).play()
                else:
                    for i in range(len(snake)):
                        bricks[snake[i][1]][snake[i][0]] = 0
                        if (i < len(snake) - 1):
                            snake[i] = snake[i + 1].copy()
                        else:
                            if (move_direction == 1):
                                snake[i][0] += 1
                            elif (move_direction == 2):
                                snake[i][1] -= 1
                            elif (move_direction == 3):
                                snake[i][0] -= 1
                            elif (move_direction == 4):
                                snake[i][1] += 1
            for i in range(len(snake)):
                if (i < len(snake) - 1):
                    bricks[snake[i][1]][snake[i][0]] = 3
                else:
                    bricks[snake[i][1]][snake[i][0]] = 2
        canvas_render(window, frame_count, score, game_over, won)
        frame_count += 1
        if (frame_count > fps):
            frame_count = 1
        pygame.display.flip()
        main_clock.tick(fps)

#====================================================================================================

main()

#====================================================================================================
#====================================================================================================
# The End.
#====================================================================================================
#====================================================================================================
