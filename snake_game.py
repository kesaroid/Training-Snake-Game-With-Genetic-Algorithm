import pygame
import numpy as np
import time
import random

def eat_apple(apple_position, score):
    apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    score += 1
    return apple_position, score

def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    else:
        return 0

def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0]+ current_direction_vector
    snake_head = snake_position[0]
    if collision_with_self(snake_position) == 1:
        return 1
    else:
        return 0

def generate_snake(snake_head, snake_position, apple_position, button_direction, score):

    if button_direction == 1:
        snake_head[0] += 10
    elif button_direction == 0:
        snake_head[0] -= 10
    elif button_direction == 2:
        snake_head[1] += 10
    elif button_direction == 3:
        snake_head[1] -= 10
    else:
        pass

    if snake_head == apple_position:
        apple_position, score = eat_apple(apple_position, score)
        snake_position.insert(0,list(snake_head))

    elif snake_head[0]<0:
        snake_head[0] = 500
    elif snake_head[1]<=0:
        snake_head[1] = 500
    elif snake_head[0]>=500:
        snake_head[0] = 0
    elif snake_head[1]>=500:
        snake_head[1] = 0

    else:
        snake_position.insert(0,list(snake_head))
        snake_position.pop()
        
    return snake_position, apple_position, score

def display_snake(snake_position):
    for position in snake_position:
        pygame.draw.rect(display,red,pygame.Rect(position[0],position[1],10,10))

def display_apple(display,apple_position):
    pygame.draw.rect(display,green,pygame.Rect(apple_position[0],apple_position[1],10,10))

def play_game(snake_head, snake_position, apple_position, button_direction, score):
    crashed = False
    prev_button_direction = 1
    button_direction = 1
    current_direction_vector = np.array(snake_position[0])-np.array(snake_position[1])

    while not crashed:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and prev_button_direction != 1:
                    button_direction = 0
                elif event.key == pygame.K_RIGHT and prev_button_direction != 0:
                    button_direction = 1
                elif event.key == pygame.K_UP and prev_button_direction != 2:
                    button_direction = 3
                elif event.key == pygame.K_DOWN and prev_button_direction != 3:
                    button_direction = 2
                else:
                    button_direction = button_direction
        
        display.fill(window_color)
        display_apple(display,apple_position)
        display_snake(snake_position)

        snake_position, apple_position, score = generate_snake(snake_head, snake_position, apple_position, button_direction, score)
        pygame.display.set_caption("Snake Game"+"  "+"SCORE: "+str(score))
        pygame.display.update()
        prev_button_direction = button_direction
        if is_direction_blocked(snake_position, current_direction_vector) == 1:
            crashed = True

        clock.tick(20)
    return score


def display_final_score(display_text, final_score):
    largeText = pygame.font.Font('freesansbold.ttf',35)
    TextSurf = largeText.render(display_text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

if __name__ == "__main__":
    
    display_width = 500
    display_height = 500
    green = (0,255,0)
    red = (255,0,0)
    black = (0,0,0)
    window_color = (100,100,200)
    clock=pygame.time.Clock() 
    
    snake_head = [250,250]
    snake_position = [[250,250],[240,250],[230,250]]
    apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    score = 0
    
    pygame.init() 

    display = pygame.display.set_mode((display_width,display_height))
    display.fill(window_color)
    pygame.display.update()
    
    final_score = play_game(snake_head, snake_position, apple_position, 1, score)
    display = pygame.display.set_mode((display_width,display_height))
    display.fill(window_color)
    pygame.display.update()

    display_text = 'Your Score is: ' + str(final_score)
    display_final_score(display_text, final_score)

    pygame.quit()
