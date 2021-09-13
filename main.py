import pygame
import os
import random

# Inicialización de pygame

pygame.mixer.quit()
pygame.mixer.pre_init(22100, -16, 2, 1024)
pygame.mixer.init(22100, -16, 2, 1024)
pygame.init()       # Necesario para inicializar sonidos

pygame.font.init()  # Necesario para inicializar fuentes


# Global constants

WINDOW_CELLS_X, WINDOW_CELLS_Y = 30, 30

SNAKE_WIDTH = 25
SNAKE_HEIGHT = 25
MAX_FOOD_VALUE = 9
FOOD_INTERVAL = 25

WIDTH, HEIGHT = SNAKE_WIDTH * WINDOW_CELLS_X, SNAKE_HEIGHT * WINDOW_CELLS_Y    # Game window size


WHITE = (255, 255, 255)     # Parameters for white color RGB
BLACK = (0, 0, 0)           # Parameters for black color RBG
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

COLLISION_FONT = pygame.font.SysFont('comicsans', 100)     # Font to show the winner
SNAKE_LENGTH_FONT = pygame.font.SysFont('comicsans', 50)     # Font to show the winner
FOOD_FONT = pygame.font.SysFont('comicsans', 40)     # Font to show the winner

FPS = 10            # Game Frames per Second

COLLISION = pygame.USEREVENT + 1           # Event for snake collision


SPACE_IMAGE = pygame.image.load(os.path.join('assets','space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana de juego
pygame.display.set_caption("Snake Game")       # Cambia el título de la ventana de juego


def generate_food (food_list, snake):
    x = random.randint(-WINDOW_CELLS_X//2+3, WINDOW_CELLS_X//2-3)
    y = random.randint(-WINDOW_CELLS_Y//2+4, WINDOW_CELLS_Y//2-3)
    while snake.count((x,y)) != 0:
        x = random.randint(-WINDOW_CELLS_X//2+3, WINDOW_CELLS_X//2-3)
        y = random.randint(-WINDOW_CELLS_Y//2+4, WINDOW_CELLS_Y//2-3)
    value = random.randint(1,MAX_FOOD_VALUE)
    food_list.append((x, y, value))
    print(food_list)

def eat_food(snake, food_list):
    food_eaten = 0
    snake_x, snake_y = snake[-1]
    for x, y, value in food_list:
        if snake_x == x and snake_y == y:
            food_eaten += value
            food_list.remove((x,y,value))
    return food_eaten

def draw_food (food_list):
    for x,y,value in food_list:
        draw_text = FOOD_FONT.render(str(value), 1, RED)
        WIN.blit(draw_text, (x * SNAKE_WIDTH + WIDTH//2, y * SNAKE_HEIGHT + HEIGHT//2))

def handle_collisions(snake):
    if snake.count(snake[-1]) > 1:
        pygame.event.post(pygame.event.Event(COLLISION))
    else:
        snake_x, snake_y = snake[-1]
        if snake_x <= -WINDOW_CELLS_X//2 or snake_x >= WINDOW_CELLS_X//2 or snake_y <= -WINDOW_CELLS_Y//2 + 3 or snake_y >= WINDOW_CELLS_Y//2 - 1:
            pygame.event.post(pygame.event.Event(COLLISION))

def draw_border():
    for y in range(3,WINDOW_CELLS_Y):
        for x in range(WINDOW_CELLS_X):
            if y == 3 or y == WINDOW_CELLS_Y-1:
                pygame.draw.rect(WIN, YELLOW, [x * SNAKE_WIDTH, y * SNAKE_HEIGHT - SNAKE_HEIGHT//2, SNAKE_WIDTH, SNAKE_HEIGHT])
            elif x == 0 or x == WINDOW_CELLS_X-1:
                pygame.draw.rect(WIN, YELLOW, [x * SNAKE_WIDTH, y * SNAKE_HEIGHT - SNAKE_HEIGHT//2, SNAKE_WIDTH, SNAKE_HEIGHT])

def draw_collision(text):
    draw_text = COLLISION_FONT.render(text, 1, YELLOW)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def draw_snake_length(snake, record_length):
    snake_length_text = SNAKE_LENGTH_FONT.render("Snake Length: " + str(len(snake)),1, WHITE)
    WIN.blit(snake_length_text, (10, 10))

    snake_length_record_text = SNAKE_LENGTH_FONT.render("Length Record: " + str(record_length),1, WHITE)
    WIN.blit(snake_length_record_text, (WIDTH - snake_length_record_text.get_width() - 10, 10))

def draw_window(snake, record_length, food_list):
    ''' Draws background and objects in window '''
    WIN.blit(SPACE, (0, 0))
    draw_border()
    draw_food (food_list)
    draw_snake_length(snake, record_length)
    for x,y in snake:
        pygame.draw.rect(WIN, WHITE, [x * SNAKE_WIDTH + WIDTH//2, y * SNAKE_HEIGHT + HEIGHT//2, SNAKE_WIDTH, SNAKE_HEIGHT])

    pygame.display.update()

def  main():

    snake_x, snake_y = (0,0)
    snake = [(snake_x, snake_y)]
    direction = (0,1)
    record_length = 0
    food = 5
    food_list = []
    generate_food(food_list, snake)
    launch_food_counter = FOOD_INTERVAL    # counter to launch new food
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = (0, -1)
                if event.key == pygame.K_DOWN:
                    direction = (0, 1)
                if event.key == pygame.K_LEFT:
                    direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    direction = (1, 0)

            if event.type == COLLISION:
                draw_collision("Colisión")
                if len(snake) > record_length:
                    record_length = len(snake)
                snake_x, snake_y = (0,0)
                snake = [(snake_x, snake_y)]
                direction = (0,1)
                food = 5
                food_list = []
                launch_food_counter = FOOD_INTERVAL
        
        snake_x += direction[0]
        snake_y += direction[1]
        if food > 0:
            food -= 1
        else:
            snake.pop(0)
        snake.append((snake_x, snake_y))
        if launch_food_counter == 0:
           generate_food(food_list, snake) 
           launch_food_counter = FOOD_INTERVAL
        else:
            launch_food_counter -= 1
        food += eat_food(snake, food_list)
        handle_collisions(snake)
        draw_window(snake, record_length, food_list)
        
    pygame.quit()

if __name__ == "__main__":
    main()

