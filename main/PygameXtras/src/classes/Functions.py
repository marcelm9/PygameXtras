import ctypes
import os

import pygame


def win_higher_resolution(boolean: bool = True):
    """
    Most Windows PCs (automatically) use scaling to 150% which makes many applications appear
    blurry. To avoid this effect, this function can be called to increase the resolution on
    affected displays without having to manually change the scaling in the computers settings.
    """
    if os.name == "nt":
        ctypes.windll.shcore.SetProcessDpiAwareness(bool(boolean))


def draw_rect_alpha(
    surface,
    color,
    rect,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(
        shape_surf,
        color,
        shape_surf.get_rect(),
        width,
        border_radius,
        border_top_left_radius,
        border_top_right_radius,
        border_bottom_left_radius,
        border_bottom_right_radius,
    )
    surface.blit(shape_surf, rect)


def draw_circle_alpha(
    surface,
    color,
    center,
    radius,
    width: int = 0,
    draw_top_right: bool = True,
    draw_top_left: bool = True,
    draw_bottom_left: bool = True,
    draw_bottom_right: bool = True,
):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(
        shape_surf,
        color,
        (radius, radius),
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def ask_filename():
    """temporary method to get filename"""
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def ask_directory():
    """temporary method to get foldername"""
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


def get_fonts():
    return [
        f.removesuffix(".ttf")
        for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "fonts"))
    ]
