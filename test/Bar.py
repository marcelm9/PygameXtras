from Pygame_Engine.classes.Bar import Bar

class NewBar:
    def __init__(self, surface, size: tuple, xy: tuple, anchor: str = "center", **kwargs):
        """
        Creates a bar.

        Instructions:
            - To create a bar, create an instance of this class before
            the mainloop of the game
            - To make the bar appear, call the method 'self.draw()' in
            every loop of the game.

        Example (simplified):
            bar = Bar(screen, (100, 25), (100, 100))
            while True:
                bar.update(player_health, player_max_health)
                bar.draw()

        Arguments:
            surface
                the surface the object will be drawn onto
                Type: pygame.Surface
            size
                width and height of the bar
                Type: tuple, list
            xy
                position of the anchor
                Type: tuple, list
            anchor
                the anchor of the object:   topleft,    midtop,    topright,
                                            midleft,    center,    midright,
                                            bottomleft, midbottom, bottomright
            backgroundcolor
            fillcolor
            bordercolor
            borderwidth
            borderradius (?)
            
        """


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