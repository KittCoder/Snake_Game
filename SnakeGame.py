# Snake Game
# 1/16/2023
# Simple Pygame implementation of classic Snake game

import pygame
import time
import random

pygame.init()

display_width = 600
display_height = 400

display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake Game')

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
yellow = (255,255,102)
green = (0,255,0)

clock = pygame.time.Clock()

snake_speed = 15
snake_block = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsans", 35)

def your_score(score):
    value = score_font.render('Your Score: ' + str(score), True, yellow)
    display.blit(value, [0,0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width/6, display_height/3])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        # x here is a list on two number the x coordinate is at index 0
        # and the y coordinate is at index one
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

def gameLoop():
    
    game_over = False
    game_close = False
    
    x1 = display_width/2
    y1 = display_height/2
    
    x1_change = 0
    y1_change = 0
    
    # This is the snake data structure
    snake_list = []
    length_of_snake = 1
    
    # This is the pellet data structure
    food_list = []
    eating = False
    for elt in range(5):
        foodx = round(random.randrange(0, display_width - snake_block)/10) * 10
        foody = round(random.randrange(0, display_height - snake_block)/10) * 10
        food_list.append((foodx, foody))
    
    while not game_over:
        
        # This loop is responsible for waiting for the player to decide 
        # if they want to quit or continue.
        
        while game_close == True:
            display.fill(blue)
            message('You lost! Press Q-Quit or C-Play Again', red)
            your_score(length_of_snake - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()
                        
        for event in pygame.event.get():                 
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block
            
        # This code identifies if your snake hits the screen boundry.
        if x1 > display_width or x1 < 0 or y1 > display_height or y1 < 0:
            game_close = True
            
        x1 += x1_change
        y1 += y1_change
        display.fill(blue)

        # Draw the single food pellet that is randomly positioned on the screen
        for elt in food_list:
            pygame.draw.rect(display, green, [elt[0],elt[1], snake_block, snake_block]) 
        
        # Accumulate the snake - start adding links to the snake
        # The links that we add are the current position of the snake
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)
        
        # we need to keep track of the snake list to equal the variable 
        # that tracks the actual Length of the snake.
        # if the snake list is longer than delete oldest snake link
        
        # we are keeping the Last Length_of_snake links in our snake_list
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        # traverse the snake list and see if the current position of the
        # snake head is already a link in the body. If it is, we have folded
        # on ourself and the game is over
        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True
        
        draw_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)
        pygame.display.update()
        
        # testing if snake ate a pellet
        for elt in food_list:
            if x1 == elt[0] and y1 == elt[1]:
                food_list.remove(elt)
                eating = True
            
                
        if eating == True:
            # Create and manage multiple food pellets
            foodx = round(random.randrange(0, display_width - snake_block)/10) * 10
            foody = round(random.randrange(0, display_height - snake_block)/10) * 10
            length_of_snake += 1
            food_list.append((foodx, foody))
            eating = False
            
        clock.tick(snake_speed)

    pygame.quit()

# This runs the game  
gameLoop()