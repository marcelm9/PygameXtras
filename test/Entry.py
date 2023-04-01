from Pygame_Engine.classes.Entry import Entry

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600,400), display=1)
fpsclock = pygame.time.Clock()
fps = 60

e = Entry(screen, "", 32, (screen.get_width()//2, screen.get_height()//2), bw=1, fd=(400,60))

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

    e.update(event_list)
    if e.get_state() == 1:
        e.update_colors(bordercolor=(0,255,0))
    else:
        e.update_colors(bordercolor=(0,0,0))
    
    screen.fill((64,64,128))
    e.draw()
    
    pygame.display.flip()
    fpsclock.tick(fps)