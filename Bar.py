""" needs to be reworked """

import pygame
from Pygame_Engine.Functions import round_half_up

class Bar:
    def __init__(self, surface, width_height: tuple, xy: tuple, anchor="center",
                 foregroundcolor=(255, 255, 255),
                 backgroundcolor=(0, 0, 0),
                 bordercolor=(255, 255, 255),
                 borderwidth=1, borderradius=0):
        self.surface = surface
        self.width, self.height = width_height[0], width_height[1]
        self.xy = xy
        self.anchor = anchor
        self.borderwidth = borderwidth
        if self.borderwidth < 0:
            raise ValueError(
                f"Invalid argument for 'borderwidth': '{self.borderwidth}'.")
        elif self.borderwidth == 0:
            self.border_exists = False
        else:
            self.border_exists = True
        self.bordercolor = bordercolor
        self.foregroundcolor = foregroundcolor
        self.backgroundcolor = backgroundcolor
        self.borderradius = borderradius
        if type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) == tuple:
            if len(self.borderradius) != 4:
                raise ValueError(
                    f"Invalid argument for 'borderradius': {self.borderradius}.")

        self.pixels_filled = 0

        options = ["topleft", "topright", "bottomleft", "bottomright",
                   "center", "midtop", "midright", "midbottom", "midleft"]
        if self.anchor not in options:
            raise ValueError(
                f"Invalid argument for 'anchor': '{self.anchor}'.")

        self.background_rect = pygame.Rect(0, 0, self.width, self.height)

        if self.anchor == "topleft":
            self.background_rect.topleft = self.xy
        elif self.anchor == "topright":
            self.background_rect.topright = self.xy
        elif self.anchor == "bottomleft":
            self.background_rect.bottomleft = self.xy
        elif self.anchor == "bottomright":
            self.background_rect.bottomright = self.xy
        elif self.anchor == "center":
            self.background_rect.center = self.xy
        elif self.anchor == "midtop":
            self.background_rect.midtop = self.xy
        elif self.anchor == "midright":
            self.background_rect.midright = self.xy
        elif self.anchor == "midbottom":
            self.background_rect.midbottom = self.xy
        elif self.anchor == "midleft":
            self.background_rect.midleft = self.xy

        self.fill_rect = pygame.Rect(self.background_rect.x+int(
            self.borderwidth/2), self.background_rect.y, 0, self.background_rect.height)
        if self.border_exists == True:
            self.border_rect = pygame.Rect(self.background_rect.x, self.background_rect.y,
                                           self.background_rect.width, self.background_rect.height)

    def update(self, variable, variable_max):
        # calculate the width of the fill_rect
        percent = variable/variable_max
        if percent > 1:
            percent = 1
        if percent < 0:
            percent = 0
        self.pixels_filled = round_half_up(
            (self.background_rect.width-self.borderwidth)*percent)
        self.fill_rect = pygame.Rect(self.background_rect.x+int(self.borderwidth/2),
                                     self.background_rect.y, self.pixels_filled, self.background_rect.height)

    def update_colors(self, textcolor=None, backgroundcolor=None, bordercolor=None):
        if textcolor != None:
            self.textcolor = textcolor
            self.create()
        if backgroundcolor != None:
            self.backgroundcolor = backgroundcolor
        if bordercolor != None:
            self.bordercolor = bordercolor

    def draw(self):
        pygame.draw.rect(
            self.surface, self.backgroundcolor, self.background_rect, 0,
            border_top_left_radius=self.borderradius[0],
            border_top_right_radius=self.borderradius[1],
            border_bottom_right_radius=self.borderradius[2],
            border_bottom_left_radius=self.borderradius[3])
        pygame.draw.rect(self.surface, self.foregroundcolor, self.fill_rect, 0,
                         border_top_left_radius=self.borderradius[0],
                         border_top_right_radius=self.borderradius[1],
                         border_bottom_right_radius=self.borderradius[2],
                         border_bottom_left_radius=self.borderradius[3])
        if self.border_exists == True:
            pygame.draw.rect(
                self.surface, self.bordercolor, self.border_rect, self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3])

    def change_pos(self, xy: tuple, anchor="center"):
        if anchor == "topleft":
            self.background_rect.topleft = xy
        elif anchor == "topright":
            self.background_rect.topright = xy
        elif anchor == "bottomleft":
            self.background_rect.bottomleft = xy
        elif anchor == "bottomright":
            self.background_rect.bottomright = xy
        elif anchor == "center":
            self.background_rect.center = xy
        elif anchor == "midtop":
            self.background_rect.midtop = xy
        elif anchor == "midright":
            self.background_rect.midright = xy
        elif anchor == "midbottom":
            self.background_rect.midbottom = xy
        elif anchor == "midleft":
            self.background_rect.midleft = xy

        self.fill_rect.center = self.background_rect.center
        if self.border_exists == True:
            self.border_rect.center = self.background_rect.center
