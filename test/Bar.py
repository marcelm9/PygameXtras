from Pygame_Engine.classes.Bar import Bar

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600,400), display=1)
fpsclock = pygame.time.Clock()
fps = 60

b = Bar(screen, 
        width_height=(200, 40),
        xy=(300, 200),
        anchor="center",
        foregroundcolor=(0,255,0),
        backgroundcolor=(0,60,0),
        bordercolor=(0,0,0),
        borderwidth=1,
        borderradius=15)

val = 20
max_val = 100
change = 1

run = True
while run:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        val = max(0, min(val + change, max_val))
    if mouse[2]:
        val = max(0, min(val - change, max_val))
    b.update(val, max_val)
    if mouse[1]:
        b.change_pos(pygame.mouse.get_pos())
    
    screen.fill((64,64,128))
    b.draw()
    
    pygame.display.flip()
    fpsclock.tick(fps)