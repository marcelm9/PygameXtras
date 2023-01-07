import pygame
import math
import os
import json
import sys
import ctypes


def higher_resolution(boolean: bool = True):
    """ probably only works on windows os """
    ctypes.windll.shcore.SetProcessDpiAwareness(bool(boolean))


def scale_image(image, factor):
    """
    Changes the size of an image while keeping its proportions.
    """
    return pygame.transform.scale(image, (int(image.get_width()*factor), int(image.get_height()*factor)))


def rotate_in_place(rect, image, degrees):
    """
    ONLY WORKS WITH SPRITES

    Usage:
    self.rect, self.image = rotate_in_place(self.rect, self.image)
    """
    old_rect_center = rect.center
    new_image = pygame.transform.rotate(image, degrees)
    new_rect = new_image.get_rect()
    new_rect.center = old_rect_center
    return new_rect, new_image


def create_animation(image_ids: list, frames_per_image: list):
    """
    create a dict with image_ids and corresponding
    images before using this function.

    If usage unclear, refer to:
    marcel-python-programs\PYGAME_GAMES\pve\mini_warfare\data\player.py
    """
    assert len(image_ids) == len(frames_per_image), "received lists of different lengths"
    seq = []
    for image_id, count in zip(image_ids, frames_per_image):
        for i in range(count):
            seq.append(image_id)
    return seq


def get_distance(xy1, xy2, digits_after_comma=None):
    x1, y1 = xy1[0], xy1[1]
    x2, y2 = xy2[0], xy2[1]
    if digits_after_comma == None:
        return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
    else:
        return round_half_up(math.sqrt(((x2-x1)**2)+((y2-y1)**2)), digits_after_comma)


def get_angle_between_points(xy1, xy2):
    vect = pygame.math.Vector2(xy2[0]-xy1[0], xy2[1]-xy1[1]).normalize()
    cos = round_half_up(vect.y, 2)
    deg_cos = int(math.degrees(math.acos(vect.x)))
    if cos <= 0:
        return deg_cos
    else:
        return 180 + (180-deg_cos)


def get_normalized_vector_between_points(xy1, xy2):
    vect = pygame.math.Vector2(xy2[0]-xy1[0], xy2[1]-xy1[1])
    if vect.length() > 0:
        vect.normalize()
    return vect


def get_normalized_vector_from_angle(angle):
    vect = pygame.Vector2(round_half_up(math.cos(math.radians(
        angle)), 3), round_half_up(math.sin(math.radians(angle)), 3))
    return vect.normalize()


def round_half_up(n, decimals=0):
    if isinstance(n, int):
        return n
    multiplier = 10 ** decimals
    if decimals == 0:
        return int(math.floor(n*multiplier + 0.5) / multiplier)
    else:
        return math.floor(n*multiplier + 0.5) / multiplier


def vect_sum(a: tuple, b: tuple):
    if len(a) != len(b):
        raise ValueError("Received vectors of different dimensions.")
    vect = []
    for num1, num2 in zip(a, b):
        vect.append(num1+num2)
    return tuple(vect)


def vs(a: tuple, b: tuple):
    """ vect_sum(...) """ 
    return vect_sum(a, b)


def invert(a: tuple):
    """ inverts a vector """
    return (-a[0], -a[1])


def inv(a: tuple):
    """ invert(...) """ 
    return invert(a)
    

def load_image(path, size: tuple[int, int] = None, colorkey: tuple[int, int, int] = None):
    """ example for <path>: data/images/image1 """
    assert type(path) == str, f"invalid argument for 'path': {path}"
    if "/" in path:
        splitted = path.split("/")
        path = os.path.join(*splitted)

    try:
        img = pygame.image.load(path)
    except:
        raise Exception("image '" + str(path) + "' not found")
    
    if size != None:
        # assertions
        assert type(size) in [tuple, list], f"invalid argument for 'size': {size}"
        assert len(size) == 2, f"invalid argument for 'size': {size}"
        for item in size:
            assert type(item) == int, f"invalid argument for 'size': {size}"
            assert item > 0, f"invalid argument for 'size': {size}"
        
        img = pygame.transform.scale(img, size)
    
    if colorkey != None:
        # assertions
        assert type(colorkey) in [tuple, list], f"invalid argument for 'colorkey': {colorkey}"
        assert len(colorkey) == 3, f"invalid argument for 'colorkey': {colorkey}"
        for item in colorkey:
            assert type(item) == int, f"invalid argument for 'colorkey': {colorkey}"
            assert 0 <= item <= 255, f"invalid argument for 'colorkey': {colorkey}"
        
        img.set_colorkey(colorkey)
    
    return img


def draw_rect_alpha(surface, color, rect,  width: int = 0, border_radius: int = -1, border_top_left_radius: int = -1, border_top_right_radius: int = -1, border_bottom_left_radius: int = -1, border_bottom_right_radius: int = -1):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), width, border_radius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)
    surface.blit(shape_surf, rect)


def draw_circle_alpha(surface, color, center, radius, width: int = 0, draw_top_right: bool = None, draw_top_left: bool = None, draw_bottom_left: bool = None, draw_bottom_right: bool = None):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius, width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def ask_filename():
    """ temporary method to get filename """
    import tkinter.filedialog
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def ask_directory():
    """ temporary method to get foldername """
    import tkinter.filedialog
    top = tkinter.Tk()
    top.withdraw()  # hide window
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


class Colors:
    ### to avoid having to initialize it ###
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    lime = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    silver = (192, 192, 192)
    gray = (128, 128, 128)
    maroon = (128, 0, 0)
    olive = (128, 128, 0)
    green = (0, 128, 0)
    purple = (128, 0, 128)
    teal = (0, 128, 128)
    navy = (0, 0, 128)
    maroon = (128, 0, 0)
    dark_red = (139, 0, 0)
    brown = (165, 42, 42)
    firebrick = (178, 34, 34)
    crimson = (220, 20, 60)
    red = (255, 0, 0)
    tomato = (255, 99, 71)
    coral = (255, 127, 80)
    indian_red = (205, 92, 92)
    light_coral = (240, 128, 128)
    dark_salmon = (233, 150, 122)
    salmon = (250, 128, 114)
    light_salmon = (255, 160, 122)
    orange_red = (255, 69, 0)
    dark_orange = (255, 140, 0)
    orange = (255, 165, 0)
    gold = (255, 215, 0)
    dark_golden_rod = (184, 134, 11)
    golden_rod = (218, 165, 32)
    pale_golden_rod = (238, 232, 170)
    dark_khaki = (189, 183, 107)
    khaki = (240, 230, 140)
    olive = (128, 128, 0)
    yellow = (255, 255, 0)
    yellow_green = (154, 205, 50)
    dark_olive_green = (85, 107, 47)
    olive_drab = (107, 142, 35)
    lawn_green = (124, 252, 0)
    chart_reuse = (127, 255, 0)
    green_yellow = (173, 255, 47)
    dark_green = (0, 100, 0)
    green = (0, 128, 0)
    forest_green = (34, 139, 34)
    lime = (0, 255, 0)
    lime_green = (50, 205, 50)
    light_green = (144, 238, 144)
    pale_green = (152, 251, 152)
    dark_sea_green = (143, 188, 143)
    medium_spring_green = (0, 250, 154)
    spring_green = (0, 255, 127)
    sea_green = (46, 139, 87)
    medium_aqua_marine = (102, 205, 170)
    medium_sea_green = (60, 179, 113)
    light_sea_green = (32, 178, 170)
    dark_slate_gray = (47, 79, 79)
    teal = (0, 128, 128)
    dark_cyan = (0, 139, 139)
    aqua = (0, 255, 255)
    cyan = (0, 255, 255)
    light_cyan = (224, 255, 255)
    dark_turquoise = (0, 206, 209)
    turquoise = (64, 224, 208)
    medium_turquoise = (72, 209, 204)
    pale_turquoise = (175, 238, 238)
    aqua_marine = (127, 255, 212)
    powder_blue = (176, 224, 230)
    cadet_blue = (95, 158, 160)
    steel_blue = (70, 130, 180)
    corn_flower_blue = (100, 149, 237)
    deep_sky_blue = (0, 191, 255)
    dodger_blue = (30, 144, 255)
    light_blue = (173, 216, 230)
    sky_blue = (135, 206, 235)
    light_sky_blue = (135, 206, 250)
    midnight_blue = (25, 25, 112)
    navy = (0, 0, 128)
    dark_blue = (0, 0, 139)
    medium_blue = (0, 0, 205)
    blue = (0, 0, 255)
    royal_blue = (65, 105, 225)
    blue_violet = (138, 43, 226)
    indigo = (75, 0, 130)
    dark_slate_blue = (72, 61, 139)
    slate_blue = (106, 90, 205)
    medium_slate_blue = (123, 104, 238)
    medium_purple = (147, 112, 219)
    dark_magenta = (139, 0, 139)
    dark_violet = (148, 0, 211)
    dark_orchid = (153, 50, 204)
    medium_orchid = (186, 85, 211)
    purple = (128, 0, 128)
    thistle = (216, 191, 216)
    plum = (221, 160, 221)
    violet = (238, 130, 238)
    magenta = (255, 0, 255)
    orchid = (218, 112, 214)
    medium_violet_red = (199, 21, 133)
    pale_violet_red = (219, 112, 147)
    deep_pink = (255, 20, 147)
    hot_pink = (255, 105, 180)
    light_pink = (255, 182, 193)
    pink = (255, 192, 203)
    antique_white = (250, 235, 215)
    beige = (245, 245, 220)
    bisque = (255, 228, 196)
    blanched_almond = (255, 235, 205)
    wheat = (245, 222, 179)
    corn_silk = (255, 248, 220)
    lemon_chiffon = (255, 250, 205)
    light_golden_rod_yellow = (250, 250, 210)
    light_yellow = (255, 255, 224)
    saddle_brown = (139, 69, 19)
    sienna = (160, 82, 45)
    chocolate = (210, 105, 30)
    peru = (205, 133, 63)
    sandy_brown = (244, 164, 96)
    burly_wood = (222, 184, 135)
    tan = (210, 180, 140)
    rosy_brown = (188, 143, 143)
    moccasin = (255, 228, 181)
    navajo_white = (255, 222, 173)
    peach_puff = (255, 218, 185)
    misty_rose = (255, 228, 225)
    lavender_blush = (255, 240, 245)
    linen = (250, 240, 230)
    old_lace = (253, 245, 230)
    papaya_whip = (255, 239, 213)
    sea_shell = (255, 245, 238)
    mint_cream = (245, 255, 250)
    slate_gray = (112, 128, 144)
    light_slate_gray = (119, 136, 153)
    light_steel_blue = (176, 196, 222)
    lavender = (230, 230, 250)
    floral_white = (255, 250, 240)
    alice_blue = (240, 248, 255)
    ghost_white = (248, 248, 255)
    honeydew = (240, 255, 240)
    ivory = (255, 255, 240)
    azure = (240, 255, 255)
    snow = (255, 250, 250)
    black = (0, 0, 0)
    dim_gray = (105, 105, 105)
    gray = (128, 128, 128)
    dark_gray = (169, 169, 169)
    silver = (192, 192, 192)
    light_gray = (211, 211, 211)
    gainsboro = (220, 220, 220)
    white_smoke = (245, 245, 245)
    white = (255, 255, 255)

    # 256 values from 'black' (0) to white (255)
    transition_black_white = [(i, i, i) for i in range(256)]

    def __init__(self):
        """
        Contains loads of colors as rgb values.

        Notice 'transition_black_white'!
        """
        ### OLD ###
        # self.AQUA =        (0, 255, 255)
        # self.BLACK =       (0, 0, 0)
        # self.BLUE =        (0, 0, 255)
        # self.ORANGE =      (255, 165, 0)
        # self.GRAY =        (128, 128, 128)
        # self.GREEN =       (0, 128, 0)
        # self.LIME =        (0, 255, 0)
        # self.MAROON =      (128, 0, 0)
        # self.NAVY_BLUE =   (0, 0, 128)
        # self.OLIVE =       (128, 128, 0)
        # self.PURPLE =      (128, 0, 128)
        # self.RED =         (255, 0, 0)
        # self.SILVER =      (192, 192, 192)
        # self.TEAL =        (0, 128, 128)
        # self.WHITE =       (255, 255, 255)
        # self.YELLOW =      (255, 255, 0)
        # self.GRASSCOLOR =  (24, 255, 0)
        # # also lowercase
        # self.aqua =        (0, 255, 255)
        # self.black =       (0, 0, 0)
        # self.blue =        (0, 0, 255)
        # self.orange =      (255, 165, 0)
        # self.gray =        (128, 128, 128)
        # self.green =       (0, 128, 0)
        # self.lime =        (0, 255, 0)
        # self.maroon =      (128, 0, 0)
        # self.navy_blue =   (0, 0, 128)
        # self.olive =       (128, 128, 0)
        # self.purple =      (128, 0, 128)
        # self.red =         (255, 0, 0)
        # self.silver =      (192, 192, 192)
        # self.teal =        (0, 128, 128)
        # self.white =       (255, 255, 255)
        # self.yellow =      (255, 255, 0)
        # self.grasscolor =  (24, 255, 0)

        ### NEW ###
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.lime = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.cyan = (0, 255, 255)
        self.magenta = (255, 0, 255)
        self.silver = (192, 192, 192)
        self.gray = (128, 128, 128)
        self.maroon = (128, 0, 0)
        self.olive = (128, 128, 0)
        self.green = (0, 128, 0)
        self.purple = (128, 0, 128)
        self.teal = (0, 128, 128)
        self.navy = (0, 0, 128)
        self.maroon = (128, 0, 0)
        self.dark_red = (139, 0, 0)
        self.brown = (165, 42, 42)
        self.firebrick = (178, 34, 34)
        self.crimson = (220, 20, 60)
        self.red = (255, 0, 0)
        self.tomato = (255, 99, 71)
        self.coral = (255, 127, 80)
        self.indian_red = (205, 92, 92)
        self.light_coral = (240, 128, 128)
        self.dark_salmon = (233, 150, 122)
        self.salmon = (250, 128, 114)
        self.light_salmon = (255, 160, 122)
        self.orange_red = (255, 69, 0)
        self.dark_orange = (255, 140, 0)
        self.orange = (255, 165, 0)
        self.gold = (255, 215, 0)
        self.dark_golden_rod = (184, 134, 11)
        self.golden_rod = (218, 165, 32)
        self.pale_golden_rod = (238, 232, 170)
        self.dark_khaki = (189, 183, 107)
        self.khaki = (240, 230, 140)
        self.olive = (128, 128, 0)
        self.yellow = (255, 255, 0)
        self.yellow_green = (154, 205, 50)
        self.dark_olive_green = (85, 107, 47)
        self.olive_drab = (107, 142, 35)
        self.lawn_green = (124, 252, 0)
        self.chart_reuse = (127, 255, 0)
        self.green_yellow = (173, 255, 47)
        self.dark_green = (0, 100, 0)
        self.green = (0, 128, 0)
        self.forest_green = (34, 139, 34)
        self.lime = (0, 255, 0)
        self.lime_green = (50, 205, 50)
        self.light_green = (144, 238, 144)
        self.pale_green = (152, 251, 152)
        self.dark_sea_green = (143, 188, 143)
        self.medium_spring_green = (0, 250, 154)
        self.spring_green = (0, 255, 127)
        self.sea_green = (46, 139, 87)
        self.medium_aqua_marine = (102, 205, 170)
        self.medium_sea_green = (60, 179, 113)
        self.light_sea_green = (32, 178, 170)
        self.dark_slate_gray = (47, 79, 79)
        self.teal = (0, 128, 128)
        self.dark_cyan = (0, 139, 139)
        self.aqua = (0, 255, 255)
        self.cyan = (0, 255, 255)
        self.light_cyan = (224, 255, 255)
        self.dark_turquoise = (0, 206, 209)
        self.turquoise = (64, 224, 208)
        self.medium_turquoise = (72, 209, 204)
        self.pale_turquoise = (175, 238, 238)
        self.aqua_marine = (127, 255, 212)
        self.powder_blue = (176, 224, 230)
        self.cadet_blue = (95, 158, 160)
        self.steel_blue = (70, 130, 180)
        self.corn_flower_blue = (100, 149, 237)
        self.deep_sky_blue = (0, 191, 255)
        self.dodger_blue = (30, 144, 255)
        self.light_blue = (173, 216, 230)
        self.sky_blue = (135, 206, 235)
        self.light_sky_blue = (135, 206, 250)
        self.midnight_blue = (25, 25, 112)
        self.navy = (0, 0, 128)
        self.dark_blue = (0, 0, 139)
        self.medium_blue = (0, 0, 205)
        self.blue = (0, 0, 255)
        self.royal_blue = (65, 105, 225)
        self.blue_violet = (138, 43, 226)
        self.indigo = (75, 0, 130)
        self.dark_slate_blue = (72, 61, 139)
        self.slate_blue = (106, 90, 205)
        self.medium_slate_blue = (123, 104, 238)
        self.medium_purple = (147, 112, 219)
        self.dark_magenta = (139, 0, 139)
        self.dark_violet = (148, 0, 211)
        self.dark_orchid = (153, 50, 204)
        self.medium_orchid = (186, 85, 211)
        self.purple = (128, 0, 128)
        self.thistle = (216, 191, 216)
        self.plum = (221, 160, 221)
        self.violet = (238, 130, 238)
        self.magenta = (255, 0, 255)
        self.orchid = (218, 112, 214)
        self.medium_violet_red = (199, 21, 133)
        self.pale_violet_red = (219, 112, 147)
        self.deep_pink = (255, 20, 147)
        self.hot_pink = (255, 105, 180)
        self.light_pink = (255, 182, 193)
        self.pink = (255, 192, 203)
        self.antique_white = (250, 235, 215)
        self.beige = (245, 245, 220)
        self.bisque = (255, 228, 196)
        self.blanched_almond = (255, 235, 205)
        self.wheat = (245, 222, 179)
        self.corn_silk = (255, 248, 220)
        self.lemon_chiffon = (255, 250, 205)
        self.light_golden_rod_yellow = (250, 250, 210)
        self.light_yellow = (255, 255, 224)
        self.saddle_brown = (139, 69, 19)
        self.sienna = (160, 82, 45)
        self.chocolate = (210, 105, 30)
        self.peru = (205, 133, 63)
        self.sandy_brown = (244, 164, 96)
        self.burly_wood = (222, 184, 135)
        self.tan = (210, 180, 140)
        self.rosy_brown = (188, 143, 143)
        self.moccasin = (255, 228, 181)
        self.navajo_white = (255, 222, 173)
        self.peach_puff = (255, 218, 185)
        self.misty_rose = (255, 228, 225)
        self.lavender_blush = (255, 240, 245)
        self.linen = (250, 240, 230)
        self.old_lace = (253, 245, 230)
        self.papaya_whip = (255, 239, 213)
        self.sea_shell = (255, 245, 238)
        self.mint_cream = (245, 255, 250)
        self.slate_gray = (112, 128, 144)
        self.light_slate_gray = (119, 136, 153)
        self.light_steel_blue = (176, 196, 222)
        self.lavender = (230, 230, 250)
        self.floral_white = (255, 250, 240)
        self.alice_blue = (240, 248, 255)
        self.ghost_white = (248, 248, 255)
        self.honeydew = (240, 255, 240)
        self.ivory = (255, 255, 240)
        self.azure = (240, 255, 255)
        self.snow = (255, 250, 250)
        self.black = (0, 0, 0)
        self.dim_gray = (105, 105, 105)
        self.gray = (128, 128, 128)
        self.dark_gray = (169, 169, 169)
        self.silver = (192, 192, 192)
        self.light_gray = (211, 211, 211)
        self.gainsboro = (220, 220, 220)
        self.white_smoke = (245, 245, 245)
        self.white = (255, 255, 255)

        # 256 values from 'black' (0) to white (255)
        self.transition_black_white = [(i, i, i) for i in range(256)]


class Label:
    def __init__(self, surface: pygame.Surface, text, size: int, xy: tuple, anchor="center", **kwargs):
        """
        Creates a label.

        Instructions:
            - To create a label, create an instance of this class before
            the mainloop of the game.
            - To make the label appear, call the method 'self.draw()' in
            every loop of the game.

        Example (simplified):
            label = Label(screen, "Hello world!", 32, (100,100), "topleft")
            while True:
                label.draw()

        Arguments:
            surface
                the surface the object will be drawn onto
                Type: pygame.Surface, pygame.display.set_mode
            text
                the text displayed on the label / button
                Type: Any
            size
                refers to the size of text in pixels
                Type: int
            xy
                refers to the position of the anchor
                Type: tuple, list
            anchor
                the anchor of the object:   topleft,    midtop,    topright,
                                            midleft,    center,    midright,
                                            bottomleft, midbottom, bottomright
                Type: str
            textcolor
                color of the text in rgb
                Type: tuple, list
            backgroundcolor
                color of the background in rgb
                Type: None, tuple, list
            antialias
                whether antialias (blurring to make text seem more realistic) should be used
                Type: bool
            font
                the font used when displaying the text; to get all fonts available, use "pygame.font.get_fonts()"
                Type: str
            x_axis_addition
                adds the given amount of pixels to the left and right (-> x axis) of the text
                Type: int
            y_axis_addition
                adds the given amount of pixels to the top and bottom (-> y axis) of the text
                Type: int
            borderwidth
                width of the border
                Type: int
            bordercolor
                color of the border
                Type: tuple, list
            force_width
                forces the width of the background
                Type: int
            force_height
                forces the height of the background
                Type: int
            force_dim
                forces width and height of the background
                Type: tuple, list
            binding_rect
                whether the text_rect or the background_rect should be used with <xy> and <anchor>
                Type: [0, 1]
            borderradius
                used to round the corners of the background_rect; use int for all corners or other types for individual corners
                Type: int, tuple, list
            text_offset
                moves the text by the given values; is inverted if binding_rect == 1
                Type: tuple, list
            image
                takes an image as background for the widget; configures the widget to use the dimensions of the image, unless specified otherwise
                Type: pygame.Surface
            info
                can store any kind of data; usage of dict recommended
                Type: Any
            text_binding
                binds the text within the background_rect
                Type: str (same as <anchor>)
            highlight
                (button only)
                makes the button shine when the mouse hovers over it; when using "True", the button shines a little brighter than
                its usual backgroundcolor; otherwise, the button shines in the given rgb color; only works when using <backgroundcolor>
                Type: True, tuple, list
            active_area
                (button only)
                makes the self.update method only work if the mouse click / hovering is also within the specified rect; useful if
                buttons are moveable but should not be clickable if they are outside a certain area
                Type: tuple, list, pygame.Rect
            stay_within_surface # TODO
                makes the text unable to cross the border of the background_rect
                Type: bool
            bold
                makes the text appear bold (faked)
                Type: bool
            italic
                makes the text appear italic (faked)
                Type: bool
            underline
                underlines the text                
                Type: bool
            one_click_manager
                (button only)
                assures that overlaying buttons can not be clicked at the same time
                Type: Pygame_Engine.OneClickManager

        All custom arguments can also be used in their short form (eg. "aa" instead of "antialias").
        To see what all the short forms look like, inspect the self.ABBREVIATIONS attribute.
        """

        self.ABBREVIATIONS = {
            "textcolor": "tc",
            "backgroundcolor": "bgc",
            "antialias": "aa",
            "font": "f",
            "x_axis_addition": "xad",
            "y_axis_addition": "yad",
            "borderwidth": "bw",
            "bordercolor": "bc",
            "force_width": "fw",
            "force_height": "fh",
            "force_dim": "fd",
            "binding_rect": "bR",
            "borderradius": "br",
            "text_offset": "to",
            "image": "img",
            "info": "info",
            "text_binding": "tb",
            "highlight": "hl",
            "active_area": "aA",
            "stay_within_surface": "sws",
            "bold": "bo",
            "italic": "it",
            "underline": "ul",
            "one_click_manager": "ocm"
        }

        self.__is_touching__ = False # if cursor is touching the rect, only for buttons
        self.__has_hl_image__ = False

        self.surface = surface
        self.text = text
        assert type(size) in [int, float], f"invalid argument for 'size': {size}"
        self.size = int(size)
        assert type(xy) in [tuple, list], f"invalid argument for 'xy': {xy}"
        assert len(xy) == 2, f"invalid argument for 'xy': {xy}"
        self.xy = int(xy[0]), int(xy[1])
        assert anchor in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
            ","), f"invalid argument for 'anchor': {anchor}"
        self.anchor = anchor

        kw = kwargs

        # textcolor
        self.textcolor = kw.get("textcolor", None)
        if self.textcolor == None:
            self.textcolor = kw.get(self.ABBREVIATIONS["textcolor"], None)
        if self.textcolor == None:
            self.textcolor = (0,0,0) # old: (255, 255, 255)
        # assertion
        if self.textcolor != None:
            assert type(self.textcolor) in [
                tuple, list], f"invalid argument for 'textcolor': {self.textcolor}"
            assert len(self.textcolor) == 3, f"invalid argument for 'textcolor': {self.textcolor}"

        # backgroundcolor
        self.backgroundcolor = kw.get("backgroundcolor", None)
        if self.backgroundcolor == None:
            self.backgroundcolor = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion
        if self.backgroundcolor != None:
            assert type(self.backgroundcolor) in [
                tuple, list], f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"
            assert len(
                self.backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"

        # backgroundcolor backup
        self.backgroundcolor_init = self.backgroundcolor
        # assertion completed by previous assertion

        # antialias
        self.antialias = kw.get("antialias", None)
        if self.antialias == None:
            self.antialias = kw.get(self.ABBREVIATIONS["antialias"], None)
        if self.antialias == None:
            self.antialias = True
        # assertion
        assert type(self.antialias) == bool, f"invalid argument for 'antialias': {self.antialias}"

        # font
        self.font = kw.get("font", None)
        if self.font == None:
            self.font = kw.get(self.ABBREVIATIONS["font"], None)
        if self.font == None:
            self.font = ""
        # assertion
        if self.font != None:
            assert type(self.font) == str, f"invalid argument for 'font': {self.font}"

        # x_axis_addition
        self.x_axis_addition = kw.get("x_axis_addition", None)
        if self.x_axis_addition == None:
            self.x_axis_addition = kw.get(self.ABBREVIATIONS["x_axis_addition"], None)
        if self.x_axis_addition == None:
            self.x_axis_addition = 0
        # assertion
        if self.x_axis_addition != None:
            assert type(
                self.x_axis_addition) == int, f"invalid argument for 'x_axis_addition': {self.x_axis_addition}"
            assert self.x_axis_addition >= 0, f"invalid argument for 'x_axis_addition': {self.x_axis_addition}"

        # y_axis_addition
        self.y_axis_addition = kw.get("y_axis_addition", None)
        if self.y_axis_addition == None:
            self.y_axis_addition = kw.get(self.ABBREVIATIONS["y_axis_addition"], None)
        if self.y_axis_addition == None:
            self.y_axis_addition = 0
        # assertion
        if self.y_axis_addition != None:
            assert type(
                self.y_axis_addition) == int, f"invalid argument for 'y_axis_addition': {self.y_axis_addition}"
            assert self.y_axis_addition >= 0, f"invalid argument for 'y_axis_addition': {self.y_axis_addition}"

        # borderwidth
        self.borderwidth = kw.get("borderwidth", None)
        if self.borderwidth == None:
            self.borderwidth = kw.get(self.ABBREVIATIONS["borderwidth"], None)
        if self.borderwidth == None:
            self.borderwidth = 0
        # assertion
        if self.borderwidth != None:
            assert type(self.borderwidth) == int, f"invalid argument for 'borderwidth': {self.borderwidth}"
            assert self.borderwidth >= 0, f"invalid argument for 'borderwidth': {self.borderwidth}"

        # bordercolor
        self.bordercolor = kw.get("bordercolor", None)
        if self.bordercolor == None:
            self.bordercolor = kw.get(self.ABBREVIATIONS["bordercolor"], None)
        if self.bordercolor == None:
            self.bordercolor = (0, 0, 0)
        # assertion
        if self.bordercolor != None:
            assert type(self.bordercolor) in [
                tuple, list], f"invalid argument for 'bordercolor': {self.bordercolor}"
            assert len(self.bordercolor) == 3, f"invalid argument for 'bordercolor': {self.bordercolor}"

        # force_width
        self.force_width = kw.get("force_width", None)
        if self.force_width == None:
            self.force_width = kw.get(self.ABBREVIATIONS["force_width"], None)
        # assertion
        if self.force_width != None:
            assert type(self.force_width) == int, f"invalid argument for 'force_width': {self.force_width}"
            assert self.force_width > 0, f"invalid argument for 'force_width': {self.force_width}"

        # force_height
        self.force_height = kw.get("force_height", None)
        if self.force_height == None:
            self.force_height = kw.get(self.ABBREVIATIONS["force_height"], None)
        # assertion
        if self.force_height != None:
            assert type(self.force_height) == int, f"invalid argument for 'force_height': {self.force_height}"
            assert self.force_height > 0, f"invalid argument for 'force_height': {self.force_height}"

        # force_dim
        force_dim = kw.get("force_dim", None)
        if force_dim == None:
            force_dim = kw.get(self.ABBREVIATIONS["force_dim"], None)
        # assertion
        if force_dim != None:
            if type(force_dim) not in [tuple, list] or len(force_dim) != 2:
                raise ValueError(
                    f"invalid argument for 'force_dim': '{force_dim}'")
            if force_dim[0] != None:
                self.force_width = force_dim[0]
            if force_dim[1] != None:
                self.force_height = force_dim[1]

        # binding_rect
        self.binding_rect = kw.get("binding_rect", None)
        if self.binding_rect == None:
            self.binding_rect = kw.get(self.ABBREVIATIONS["binding_rect"], None)
        if self.binding_rect == None:
            self.binding_rect = 1 # old: 0
        # assertion
        assert self.binding_rect in [0, 1], f"invalid argument for 'binding_rect': {self.binding_rect}"

        # borderradius
        self.borderradius = kw.get("borderradius", None)
        if self.borderradius == None:
            self.borderradius = kw.get(self.ABBREVIATIONS["borderradius"], None)
        if self.borderradius == None:
            self.borderradius = (1, 1, 1, 1) # (0, 0, 0, 0)
        # assertion
        elif type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) in [tuple, list]:
            if len(self.borderradius) != 4:
                raise ValueError(
                    f"Invalid argument for 'borderradius': {self.borderradius}.")
        else:
            raise Exception(f"invalid argument for 'borderradius': {self.borderradius}")

        # text_offset
        self.text_offset = kw.get("text_offset", None)
        if self.text_offset == None:
            self.text_offset = kw.get(self.ABBREVIATIONS["text_offset"], None)
        if self.text_offset == None:
            self.text_offset = (0, 0)
        # assertion
        if self.text_offset != None:
            assert type(self.text_offset) in [
                tuple, list], f"invalid argument for 'text_offset': {self.text_offset}"
            assert len(self.text_offset) == 2, f"invalid argument for 'text_offset': {self.text_offset}"

        # image
        self.image = kw.get("image", None)
        if self.image == None:
            self.image = kw.get(self.ABBREVIATIONS["image"], None)
        # assertion
        if self.image != None:
            assert type(self.image) == pygame.Surface, f"invalid argument for 'image': {self.image}"
            if self.force_width == None:
                self.force_width = self.image.get_width()
            if self.force_height == None:
                self.force_height = self.image.get_height()
            self.image = pygame.transform.scale(self.image, (self.force_width, self.force_height))

        # info
        self.info = kw.get("info", None)
        if self.info == None:
            self.info = kw.get(self.ABBREVIATIONS["info"], None)
        # no assertion needed

        # text_binding
        self.text_binding = kw.get("text_binding", None)
        if self.text_binding == None:
            self.text_binding = kw.get(self.ABBREVIATIONS["text_binding"], None)
        if self.text_binding == None:
            self.text_binding = "center"
        # assertion
        if self.text_binding != None:
            assert self.text_binding in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
                ","), f"invalid argument for 'text_binding': {self.text_binding}"

        # highlight
        self.highlight = kw.get("highlight", None)
        if self.highlight == None:
            self.highlight = kw.get(self.ABBREVIATIONS["highlight"], None)
        # assertion
        if self.highlight != None:
            if type(self.highlight) in [tuple, list] and len(self.highlight) == 3:
                pass # ok
            elif self.highlight == False:
                self.highlight = None # ok
            elif self.highlight == True:
                if self.image == None:
                    assert self.backgroundcolor != None, f"'backgroundcolor' (currently: {self.backgroundcolor}) must be defined when using 'highlight' (currently: {self.highlight})"
            else:
                raise AssertionError(f"invalid argument for 'highlight': {self.highlight}")

            if self.image == None:
                if self.highlight == True:
                    self.highlight = (
                        min(self.backgroundcolor[0] + 50, 255),
                        min(self.backgroundcolor[1] + 50, 255),
                        min(self.backgroundcolor[2] + 50, 255)
                    )
            else:
                self.__has_hl_image__ = True
                # if the backgroundcolor is not defined, the regular image will be taken for the hl_image
                # if there is a backgroundcolor, the backgroundcolor will be included in the hl_image
                if self.backgroundcolor == None:
                    self.hl_image = self.image.copy()
                else:
                    self.hl_image = pygame.Surface(self.image.get_size())
                    self.hl_image.fill(self.backgroundcolor)
                    self.hl_image.blit(self.image, (0,0))
                # applying the brightening effect / coloring
                if self.highlight == True:
                    self.hl_image.fill((50,50,50), special_flags=pygame.BLEND_RGB_ADD)
                else:
                    self.hl_image.fill(self.highlight, special_flags=pygame.BLEND_RGB_MULT)
                # scaling to fit the size
                self.hl_image = pygame.transform.scale(self.hl_image, (self.force_width, self.force_height))

        # active_area
        self.active_area = kw.get("active_area", None)
        if self.active_area == None:
            self.active_area = kw.get(self.ABBREVIATIONS["active_area"], None)
        # assertion
        if self.active_area != None:
            if type(self.active_area) in [tuple, list]:
                assert len(self.active_area) == 4, f"invalid argument for 'active_area': {self.active_area}"
                self.active_area = pygame.Rect(*self.active_area)
            elif type(self.active_area) == pygame.Rect:
                pass
            else:
                raise Exception(f"invalid argument for 'active_area': {self.active_area}")

        # stay_within_surface # TODO
        self.stay_within_surface = kw.get("stay_within_surface", False)
        if self.stay_within_surface == False:
            self.stay_within_surface = kw.get(self.ABBREVIATIONS["stay_within_surface"], False)
        # assertion
        assert type(
            self.stay_within_surface) == bool, f"invalid argument for 'stay_within_surface': {self.stay_within_surface}"

        # bold
        self.bold = kw.get("bold", None)
        if self.bold == None:
            self.bold = kw.get(self.ABBREVIATIONS["bold"], None)
        if self.bold == None:
            self.bold = False
        # assertion
        assert type(self.bold) == bool, f"invalid argument for 'bold': {self.bold}"

        # italic
        self.italic = kw.get("italic", None)
        if self.italic == None:
            self.italic = kw.get(self.ABBREVIATIONS["italic"], None)
        if self.italic == None:
            self.italic = False
        # assertion
        assert type(self.italic) == bool, f"invalid argument for 'italic': {self.italic}"

        # underline
        self.underline = kw.get("underline", None)
        if self.underline == None:
            self.underline = kw.get(self.ABBREVIATIONS["underline"], None)
        if self.underline == None:
            self.underline = False
        # assertion
        assert type(self.underline) == bool, f"invalid argument for 'underline': {self.underline}"

        # one_click_manager
        self.one_click_manager = kwargs.get("one_click_manager", None)
        if self.one_click_manager == None:
            self.one_click_manager = kw.get(self.ABBREVIATIONS["one_click_manager"], None)
        # assertion
        if self.one_click_manager != None:
            assert type(self.one_click_manager) == OneClickManager, f"invalid argument for 'one_click_manager': {self.one_click_manager}"

        self.__create__()

    def __create__(self):

        font = pygame.font.Font(
            pygame.font.match_font(self.font), self.size)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        font.set_underline(self.underline)
        self.text_surface = font.render(
            str(self.text), self.antialias, self.textcolor)
        self.text_rect = self.text_surface.get_rect()

        # sx sy w h
        # x_axis: sx, w
        # y_axis: sy, h

        if self.x_axis_addition == 0:
            sx = self.text_rect.x
            w = self.text_rect.width
        elif self.x_axis_addition > 0:
            sx = self.text_rect.x - self.x_axis_addition
            w = self.text_rect.width + self.x_axis_addition * 2

        if self.y_axis_addition == 0:
            sy = self.text_rect.y
            h = self.text_rect.height
        elif self.y_axis_addition > 0:
            sy = self.text_rect.y - self.y_axis_addition
            h = self.text_rect.height + self.y_axis_addition * 2

        if self.force_width == None:
            pass
        elif self.force_width < 0:
            raise ValueError(
                f"Invalid argument for 'force_width': '{self.force_width}'.")
        else:
            w = self.force_width

        if self.force_height == None:
            pass
        elif self.force_height < 0:
            raise ValueError(
                f"Invalid argument for 'force_height': '{self.force_height}'.")
        else:
            h = self.force_height

        # creating the background rect
        self.background_rect = pygame.Rect(sx, sy, w, h)

        # putting everything in correct position
        self.update_pos(self.xy, self.anchor)
        
        if self.stay_within_surface:
            """
            idea: just draw the whole thing (text, background, border) onto an extra
            surface and then take only the background_rect from that surface
            """
            # a = pygame.Surface((min(self.background_rect.width, self.text_rect.width),
            #                    min(self.background_rect.height, self.text_rect.height))) # ?
            # a = pygame.Surface((self.text_rect.width, self.text_rect.height))
            # def next_col(col):
            #     if col[0] < 255:
            #         return [col[0]+1, col[1], col[2]]
            #     elif col[1] < 255:
            #         return [col[0], col[1]+1, col[2]]
            #     elif col[2] < 255:
            #         return [col[0], col[1], col[2]+1]
            #     else:
            #         raise Exception("should not be possible...")
            # col = [0,0,0]
            # while self.textcolor == tuple(col) or self.backgroundcolor == tuple(col) or self.bordercolor == tuple(col):
            #     col = next_col(col)
            # print(col)
            # a.fill(col)
            # a.set_colorkey(col)
            # r = (self.background_rect.left - self.text_rect.left, self.background_rect.top - self.text_rect.top, self.background_rect.width, self.background_rect.height)

            # subsurf = self.text_surface.subsurface(r)

            # pygame.draw.rect(a, (0,0,255), r, 1)
            # a.blit(subsurf, (0,0))
            # self.text_surface = a
            # self.text_rect = self.text_surface.get_rect() # ?

            # x / w #
            if self.text_rect.width > self.background_rect.width:
                x = self.background_rect.left - self.text_rect.left
                w = self.background_rect.width
            else:
                x = 0
                w = self.text_rect.width
            # y / h #
            if self.text_rect.height > self.background_rect.height:
                y = self.background_rect.top - self.text_rect.top
                h = self.background_rect.height
            else:
                y = 0
                h = self.text_rect.height

            print(x,y,w,h)
            pygame.image.save(self.text_surface, r"C:\Users\marce\AppData\Local\Programs\Python\Python39\Lib\site-packages\my_lib_folder\text_surface.png")
            a = self.text_surface.subsurface((x,y,w,h))
            self.text_surface = a
            self.text_rect = a.get_rect()
            pygame.image.save(a, r"C:\Users\marce\AppData\Local\Programs\Python\Python39\Lib\site-packages\my_lib_folder\text_surface_subsurf.png")

        # data # should actually be accessed through 'self.rect.' but I
        # will leave it as it is to not break any programs
        self.topleft = self.background_rect.topleft
        self.topright = self.background_rect.topright
        self.bottomleft = self.background_rect.bottomleft
        self.bottomright = self.background_rect.bottomright
        self.center = self.background_rect.center
        self.midtop = self.background_rect.midtop
        self.midright = self.background_rect.midright
        self.midbottom = self.background_rect.midbottom
        self.midleft = self.background_rect.midleft
        self.left = self.background_rect.left
        self.right = self.background_rect.right
        self.top = self.background_rect.top
        self.bottom = self.background_rect.bottom

        self.rect = self.background_rect

        # for buttons:
        self.x_range = (self.background_rect.x,
                        self.background_rect.x + self.background_rect.width)
        self.y_range = (self.background_rect.y,
                        self.background_rect.y + self.background_rect.height)

    def draw(self):
        """
        Draws the widget to the screen.
        """

        if self.backgroundcolor != None:
            if self.__is_touching__ and self.image == None:
                pygame.draw.rect(
                    self.surface, self.highlight, self.background_rect, 0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3])
            else:
                pygame.draw.rect(
                    self.surface, self.backgroundcolor, self.background_rect, 0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3])
        if self.image != None:
            if self.__has_hl_image__ and self.__is_touching__:
                self.surface.blit(self.hl_image, self.background_rect)
            else:
                self.surface.blit(self.image, self.background_rect)

        if self.borderwidth > 0:
            pygame.draw.rect(
                self.surface, self.bordercolor, self.background_rect, self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3])
        self.surface.blit(self.text_surface, self.text_rect)

    def draw_to(self, surface: pygame.Surface):
        """
        Draws the widget to a different surface than initially specified.
        """
        assert type(surface) == pygame.Surface, f"invalid argument for 'surface': {surface}"

        if self.backgroundcolor != None:
            if self.__is_touching__ and self.image == None:
                pygame.draw.rect(
                    surface, self.highlight, self.background_rect, 0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3])
            else:
                pygame.draw.rect(
                    surface, self.backgroundcolor, self.background_rect, 0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3])
        if self.image != None:
            if self.__has_hl_image__ and self.__is_touching__:
                surface.blit(self.hl_image, self.background_rect)
            else:
                surface.blit(self.image, self.background_rect)


        if self.borderwidth > 0:
            pygame.draw.rect(
                surface, self.bordercolor, self.background_rect, self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3])
        surface.blit(self.text_surface, self.text_rect)

    def update_text(self, text):
        """
        Updates the text of a widget. Call this
        method before drawing to the screen.
        """
        if str(text) != str(self.text):
            self.text = str(text)
            self.__create__()

    def update_colors(self, textcolor=None, backgroundcolor=None, bordercolor=None):
        """
        Updates the colors of a widget. Call this
        method before drawing to the screen.

        This method can be called every loop without worrying about performance problems.
        """
        if textcolor != None and textcolor != self.textcolor:
            assert type(textcolor) in [
                tuple, list], f"invalid argument for 'textcolor': {textcolor}"
            assert len(textcolor) == 3, f"invalid argument for 'textcolor': {textcolor}"
            self.textcolor = textcolor
            self.__create__()
        if backgroundcolor != None and backgroundcolor != self.backgroundcolor:
            assert type(backgroundcolor) in [
                tuple, list], f"invalid argument for 'backgroundcolor': {backgroundcolor}"
            assert len(
                backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {backgroundcolor}"
            self.backgroundcolor = backgroundcolor
            self.backgroundcolor_init = backgroundcolor
            val = 50
            self.highlight = (
                min(self.backgroundcolor[0] + val, 255),
                min(self.backgroundcolor[1] + val, 255),
                min(self.backgroundcolor[2] + val, 255)
            )
            self.__create__()
        if bordercolor != None and bordercolor != self.bordercolor:
            assert type(bordercolor) in [
                tuple, list], f"invalid argument for 'bordercolor': {bordercolor}"
            assert len(bordercolor) == 3, f"invalid argument for 'bordercolor': {bordercolor}"
            self.bordercolor = bordercolor

    def update_borderwidth(self, borderwidth: int):
        """
        Updates the borderwidth of the widget. Call
        this method before drawing to the screen.
        """
        assert type(borderwidth) == int, f"invalid argument for 'borderwidth': {borderwidth}"
        assert borderwidth >= 0, f"invalid argument for 'borderwidth': {borderwidth}"
        self.borderwidth = borderwidth

    def update_pos(self, xy, anchor=None):
        """
        Changes the widgets position. Call this
        method before drawing to the screen.
        """
        assert type(xy) in [tuple, int], f"invalid argument for 'xy': {xy}"
        assert len(xy) == 2, f"invalid argument for 'xy': {xy}"
        self.xy = xy
        assert anchor in ["topleft", "topright", "bottomleft", "bottomright",
                                   "center", "midtop", "midright", "midbottom", "midleft", None]
        if anchor is not None:
            self.anchor = anchor

        if self.binding_rect == 0:
            self.text_rect.__setattr__(self.anchor, self.xy)
            text_rect_coords = getattr(self.text_rect, self.text_binding)
            self.background_rect.__setattr__(
                self.text_binding,
                (text_rect_coords[0] + self.text_offset[0],
                 text_rect_coords[1] + self.text_offset[1]))

        elif self.binding_rect == 1:
            self.background_rect.__setattr__(self.anchor, self.xy)
            background_rect_coords = getattr(self.background_rect, self.text_binding)
            self.text_rect.__setattr__(
                self.text_binding,
                (background_rect_coords[0] + self.text_offset[0],
                 background_rect_coords[1] + self.text_offset[1]))
    
    def set_style(self, bold: bool = None, italic: bool = None):
        old_bold = self.bold
        if bold != None:
            self.bold = bool(bold)
        old_italic = self.italic
        if italic != None:
            self.italic = bool(italic)
        if old_bold != self.bold or old_italic != self.italic:
            self.__create__()

    def get_rect(self):
        return self.rect


class Button(Label):
    def __init__(self, surface, text, size, xy: tuple, anchor="center", **kwargs):
        """
        Creates a clickable button.

        Instructions:
            - To create a button, create an instance of this class before
            the mainloop of the game.
            - To make the button appear, call the method 'self.draw()' in
            every loop of the game.
            - To check if the button has been clicked, call the method
            'self.update()' with a list of mouse events in an if-statement.

        Example (simplified):
            button = Button(screen, "Hello world!", 32, (100,100), "topleft")
            while True:
                events = pygame.event.get()
                if button.update(events):
                    ...
                button.draw()

        For information about arguments see parent class (Label).
        """

        super().__init__(surface, text, size, xy, anchor, **kwargs)

    def update(self, event_list, button: int = 1, offset: tuple = (0, 0)) -> bool:
        """
        Checks if button has been pressed and returns True if so.
        <button> can specify a certain button (1-3).
        <offset> will be subtracted from the current mouse position.
        """
        assert type(button) == int, f"invalid argument for 'button': {button}"
        assert 1 <= button <= 5, f"invalid argument for 'button': {button}"
        assert type(offset) in [tuple, list], f"invalid argument for 'offset': {offset}"
        assert len(offset) == 2, f"invalid argument for 'offset: {offset}"

        # stops if one_click_manager tells that a click has taken place elsewhere
        if self.one_click_manager != None and self.one_click_manager.get_clicked() == True:
            self.__is_touching__ = False
            return False

        # managing the actual clicks
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = list(event.pos)
                if self.active_area != None and not self.active_area.collidepoint(pos):
                    continue
                pos[0] -= offset[0]
                pos[1] -= offset[1]
                if button == None:
                    if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                        if self.one_click_manager != None:
                            self.one_click_manager.set_clicked()
                        return True

                elif 0 < button < 4:
                    if button == event.button:
                        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                            if self.one_click_manager != None:
                                self.one_click_manager.set_clicked()
                            return True

                else:
                    raise ValueError(f"invalid argument for 'button': {button}")

        if self.one_click_manager != None and self.one_click_manager.get_hovering() == True:
            self.__is_touching__ = False
            return False

        # managing the hovering (highlight)
        pos = list(pygame.mouse.get_pos())
        if self.active_area != None and not self.active_area.collidepoint(pos):
            self.__is_touching__ = False
            return False
        pos[0] -= offset[0]
        pos[1] -= offset[1]
        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
            if self.highlight != None:
                self.__is_touching__ = True
            if self.one_click_manager != None:
                self.one_click_manager.set_hovering()
        else:
            self.__is_touching__ = False

        return False


class Paragraph:
    def __init__(self, surface, text, size, xy: tuple, anchor="center", **kwargs):
        """
        Creates a multiline label (using '\\n').

        Instructions:
            - To create a label, create an instance of this class before
            the mainloop of the game.
            - To make the label appear, call the method 'self.draw()' in
            every loop of the game.

        Example (simplified):
            label = Label(screen, "Hello world!", 32, (100,100), "topleft")
            while True:
                label.draw()

        Arguments:
            surface
                the surface the object will be drawn onto
                Type: pygame.Surface, pygame.display.set_mode
            text
                the text displayed on the label / button
                Type: Any
            size
                refers to the size of text in pixels
                Type: int
            xy
                refers to the position of the anchor
                Type: tuple, list
            anchor
                the anchor of the object:   topleft,    midtop,    topright,
                                            midleft,    center,    midright,
                                            bottomleft, midbottom, bottomright
                Type: str
            textcolor
                color of the text in rgb
                Type: tuple, list
            backgroundcolor
                color of the background in rgb
                Type: None, tuple, list
            antialias
                whether antialias (blurring to make text seem more realistic) should be used
                Type: bool
            font
                the font used when displaying the text; to get all fonts available, use "pygame.font.get_fonts()"
                Type: str
            x_axis_addition
                adds the given amount of pixels to the left and right (-> x axis) of the text
                Type: int
            y_axis_addition
                adds the given amount of pixels to the top and bottom (-> y axis) of the text
                Type: int
            borderwidth
                width of the border
                Type: int
            bordercolor
                color of the border
                Type: tuple, list
            force_width
                forces the width of the background
                Type: int
            force_height
                forces the height of the background
                Type: int
            force_dim
                forces width and height of the background
                Type: tuple, list
            binding_rect
                whether the text_rect or the background_rect should be used with <xy> and <anchor>
                Type: [0, 1]
            borderradius
                used to round the corners of the background_rect; use int for all corners or other types for individual corners
                Type: int, tuple, list
            text_offset
                moves the text by the given values; is inverted if binding_rect == 1
                Type: tuple, list
            image
                blits an image onto the label / button; only works when using <force_dim>
                Type: pygame.Image
            info
                can store any kind of data; usage of dict recommended
                Type: Any
            text_binding
                binds the text within the background_rect
                Type: str (same as <anchor>)
            highlight
                (button only)
                makes the button shine when the mouse hovers over it; when using "True", the button shines a little brighter than
                its usual backgroundcolor; otherwise, the button shines in the given rgb color; only works when using <backgroundcolor>
                Type: True, tuple, list
            active_area
                (button only)
                makes the self.update method only work if the mouse click / hovering is also within the specified rect; useful if
                buttons are moveable but should not be clickable if they are outside a certain area
                Type: tuple, list, pygame.Rect
            stay_within_surface # TODO
                makes the text unable to cross the border of the background_rect
                Type: bool

        All custom arguments can also be used in their short form (eg. "aa" instead of "antialias").
        To see what all the short forms look like, inspect the self.ABBREVIATIONS attribute.
        """

        self.ABBREVIATIONS = {
            "textcolor": "tc",
            "backgroundcolor": "bgc",
            "antialias": "aa",
            "font": "f",
            "x_axis_addition": "xad",
            "y_axis_addition": "yad",
            "borderwidth": "bw",
            "bordercolor": "bc",
            "force_width": "fw",
            "force_height": "fh",
            "force_dim": "fd",
            "binding_rect": "bR",
            "borderradius": "br",
            "text_offset": "to",
            "image": "img",
            "info": "info",
            "text_binding": "tb",
            "highlight": "hl",
            "active_area": "aA",
            "stay_within_surface": "sws"
        }

        self.surface = surface
        self.text = text
        assert type(size) in [int, float], f"invalid argument for 'size': {size}"
        self.size = int(size)
        assert type(xy) in [tuple, list], f"invalid argument for 'xy': {xy}"
        assert len(xy) == 2, f"invalid argument for 'xy': {xy}"
        self.xy = xy
        assert anchor in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
            ","), f"invalid argument for 'anchor': {anchor}"
        self.anchor = anchor

        kw = kwargs

        # textcolor
        self.textcolor = kw.get("textcolor", None)
        if self.textcolor == None:
            self.textcolor = kw.get(self.ABBREVIATIONS["textcolor"], None)
        if self.textcolor == None:
            self.textcolor = (255, 255, 255)
        # assertion
        if self.textcolor != None:
            assert type(self.textcolor) in [
                tuple, list], f"invalid argument for 'textcolor': {self.textcolor}"
            assert len(self.textcolor) == 3, f"invalid argument for 'textcolor': {self.textcolor}"

        # backgroundcolor
        self.backgroundcolor = kw.get("backgroundcolor", None)
        if self.backgroundcolor == None:
            self.backgroundcolor = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion
        if self.backgroundcolor != None:
            assert type(self.backgroundcolor) in [
                tuple, list], f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"
            assert len(
                self.backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"

        # backgroundcolor backup
        self.backgroundcolor_init = kw.get("backgroundcolor", None)
        if self.backgroundcolor_init == None:
            self.backgroundcolor_init = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion completed by previous assertion

        # antialias
        self.antialias = kw.get("antialias", None)
        if self.antialias == None:
            self.antialias = kw.get(self.ABBREVIATIONS["antialias"], None)
        if self.antialias == None:
            self.antialias = True
        # assertion
        assert type(self.antialias) == bool, f"invalid argument for 'antialias': {self.antialias}"

        # font
        self.font = kw.get("font", None)
        if self.font == None:
            self.font = kw.get(self.ABBREVIATIONS["font"], None)
        if self.font == None:
            self.font = ""
        # assertion
        if self.font != None:
            assert type(self.font) == str, f"invalid argument for 'font': {self.font}"

        # x_axis_addition
        self.x_axis_addition = kw.get("x_axis_addition", None)
        if self.x_axis_addition == None:
            self.x_axis_addition = kw.get(self.ABBREVIATIONS["x_axis_addition"], None)
        if self.x_axis_addition == None:
            self.x_axis_addition = 0
        # assertion
        if self.x_axis_addition != None:
            assert type(
                self.x_axis_addition) == int, f"invalid argument for 'x_axis_addition': {self.x_axis_addition}"
            assert self.x_axis_addition >= 0, f"invalid argument for 'x_axis_addition': {self.x_axis_addition}"

        # y_axis_addition
        self.y_axis_addition = kw.get("y_axis_addition", None)
        if self.y_axis_addition == None:
            self.y_axis_addition = kw.get(self.ABBREVIATIONS["y_axis_addition"], None)
        if self.y_axis_addition == None:
            self.y_axis_addition = 0
        # assertion
        if self.y_axis_addition != None:
            assert type(
                self.y_axis_addition) == int, f"invalid argument for 'y_axis_addition': {self.y_axis_addition}"
            assert self.y_axis_addition >= 0, f"invalid argument for 'y_axis_addition': {self.y_axis_addition}"

        # borderwidth
        self.borderwidth = kw.get("borderwidth", None)
        if self.borderwidth == None:
            self.borderwidth = kw.get(self.ABBREVIATIONS["borderwidth"], None)
        if self.borderwidth == None:
            self.borderwidth = 0
        # assertion
        if self.borderwidth != None:
            assert type(self.borderwidth) == int, f"invalid argument for 'borderwidth': {self.borderwidth}"
            assert self.borderwidth >= 0, f"invalid argument for 'borderwidth': {self.borderwidth}"

        # bordercolor
        self.bordercolor = kw.get("bordercolor", None)
        if self.bordercolor == None:
            self.bordercolor = kw.get(self.ABBREVIATIONS["bordercolor"], None)
        if self.bordercolor == None:
            self.bordercolor = (0, 0, 0)
        # assertion
        if self.bordercolor != None:
            assert type(self.bordercolor) in [
                tuple, list], f"invalid argument for 'bordercolor': {self.bordercolor}"
            assert len(self.bordercolor) == 3, f"invalid argument for 'bordercolor': {self.bordercolor}"

        # force_width
        self.force_width = kw.get("force_width", None)
        if self.force_width == None:
            self.force_width = kw.get(self.ABBREVIATIONS["force_width"], None)
        # assertion
        if self.force_width != None:
            assert type(self.force_width) == int, f"invalid argument for 'force_width': {self.force_width}"
            assert self.force_width > 0, f"invalid argument for 'force_width': {self.force_width}"

        # force_height
        self.force_height = kw.get("force_height", None)
        if self.force_height == None:
            self.force_height = kw.get(self.ABBREVIATIONS["force_height"], None)
        # assertion
        if self.force_height != None:
            assert type(self.force_height) == int, f"invalid argument for 'force_height': {self.force_height}"
            assert self.force_height > 0, f"invalid argument for 'force_height': {self.force_height}"

        # force_dim
        force_dim = kw.get("force_dim", None)
        if force_dim == None:
            force_dim = kw.get(self.ABBREVIATIONS["force_dim"], None)
        # assertion
        if force_dim != None:
            if type(force_dim) not in [tuple, list] or len(force_dim) != 2:
                raise ValueError(
                    f"Invalid argument for 'force_dim': '{force_dim}'.")
            if force_dim[0] != None:
                self.force_width = force_dim[0]
            if force_dim[1] != None:
                self.force_height = force_dim[1]

        # binding_rect
        self.binding_rect = kw.get("binding_rect", None)
        if self.binding_rect == None:
            self.binding_rect = kw.get(self.ABBREVIATIONS["binding_rect"], None)
        if self.binding_rect == None:
            self.binding_rect = 0
        # assertion
        assert self.binding_rect in [0, 1], f"invalid argument for 'binding_rect': {self.binding_rect}"

        # borderradius
        self.borderradius = kw.get("borderradius", None)
        if self.borderradius == None:
            self.borderradius = kw.get(self.ABBREVIATIONS["borderradius"], None)
        if self.borderradius == None:
            self.borderradius = (0, 0, 0, 0)
        # assertion
        elif type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) in [tuple, list]:
            if len(self.borderradius) != 4:
                raise ValueError(
                    f"Invalid argument for 'borderradius': {self.borderradius}.")
        else:
            raise Exception(f"invalid argument for 'borderradius': {self.borderradius}")

        # text_offset
        self.text_offset = kw.get("text_offset", None)
        if self.text_offset == None:
            self.text_offset = kw.get(self.ABBREVIATIONS["text_offset"], None)
        if self.text_offset == None:
            self.text_offset = (0, 0)
        # assertion
        if self.text_offset != None:
            assert type(self.text_offset) in [
                tuple, list], f"invalid argument for 'text_offset': {self.text_offset}"
            assert len(self.text_offset) == 2, f"invalid argument for 'text_offset': {self.text_offset}"

        # image
        self.image = kw.get("image", None)
        if self.image == None:
            self.image = kw.get(self.ABBREVIATIONS["image"], None)
        # # assertion # ! somethings not working here # TODO
        # if self.image != None:
        #     if self.force_width == None or self.force_height == None:
        #         raise ValueError(
        #             "If an image is used, forced dimensions are needed!")
        #     try:
        #         img = pygame.transform.scale(pygame.image.load(self.image), (self.force_width, self.force_height))
        #         self.image = img
        #     except FileNotFoundError:
        #         raise Exception(f"Could not find file '{self.image}'")

        # info
        self.info = kw.get("info", None)
        if self.info == None:
            self.info = kw.get(self.ABBREVIATIONS["info"], None)
        # no assertion needed

        # text_binding
        self.text_binding = kw.get("text_binding", None)
        if self.text_binding == None:
            self.text_binding = kw.get(self.ABBREVIATIONS["text_binding"], None)
        if self.text_binding == None:
            self.text_binding = "center"
        # assertion
        if self.text_binding != None:
            assert self.text_binding in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
                ","), f"invalid argument for 'text_binding': {self.text_binding}"

        # highlight
        self.highlight = kw.get("highlight", None)
        if self.highlight == None:
            self.highlight = kw.get(self.ABBREVIATIONS["highlight"], None)
        # assertion
        if self.highlight != None:
            assert type(self.backgroundcolor) in [
                tuple, list], f"'backgroundcolor' (currently: {self.backgroundcolor}) must be defined when using 'highlight' (currently: {self.highlight})"
            if self.highlight == True:
                val = 50
                self.highlight = (
                    min(self.backgroundcolor[0] + val, 255),
                    min(self.backgroundcolor[1] + val, 255),
                    min(self.backgroundcolor[2] + val, 255)
                )
            else:
                assert type(self.highlight) in [
                    tuple, list], f"unknown format for 'highlight': (type: {type(self.highlight)}, value: {self.highlight})"

        # active_area
        self.active_area = kw.get("active_area", None)
        if self.active_area == None:
            self.active_area = kw.get(self.ABBREVIATIONS["active_area"], None)
        # assertion
        if self.active_area != None:
            if type(self.active_area) in [tuple, list]:
                assert len(self.active_area) == 4, f"invalid argument for 'active_area': {self.active_area}"
                self.active_area = pygame.Rect(*self.active_area)
            elif type(self.active_area) == pygame.Rect:
                pass
            else:
                raise Exception(f"invalid argument for 'active_area': {self.active_area}")

        # stay_within_surface
        self.stay_within_surface = kw.get("stay_within_surface", False)
        if self.stay_within_surface == False:
            self.stay_within_surface = kw.get(self.ABBREVIATIONS["stay_within_surface"], False)
        # assertion
        assert type(
            self.stay_within_surface) == bool, f"invalid argument for 'stay_within_surface': {self.stay_within_surface}"

        self.kwargs = kwargs
        self.__create__()

    def __create__(self):
        self.__labels__: list[Label] = []
        strings = self.text.split("\n")
        width = 0
        height = 0
        for string in strings:
            l = Label(
                self.surface, string, self.size, self.xy, **self.kwargs
            )
            width = max(width, l.rect.width)
            height = max(height, l.rect.height)

        # removing some arguments by setting them to default
        # bR, fd
        parsed_kwargs = self.kwargs.copy()
        parsed_kwargs["bR"] = 1
        parsed_kwargs["fd"] = (width, height)
        self.__borderwidth__ = self.borderwidth
        parsed_kwargs["bw"] = 0
        self.__borderradius__ = self.borderradius
        parsed_kwargs["br"] = (0, 0, 0, 0)
        self.__bordercolor__ = self.bordercolor
        # kwargs["bc"] = (0, 0, 0) # not needed

        for count, string in enumerate(strings):
            self.__labels__.append(
                Label(
                    self.surface, string, self.size,
                    (self.xy[0],
                     self.xy[1] + height * count),
                    self.anchor, **parsed_kwargs))

        fl = self.__labels__[0]     # first label
        ll = self.__labels__[-1]    # last label
        self.rect = pygame.Rect(fl.rect.left, fl.rect.top, ll.rect.right-fl.rect.left,
                                ll.rect.bottom-fl.rect.top)

    def draw(self):
        for label in self.__labels__:
            label.draw()
        if self.__borderwidth__ > 0:
            pygame.draw.rect(self.surface, self.__bordercolor__, self.rect,
                             self.__borderwidth__, *self.__borderradius__)

    def update_text(self, text: str):
        if str(text) != str(self.text):
            self.text = str(text)
            self.__create__()

    def update_colors(self, textcolor=None, backgroundcolor=None, bordercolor=None):
        if textcolor != None:
            assert type(textcolor) in [
                tuple, list], f"invalid argument for 'textcolor': {textcolor}"
            assert len(textcolor) == 3, f"invalid argument for 'textcolor': {textcolor}"
            self.textcolor = textcolor
            self.__create__()
        if backgroundcolor != None:
            assert type(backgroundcolor) in [
                tuple, list], f"invalid argument for 'backgroundcolor': {backgroundcolor}"
            assert len(
                backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {backgroundcolor}"
            self.backgroundcolor = backgroundcolor
            self.backgroundcolor_init = backgroundcolor
            val = 50
            self.highlight = (
                min(self.backgroundcolor[0] + val, 255),
                min(self.backgroundcolor[1] + val, 255),
                min(self.backgroundcolor[2] + val, 255)
            )
            self.__create__()
        if bordercolor != None:
            assert type(bordercolor) in [
                tuple, list], f"invalid argument for 'bordercolor': {bordercolor}"
            assert len(bordercolor) == 3, f"invalid argument for 'bordercolor': {bordercolor}"
            self.bordercolor = bordercolor


class ImageFrame:
    def __init__(
            self, surface, width_height: tuple, xy: tuple, anchor="center", auto_scale=True, borderwidth=0,
            bordercolor=(0, 0, 0),
            borderradius=0):
        self.surface = surface
        self.width = width_height[0]
        self.height = width_height[1]
        self.xy = xy
        self.anchor = anchor
        self.auto_scale = auto_scale
        self.borderwidth = borderwidth
        self.bordercolor = bordercolor
        self.image = None
        self.borderradius = borderradius
        if type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) == tuple:
            if len(self.borderradius) != 4:
                raise ValueError(
                    f"Invalid argument for 'borderradius': {self.borderradius}.")

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # putting in correct position
        if anchor == "topleft":
            self.rect.topleft = xy
        elif anchor == "topright":
            self.rect.topright = xy
        elif anchor == "bottomleft":
            self.rect.bottomleft = xy
        elif anchor == "bottomright":
            self.rect.bottomright = xy
        elif anchor == "center":
            self.rect.center = xy
        elif anchor == "midtop":
            self.rect.midtop = xy
        elif anchor == "midright":
            self.rect.midright = xy
        elif anchor == "midbottom":
            self.rect.midbottom = xy
        elif anchor == "midleft":
            self.rect.midleft = xy

    def insert_image(self, image):
        """
        Puts a pygame image into the frame.
        """
        if self.auto_scale == True:
            self.image = pygame.transform.scale(
                image, (self.width, self.height))
        else:
            self.image = image
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.rect.center

    def draw(self):
        """
        Draws object to the screen.
        """
        if self.auto_scale == False:
            self.surface.blit(self.image, self.image_rect)
        else:
            self.surface.blit(self.image, self.rect)
        if self.borderwidth > 0:
            pygame.draw.rect(
                self.surface, self.bordercolor, self.rect, self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3])


class PlayStation_Controller_Buttons:
    def __init__(self):
        """
        Makes it easier to map PlayStation-Controller buttons to functions.
        """
        self.cross = 0
        self.circle = 1
        self.square = 2
        self.triangle = 3
        self.share_button = 4
        self.ps_button = 5
        self.options_button = 6
        self.left_stick_in = 7
        self.right_stick_in = 8
        self.l1 = 9
        self.r1 = 10
        self.arrow_up = 11
        self.arrow_down = 12
        self.arrow_left = 13
        self.arrow_right = 14
        self.touch_pad_click = 15


class PlayStation_Controller:
    def __init__(self, joystick_num, threshold: float = 0.05):
        """
        Makes handling of keypresses on a controller easier.
        """
        self.joystick_num = joystick_num
        assert threshold >= 0, f"threshold must be at least 0 (currently {threshold})"
        assert threshold < 1, f"threshold must be less than 1 (currently {threshold})"
        self.threshold = threshold
        pygame.init()
        self.js = pygame.joystick.Joystick(joystick_num)
        self.js.init()
        self.pressed = {}

    def get_pressed(self):
        """
        Returns a dict of all keys pressed on the controller.
        Usage:
            keys = self.get_pressed()
            if keys[<key_num>]:
                action()
        """
        self.pressed = {}
        for button_num in range(self.js.get_numbuttons()):
            self.pressed[button_num] = self.js.get_button(button_num)
        return self.pressed

    def get_left_stick(self, custom_threshold=None) -> tuple[float, float]:
        """ returns a tuple representing the position of the left joystick """
        # pygame.event.pump()
        if custom_threshold == None:
            threshold = self.threshold
        elif type(custom_threshold) in [int, float]:
            assert custom_threshold >= 0
            threshold = custom_threshold
        else:
            raise TypeError(
                f"<custom_threshold> must be either None or an Integer or a float (not '{custom_threshold}')")

        vect = pygame.Vector2((self.js.get_axis(0), self.js.get_axis(1)))
        if vect.length() < threshold:
            return (0, 0)
        else:
            return vect

    def get_left_stick_angle(self, always_positive=True, decimals=1, default_return_value=0,
                             custom_threshold=None) -> int:
        """ returns the current angle of the left joystick; 0 == down """
        assert type(always_positive) == bool
        assert type(decimals) == int

        js = self.get_right_stick(custom_threshold)
        if js == (0, 0):
            return default_return_value
        deg = round_half_up(math.degrees(math.atan2(js[0], js[1])), decimals)

        if always_positive:
            return abs(deg)
        return deg

    def get_right_stick(self, custom_threshold=None) -> tuple[float, float]:
        """ returns a tuple representing the position of the right joystick """
        if custom_threshold == None:
            threshold = self.threshold
        elif type(custom_threshold) in [int, float]:
            assert custom_threshold >= 0
            threshold = custom_threshold
        else:
            raise TypeError(
                f"<custom_threshold> must be either None or an Integer or a float (not '{custom_threshold}')")

        vect = pygame.Vector2((self.js.get_axis(2), self.js.get_axis(3)))
        if vect.length() < threshold:
            return (0, 0)
        else:
            return vect

    def get_right_stick_angle(
            self, always_positive=True, decimals=1, default_return_value=0, custom_threshold=None) -> int:
        """ returns the current angle of the right joystick; 0 == down """
        assert type(always_positive) == bool
        assert type(decimals) == int

        js = self.get_right_stick(custom_threshold)
        if js == (0, 0):
            return default_return_value
        deg = round_half_up(math.degrees(math.atan2(js[0], js[1])), decimals)

        if always_positive:
            return abs(deg)
        return deg

    def get_l2(self, decimals=1) -> float:
        """ returns a float (-1 <= x <= 1) representing how much the paddle is pressed """
        return round_half_up(self.js.get_axis(4), decimals)

    def get_r2(self, decimals=1) -> float:
        """ returns a float (-1 <= x <= 1) representing how much the paddle is pressed """
        return round_half_up(self.js.get_axis(5), decimals)


class Switcheroo:
    def __init__(self, surface, switcheroo_elements, previous_next_keys, lower_higher_keys,
                 scrolling_cooldown, starting_index=0, bordercolor=(255, 255, 255),
                 borderwidth=1, borderradius=0):
        """
        game = pygame game object 
        """
        self.surface = surface
        self.switcheroo_elements = switcheroo_elements
        self.previous_key, self.next_key = previous_next_keys[0], previous_next_keys[1]
        self.lower_key, self.higher_key = lower_higher_keys[0], lower_higher_keys[1]
        self.scrolling_cooldown = scrolling_cooldown
        self.scrolling_cooldown_frames = 0
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.borderradius = borderradius

        self.current_index = starting_index  # the element thats currently being edited

        if starting_index not in range(len(switcheroo_elements)):
            raise ValueError(
                f"Invalid argument for 'starting index': '{starting_index}'. Index out of range.")

    def draw_box(self):
        """
        Outlines the current field.
        """
        active_element = self.switcheroo_elements[self.current_index]
        label = active_element.label_object
        pygame.draw.rect(
            self.surface, self.bordercolor,
            (label.rect.x, label.rect.y, label.rect.width, label.rect.height),
            self.borderwidth, self.borderradius)

    def update(self, keys_pressed):
        """
        Updates all values and returns them.

        Usage:
        value_1, value_2, ... = self.update(keys_pressed)
        """
        # decreases the cooldown for all elements
        for element in self.switcheroo_elements:
            if element.cooldown_frames > 0:
                element.cooldown_frames -= 1
        if self.scrolling_cooldown_frames > 0:
            self.scrolling_cooldown_frames -= 1
        # END OF BLOCK #

        # handles global scrolling first #
        keys = keys_pressed
        if not (keys[self.previous_key] and keys[self.next_key]):
            if keys[self.previous_key] and self.current_index > 0 and self.scrolling_cooldown_frames == 0:
                self.current_index -= 1
                self.scrolling_cooldown_frames = self.scrolling_cooldown
            if keys[self.next_key] and self.current_index < len(self.switcheroo_elements)-1 and self.scrolling_cooldown_frames == 0:
                self.current_index += 1
                self.scrolling_cooldown_frames = self.scrolling_cooldown
        # END OF BLOCK #

        # handles individual scrolling second #
        active_element = self.switcheroo_elements[self.current_index]
        if not (keys[self.lower_key] and keys[self.higher_key]):
            if keys[self.lower_key] and active_element.cooldown_frames == 0:
                active_element.decrease()
            if keys[self.higher_key] and active_element.cooldown_frames == 0:
                active_element.increase()
        # END OF BLOCK #

        # in the end, update all text fields and return the values
        values_list = []
        for element in self.switcheroo_elements:
            shown_value = element.var_range[element.index]
            true_value = ...

            # dict like {"Allowed":True,"Forbidden":False} ... basically {"shown_value":true_value}
            has_custom_value = False
            if element.custom_dict != None:
                if shown_value in element.custom_dict.keys():
                    true_value = element.custom_dict[shown_value]
                    has_custom_value = True

            element.label_object.update_text(shown_value)
            if has_custom_value == True:
                values_list.append(true_value)
            else:
                values_list.append(shown_value)
        # END OF BLOCK #

        return values_list


class Switcheroo_Element:
    def __init__(self, label_object, variable, var_range, starting_variable, cooldown, custom_dict=None):
        self.label_object = label_object
        self.variable = variable
        self.var_range = var_range
        self.cooldown = cooldown
        self.cooldown_frames = 0
        self.index = ...
        self.custom_dict = custom_dict

        # searching for the index of the starting variable
        # if type(starting_variable) != str:
        #     raise ValueError(f"Starting variable must be 'str'.")
        found = False
        for num, var in enumerate(var_range):
            if str(var) == str(starting_variable):
                self.index = num
                found = True
                break
        if found == False:
            raise ValueError(
                f"The starting variable '{starting_variable}' could not be found in the variables range.")

    def increase(self):
        """
        Increases self.index by 1 if its within the defined range.
        """
        if self.index + 1 < len(self.var_range):
            self.index += 1
            self.cooldown_frames = self.cooldown

    def decrease(self):
        """
        Decreases self.index by 1 if its within the defined range.
        """
        if self.index - 1 >= 0:
            self.index -= 1
            self.cooldown_frames = self.cooldown


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


class Table:
    def __init__(
            self, surface, xy: tuple, columns_rows: tuple, x_distance_y_distance: tuple,
            circle_color=(0, 0, 255),
            circle_radius=10):
        """
        xy centers the table at the given position.
        """

        self.surface = surface
        self.columns, self.rows = columns_rows[0], columns_rows[1]
        self.x_distance, self.y_distance = x_distance_y_distance[0], x_distance_y_distance[1]
        self.circle_color = circle_color
        self.circle_radius = circle_radius

        x = xy[0]-((self.columns-1)/2)*self.x_distance
        y = xy[1]-((self.rows-1)/2)*self.y_distance
        self.xy = (x, y)

        if self.rows < 1:
            raise ValueError(
                f"Invalid argument for 'rows': '{self.rows}'.")
        if self.columns < 1:
            raise ValueError(
                f"Invalid argument for 'columns': '{self.columns}'.")
        if self.x_distance < 1:
            raise ValueError(
                f"Invalid argument for 'x_distance': '{self.x_distance}'.")
        if self.y_distance < 1:
            raise ValueError(
                f"Invalid argument for 'y_distance': '{self.y_distance}'.")

        # target: dict["row"]["column"] ("self.tdict")
        self.dict = {}
        for x in range(self.columns):
            temp_d = {}
            for y in range(self.rows):
                temp_d[y] = (self.xy[0]+x*self.x_distance,
                             self.xy[1]+y*self.y_distance)
            self.dict[x] = temp_d

    def draw_dots(self):
        for x in range(self.columns):
            for y in range(self.rows):
                pygame.draw.circle(
                    self.surface, self.circle_color, self.dict[x][y], self.circle_radius)


class CustomTemplate:
    def __init__(self, surface, text="", size=12, anchor="center", textcolor=(255, 255, 255),
                 backgroundcolor=None, antialias=True, font="", x_axis_addition=0, y_axis_addition=0,
                 borderwidth=0, bordercolor=(0, 0, 0),
                 force_width=None, force_height=None, force_dim: tuple = None, binding_rect=0, borderradius=0):
        self.surface = surface
        self.text = text
        self.size = size
        self.anchor = anchor
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.antialias = antialias
        self.font = font
        self.x_axis_addition = x_axis_addition
        self.y_axis_addition = y_axis_addition
        self.borderwidth = borderwidth
        self.bordercolor = bordercolor
        self.force_width = force_width
        self.force_height = force_height
        self.force_dim = force_dim
        self.binding_rect = binding_rect
        self.borderradius = borderradius

    def label(self, xy, **kwargs):
        return Label(
            self.surface,
            kwargs.get('text', self.text),
            kwargs.get('size', self.size),
            xy,
            kwargs.get('anchor', self.anchor),
            kwargs.get('textcolor', self.textcolor),
            kwargs.get('backgroundcolor', self.backgroundcolor),
            kwargs.get('antialias', self.antialias),
            kwargs.get('font', self.font),
            kwargs.get('x_axis_addition', self.x_axis_addition),
            kwargs.get('y_axis_addition', self.y_axis_addition),
            kwargs.get('borderwidth', self.borderwidth),
            kwargs.get('bordercolor', self.bordercolor),
            kwargs.get('force_width', self.force_width),
            kwargs.get('force_height', self.force_height),
            kwargs.get('force_dim', self.force_dim),
            kwargs.get('binding_rect', self.binding_rect),
            kwargs.get('borderradius', self.borderradius)
        )


class ImageImport_rotate:
    def __init__(self, assets_dir):
        """
        Simplifies image importing ('up','right','dowm','left').
        """
        self.assets_dir = assets_dir

    def load(self, img_name, width, height, facing="right", colorkey=None, assets_dir=None):
        if assets_dir != None:
            ad = assets_dir
        else:
            ad = self.assets_dir
        try:
            img = pygame.image.load(os.path.join(ad, img_name))
        except:
            raise ValueError(
                f"Could not find file '{img_name}' in '{ad}'.")
        img = pygame.transform.scale(img, (int(width), int(height)))
        if colorkey != None:
            img.set_colorkey(colorkey)
        if facing == "right":
            self.img_right = img
            self.img_down = pygame.transform.rotate(img, 270)
            self.img_left = pygame.transform.rotate(img, 180)
            self.img_up = pygame.transform.rotate(img, 90)
        elif facing == "down":
            self.img_down = img
            self.img_left = pygame.transform.rotate(img, 270)
            self.img_up = pygame.transform.rotate(img, 180)
            self.img_right = pygame.transform.rotate(img, 90)
        elif facing == "left":
            self.img_left = img
            self.img_up = pygame.transform.rotate(img, 270)
            self.img_right = pygame.transform.rotate(img, 180)
            self.img_down = pygame.transform.rotate(img, 90)
        elif facing == "up":
            self.img_up = img
            self.img_right = pygame.transform.rotate(img, 270)
            self.img_down = pygame.transform.rotate(img, 180)
            self.img_left = pygame.transform.rotate(img, 90)

        dct = {}
        dct["right"] = self.img_right
        dct["down"] = self.img_down
        dct["left"] = self.img_left
        dct["up"] = self.img_up
        return dct


class ImageImport_flip:
    def __init__(self, assets_dir):
        """
        Simplifies image importing ('right','left').
        """
        self.assets_dir = assets_dir

    def load(self, img_name, width, height, facing="right", colorkey=None, assets_dir=None):
        if assets_dir != None:
            ad = assets_dir
        else:
            ad = self.assets_dir
        try:
            img = pygame.image.load(os.path.join(ad, img_name))
        except:
            raise ValueError(
                f"Could not find file '{img_name}' in '{ad}'.")
        img = pygame.transform.scale(img, (int(width), int(height)))
        if colorkey != None:
            img.set_colorkey(colorkey)
        if facing == "right":
            self.img_right = img
            self.img_left = pygame.transform.flip(img, True, False)
        elif facing == "left":
            self.img_left = img
            self.img_right = pygame.transform.flip(img, True, False)

        dct = {}
        dct["right"] = self.img_right
        dct["left"] = self.img_left
        return dct


class Tile:
    def __init__(self, image, rect, type=None, hitbox=None, pos_hint=None):
        """
        image needs to be an image of the size of rect.
        rect needs to be a pygame.Rect object.
        hitbox can be None or a pygame.Rect object.
        """
        self.image = image
        self.rect = rect
        self.type = type
        self.pos_hint = pos_hint
        if hitbox != None:
            self.hitbox = pygame.Rect(
                self.rect.x + hitbox.x,
                self.rect.y + hitbox.y,
                hitbox.width,
                hitbox.height
            )


class Spritesheet:
    def __init__(self, path_to_folder: str, images_facing: str = "right"):
        """
        <name> must be the path to the folder containing the files listed below \n
        every file inside that folder must have the same name as the folder itself (ignoring endings) \n

        use self.get_frames to get images from the spritesheet (not self.__get_frame__ !)

        files necessary:
            - <name>.png
            - <name>.json (containing metadata)

        (works only with aseprite, best with horizontal strip)

        the json file has to have the following structure (the names
        of the frames have to be called just by their number):
        {
            "frames": {
                1: {
                    "frame": {
                        "x": ...,
                        "y": ...,
                        "w": ...,
                        "h": ...
                    }
                }
            }
        }
        """
        foldername = path_to_folder.split(os.sep)[-1]
        png_file = os.path.join(os.path.abspath(path_to_folder), (foldername + ".png"))
        json_file = os.path.join(os.path.abspath(path_to_folder), (foldername + ".json"))
        if not os.path.exists(png_file):
            raise FileNotFoundError(f"Could not find file {png_file}")
        elif not os.path.exists(json_file):
            raise FileNotFoundError(f"Could not find file {json_file}")

        self.base_image = pygame.image.load(png_file)
        with open(json_file) as f:
            self.metadata = json.load(f)

        assert images_facing in ["left", "right"], "invalid direction"
        self.images_facing = images_facing

    def __get_frame__(
            self, frame_number: int, colorkey: tuple[int, int, int] = (0, 0, 0),
            resize_factor: int = 1) -> dict:
        """returns a dict with images (left, right, flipped_left, flipped_right)"""

        assert self.metadata["frames"][str(frame_number)], f"no frame with number '{frame_number}' found"
        assert resize_factor > 0, "resize factor must be above 0"

        x = self.metadata["frames"][str(frame_number)]["frame"]["x"]
        y = self.metadata["frames"][str(frame_number)]["frame"]["y"]
        width = self.metadata["frames"][str(frame_number)]["frame"]["w"]
        height = self.metadata["frames"][str(frame_number)]["frame"]["h"]
        base_surface = pygame.Surface((width, height))
        base_surface.set_colorkey(colorkey)
        base_surface.blit(self.base_image, (0, 0), (x, y, width, height))

        if resize_factor != 1:
            new_width, new_height = int(width*resize_factor), int(height*resize_factor)
            base_surface = pygame.transform.scale(base_surface, (new_width, new_height))

        if self.images_facing == "right":
            img_dict = {
                "right": base_surface,
                "left": pygame.transform.flip(base_surface, True, False),
                "flipped_right": pygame.transform.flip(base_surface, False, True),
                "flipped_left": pygame.transform.flip(base_surface, False, True)
            }
        elif self.images_facing == "left":
            img_dict = {
                "right": pygame.transform.flip(base_surface, True, False),
                "left": base_surface,
                "flipped_right": pygame.transform.flip(base_surface, True, True),
                "flipped_left": pygame.transform.flip(base_surface, False, True)
            }

        return img_dict

    def get_frames(self, first_frame_number: int, last_frame_number: int,
                   colorkey: tuple[int, int, int] = (0, 0, 0),
                   resize_factor: int = 1) -> list[dict]:
        """ returns a list of the requested frames \n
        first_frame_number and last_frame_number are inclusive """
        # try:
        return [self.__get_frame__(i, colorkey, resize_factor) for i in range(first_frame_number, last_frame_number + 1)]
        # except KeyError:
        #     raise KeyError(
        #         f"key not found. you probably requested more frames than there are pictures in this spritesheet")

    def get_size(self, frame_number=0):
        width = self.metadata["frames"][str(frame_number)]["frame"]["w"]
        height = self.metadata["frames"][str(frame_number)]["frame"]["h"]
        return [width, height]


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        """
        call super().__init__() right after creating self.image and self.rect

        IMPORTANT: images for animations must be a dict like:
        {
            left: img_left,
            right: img_right
        }

        self.__action__ will be priorized over self.__looping_action_   #! (is it?)

        use Pygame_Engine.Spritesheet for images (in self.add_action(...))
        """
        super().__init__()

        self.__entity_pos__ = [0, 0]
        self.rect = pygame.Rect(
            0, 0, self.rect.width, self.rect.height)

        self.__hitbox_data__ = (0, 0, self.rect.width, self.rect.height)
        self.__initial_hitbox_data__ = (0, 0, self.rect.width,
                                        self.rect.height)
        self.__hitbox_rect__ = pygame.Rect(
            0, 0, self.rect.width, self.rect.height)

        self.__game_map_tiles__ = None
        self.__do_tile_collision__ = False
        self.__tile_sidelength__ = None
        self.__is_platformer__ = False
        self.__is_touching_ground_precision__ = 0

        # ? idea: a dict that contains what happens during an action (eg "launch rocket at frame 7" or "die at frame 15")
        # ? the dict stores strings that look like functions and that can be called with "exec()"

        # a dict with useful data, such as "has moved", "which direction moved", "jumped", old_center, ...
        # updates every frame so all the data is accessible
        self.__data__ = {
            "old_center": (0, 0),
            "center": (0, 0),
            "last_movement": (0, 0),
            "current_movement": (0, 0),
            "has_moved": False,
            "has_moved_left": False,
            "has_moved_up": False,
            "has_moved_right": False,
            "has_moved_down": False,
            "direction": "right",
            "width": self.rect.width,
            "height": self.rect.height,
            "rect": self.rect,

            # for platformers
            "is_touching_ground": False
        }
        self.__data__["is_touching_ground_list"] = [False for i in range(
            self.__is_touching_ground_precision__)]  # [new, old, older, ...]

        # checking the init-method
        self.__init_check__ = {
            "self.add_action": False,
            "self.set_looping_action": False,
            "self.set_speed": False,
            "self.set_tile_collision": False
        }
        self.__init_check_success__ = False

        # contains the images, that are blitted next
        self.__animation_sequence__ = []

        # current 'action', change with self.__set_action__()
        self.__action__ = None
        self.__looping_action__ = None
        self.__current_action__ = None
        self.__actions__ = {}
        self.__action_run_timer__ = 0

        # additional data for movement
        self.__entity_speed__ = 0
        self.__movement_vector__ = [0, 0]
        self.__constant_movement_vector__ = [0, 0]
        self.__constant_movement_max_vector__ = [0, 0]
        self.__constant_movement_initial_vector__ = [0, 0]
        self.__constant_movement_affection__ = False
        self.__knockback_vector__ = [0, 0]
        self.__knockback_resistance__ = 1
        self.__automatic_direction_control__ = True
        self.__direction_factor__ = 1  # -1 == left; 1 == right
        self.__rotation__ = 0
        self.__rotation_point_right__ = (0, 0)
        self.__rotation_point_left__ = (0, 0)
        self.__temp_collision_rects__ = []

    def __get_distance__(self, xy1, xy2, digits_after_comma=None):
        x1, y1 = xy1[0], xy1[1]
        x2, y2 = xy2[0], xy2[1]
        if digits_after_comma == None:
            return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        else:
            return self.round_half_up(math.sqrt(((x2-x1)**2)+((y2-y1)**2)), digits_after_comma)

    def __get_angle_between_points__(self, xy1, xy2):
        vect = pygame.math.Vector2(xy2[0]-xy1[0], xy2[1]-xy1[1])
        if vect.length() != 0:
            vect.normalize()
        cos = self.__rhu__(vect.y, 2)
        deg_cos = int(math.degrees(math.acos(vect.x)))
        if cos <= 0:
            return deg_cos
        else:
            return 180 + (180-deg_cos)

    def __get_normalized_vector_between_points__(self, xy1, xy2):
        return pygame.math.Vector2(xy2[0]-xy1[0], xy2[1]-xy1[1]).normalize()

    def __get_normalized_vector_from_angle__(self, angle):
        vect = pygame.Vector2(self.__rhu__(math.cos(math.radians(
            angle)), 3), self.__rhu__(math.sin(math.radians(angle)), 3))
        return vect.normalize()

    def __rhu__(self, n, decimals=0):
        """ -> round_half_up """
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier

    def __reset_constant_movement_vector__(self):
        self.__constant_movement_vector__ = self.__constant_movement_initial_vector__[:]

    def __move__(self):

        # x movement ##########################################################################################

        if self.__knockback_vector__[0] != 0:
            self.__movement_vector__[0] += self.__knockback_vector__[0]
            self.__knockback_vector__[0] = int(self.__knockback_vector__[0] / self.__knockback_resistance__)

        if self.__constant_movement_affection__:
            self.__movement_vector__[0] += self.__constant_movement_vector__[0]

            if (self.__movement_vector__[0] > 0 and self.__constant_movement_vector__[0] > 0) or \
                    (self.__movement_vector__[0] < 0 and self.__constant_movement_vector__[0] < 0):
                self.__constant_movement_vector__[0] += self.__constant_movement_initial_vector__[0]
            else:
                self.__constant_movement_vector__[0] = self.__constant_movement_initial_vector__[0]

            # limits the vector to its maximum value
            if self.__constant_movement_max_vector__[0] > 0:
                if self.__constant_movement_vector__[0] > self.__constant_movement_max_vector__[0]:
                    self.__constant_movement_vector__[0] = self.__constant_movement_max_vector__[0]
            elif self.__constant_movement_max_vector__[0] < 0:
                if self.__constant_movement_vector__[0] < self.__constant_movement_max_vector__[0]:
                    self.__constant_movement_vector__[0] = self.__constant_movement_max_vector__[0]

        self.rect.x += self.__movement_vector__[0]
        self.__adjust_hitbox_position__()
        if self.__do_tile_collision__:
            surrounding_tiles = self.__get_tiles_within_radius__(
                self.__game_map_tiles__, self.get_pos_factor(1/self.__tile_sidelength__))
            if len(self.__temp_collision_rects__) > 0:
                surrounding_tiles += self.__temp_collision_rects__
            collided_tiles = self.__tile_collision_test__(surrounding_tiles)
            for tile in collided_tiles:
                if self.__movement_vector__[0] > 0:
                    self.__hitbox_rect__.right = tile.left
                elif self.__movement_vector__[0] < 0:
                    self.__hitbox_rect__.left = tile.right
                self.__adjust_rect_position__()
                self.__constant_movement_vector__[0] = self.__constant_movement_initial_vector__[0]
                self.__knockback_vector__[0] = 0
        self.__movement_vector__[0] = 0

        # y movement ##########################################################################################

        if self.__knockback_vector__[1] != 0:
            self.__movement_vector__[1] += self.__knockback_vector__[1]
            self.__knockback_vector__[1] = int(self.__knockback_vector__[1] / self.__knockback_resistance__)

        if self.__constant_movement_affection__:
            self.__movement_vector__[1] += self.__constant_movement_vector__[1]

            if (self.__movement_vector__[1] > 0 and self.__constant_movement_vector__[1] > 0) or \
                    (self.__movement_vector__[1] < 0 and self.__constant_movement_vector__[1] < 0):
                self.__constant_movement_vector__[1] += self.__constant_movement_initial_vector__[1]
            else:
                self.__constant_movement_vector__[1] = self.__constant_movement_initial_vector__[1]

            # limits the vector to its maximum value
            if self.__constant_movement_max_vector__[1] > 0:
                if self.__constant_movement_vector__[1] > self.__constant_movement_max_vector__[1]:
                    self.__constant_movement_vector__[1] = self.__constant_movement_max_vector__[1]
            elif self.__constant_movement_max_vector__[1] < 0:
                if self.__constant_movement_vector__[1] < self.__constant_movement_max_vector__[1]:
                    self.__constant_movement_vector__[1] = self.__constant_movement_max_vector__[1]

        if self.__is_platformer__:
            # moving the list by one
            for i in range(self.__is_touching_ground_precision__-1, 0, -1):
                self.__data__["is_touching_ground_list"][i] = self.__data__["is_touching_ground_list"][i-1]

            self.__data__["is_touching_ground_list"][0] = False
            old_y = self.rect.y
        self.rect.y += self.__movement_vector__[1]
        self.__adjust_hitbox_position__()
        if self.__do_tile_collision__:
            surrounding_tiles = self.__get_tiles_within_radius__(
                self.__game_map_tiles__, self.get_pos_factor(1/self.__tile_sidelength__))
            if len(self.__temp_collision_rects__) > 0:
                surrounding_tiles += self.__temp_collision_rects__
            collided_tiles = self.__tile_collision_test__(surrounding_tiles)
            for tile in collided_tiles:
                if self.__movement_vector__[1] > 0:
                    self.__hitbox_rect__.bottom = tile.top
                elif self.__movement_vector__[1] < 0:
                    self.__hitbox_rect__.top = tile.bottom
                self.__adjust_rect_position__()
                self.__constant_movement_vector__[1] = self.__constant_movement_initial_vector__[1]
                self.__knockback_vector__[1] = 0

        if self.__is_platformer__:
            if old_y == self.rect.y:
                self.__data__["is_touching_ground_list"][0] = True
        self.__movement_vector__[1] = 0

        self.__temp_collision_rects__ = []

    def __update_data__(self):
        self.__data__["old_center"] = self.__data__["center"]
        self.__data__["center"] = self.get_pos()
        self.__data__["last_movement"] = (
            self.__data__["center"][0] - self.__data__["old_center"][0],
            self.__data__["center"][1] - self.__data__["old_center"][1]
        )
        self.__data__["has_moved_left"] = self.__data__["last_movement"][0] < 0
        self.__data__["has_moved_right"] = self.__data__["last_movement"][0] > 0
        self.__data__["has_moved_up"] = self.__data__["last_movement"][1] < 0
        self.__data__["has_moved_down"] = self.__data__["last_movement"][1] > 0
        self.__data__["has_moved"] = any(
            [self.__data__["has_moved_" + direction]
             for direction in "left,up,right,down".split(",")])
        if self.__automatic_direction_control__ and self.__data__["has_moved"]:
            if self.__data__["has_moved_left"]:
                self.__data__["direction"] = "left"
                self.__direction_factor__ = -1
            elif self.__data__["has_moved_right"]:
                self.__data__["direction"] = "right"
                self.__direction_factor__ = 1
        self.__data__["is_touching_ground"] = all(self.__data__["is_touching_ground_list"])

        # updating global position and position on the screen
        self.__entity_pos__ = list(self.get_pos())
        self.rect.center = self.get_pos()

    def __update_image__(self):

        self.__action_run_timer__ += 1

        static_image = False  # ! not tested (15.2.2022, 11:57)
        if self.__animation_sequence__ == []:
            if len(self.__actions__[self.__looping_action__]["frames"]) == 1:
                static_image = True
                next_image = self.__actions__[
                    self.__looping_action__]["frames"][0][
                    self.__data__["direction"]]
            else:
                self.__animation_sequence__ += self.__actions__[self.__looping_action__]["frames"]
                self.__action_run_timer__ = 0
                self.__current_action__ = self.__looping_action__

        if not static_image:
            try:
                next_image = self.__animation_sequence__[0][self.__data__["direction"]]
            except TypeError as e:
                raise Exception(
                    "At least some elements of the action '" + self.__current_action__ +
                    "' are not formatted correctly. Make sure that all elements are in the form of a dict: \n{'left': <image_left>, 'right': <image_right>}")

        if self.__rotation__ != 0:  # ! not tested (15.2.2022, 11:47)
            blue_vect = pygame.Vector2(
                self.__rotation_point_right__[0] * self.get_direction_factor(),
                self.__rotation_point_right__[1])
            saved_center = pygame.Vector2(
                self.rect.center) + pygame.Vector2(
                self.__rotation_point_right__[0] * self.get_direction_factor(),
                self.__rotation_point_right__[1])
            new_vect = blue_vect.rotate(-self.__rotation__ * self.get_direction_factor())
            next_image = pygame.transform.rotate(next_image, self.__rotation__ * self.get_direction_factor())
            self.rect = self.image.get_rect(center=saved_center - new_vect)

        # ? check hitbox stuff
        # ? check pygame.mask

        self.image = next_image

        if not static_image:
            del self.__animation_sequence__[0]

    def __execute_action_methods__(self):
        if self.__action_run_timer__ in self.__actions__[
                self.__current_action__]["methods_to_execute"].keys():
            string = "self." + self.__actions__[
                self.__current_action__]["methods_to_execute"][
                self.__action_run_timer__]
            try:
                exec(string)
            except Exception as e:
                raise Exception(
                    f"An error occurred while executing a method from the action '{self.__current_action__}':\n\n{e}")

    def __tile_collision_test__(self, tiles: list) -> list:
        """ not very precise, should only be used for movement """
        collisions = []
        for tile in tiles:
            if self.__hitbox_rect__.colliderect(tile):
                collisions.append(tile)
        return collisions

    def __get_tiles_within_radius__(self, tiles_in_2d: list[list], xy: tuple, radius: int = 2) -> list:
        """ gets awfully inefficient with increasing radius, but 2 should be sufficient for everything """
        # automatically avoids crossing game borders
        tiles = []
        for x in range(max(int(xy[0])-radius, 0),
                       min(int(xy[0])+radius, len(tiles_in_2d))):
            for y in range(max(int(xy[1])-radius, 0),
                           min(int(xy[1])+radius, len(tiles_in_2d[0]))):
                if tiles_in_2d[x][y] != 0:
                    tiles.append(tiles_in_2d[x][y])
        return tiles

    def __adjust_hitbox_position__(self):
        self.__hitbox_rect__.topleft = (
            self.rect.topleft[0] + self.__hitbox_data__[0],
            self.rect.topleft[1] + self.__hitbox_data__[1])

    def __adjust_rect_position__(self):
        self.rect.topleft = (
            self.__hitbox_rect__.topleft[0] - self.__hitbox_data__[0],
            self.__hitbox_rect__.topleft[1] - self.__hitbox_data__[1])

    def __init_check_func__(self):
        if not all(self.__init_check__.values()):
            string1 = [f"{k}: {v}" for k, v in self.__init_check__.items()]
            string2 = "\n".join(string1)
            raise Exception(f"Not all necessary init-methods called:\n\n{string2}")

    def internal_update(self):
        """ needs to be called at the end of the entities .move method \n
            methods can also be called individually """
        if self.__init_check_success__ == False:
            self.__init_check_func__()
            self.__init_check_success__ = True

        self.__move__()
        self.__update_data__()
        self.__update_image__()
        self.__execute_action_methods__()

    def add_action(self, name: str, image_dicts: list, frames_per_image: list[int],
                   methods_to_execute: dict[str: str] = None):
        """
        image_dicts: dicts of image ("left":..., "right":...)
        frames_per_image can be either a list or an int \n
        adds an action to self.__actions__ in the following form:
        {
            "<action_name>": {
                "frames": ["<frame0>", "<frame1>", "<frame2>", ...],
                "methods_to_execute": {
                    "<frame>": "self.method(*args)",
                    ...
                }
            }
        }
        """
        if type(frames_per_image) == list:
            assert len(image_dicts) == len(
                frames_per_image), "received lists of different lengths"

        # creating list
        frame_sequence = []
        if type(frames_per_image) == list:
            for image, count in zip(image_dicts, frames_per_image):
                for i in range(count):
                    frame_sequence.append(image)
        elif type(frames_per_image) == int:
            for image in image_dicts:
                for i in range(frames_per_image):
                    frame_sequence.append(image)

        # adding "methods_to_execute" functionality
        self._layer = None  # dont ask why this is here, but it crashes if it isnt
        if methods_to_execute != None:
            method_list = [func for func in dir(self) if callable(
                getattr(self, func)) and not func.startswith("__")]  # "set_action", ...
            for k, v in methods_to_execute.items():
                if type(k) != int:
                    raise ValueError(
                        f"Error in 'methods_to_execute': '{k}' is not a number")
                if v.split("(")[0] not in method_list:  # ) avoid brackets changing colors
                    # ! not sure if this works as intended
                    raise Exception(
                        f"Error in 'methods_to_execute': '{v.split('(')[0]}' is not a valid method")  # )
        else:
            methods_to_execute = {}

        self.__actions__[name] = {
            "frames": frame_sequence,
            "methods_to_execute": methods_to_execute
        }
        self.__init_check__["self.add_action"] = True

    def set_looping_action(self, action: str, cancel_other_action: bool = True) -> None:
        assert action in self.__actions__.keys(), f"unknown action: '{action}'"
        if cancel_other_action and self.__looping_action__ != action:
            self.__animation_sequence__ = []
            self.__animation_sequence__ += self.__actions__[action]["frames"]
            self.__action_run_timer__ = 0
            self.__current_action__ = action
        self.__looping_action__ = action
        self.__init_check__["self.set_looping_action"] = True

    def set_action(self, action: str, cancel_other_action: bool = True) -> None:
        assert action in self.__actions__.keys(), f"unknown action: '{action}'"
        if cancel_other_action and self.__current_action__ != action:
            self.__animation_sequence__ = []
            self.__animation_sequence__ += self.__actions__[action]["frames"]
            self.__action_run_timer__ = 0
            self.__current_action__ = action
        self.__action__ = action

    def get_data(self, name: str):
        """ access useful data like "has_moved", "last_movement", etc. """
        assert name in self.__data__.keys(), f"no entry in __data__ for '{name}'"
        return self.__data__[name]

    def set_speed(self, speed: float):
        """ needs to be called in the init-method """
        self.__entity_speed__ = speed
        self.__init_check__["self.set_speed"] = True

    def get_speed(self):
        return self.__entity_speed__

    def move_right(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[0] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[0] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_left(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[0] -= self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[0] -= custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_up(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[1] -= self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[1] -= custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_down(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[1] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[1] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_horizontal(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[0] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[0] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_vertical(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[1] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[1] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def get_pos(self, reference_point="center"):
        """ uses pixel """
        assert reference_point in ["topleft", "top", "topright",
                                   "left", "center", "centerx", "centery", "right",
                                   "bottomleft", "bottom", "bottomright"]

        if reference_point == "topleft":
            return self.rect.topleft
        elif reference_point == "top":
            return self.rect.top
        elif reference_point == "topright":
            return self.rect.topright
        elif reference_point == "left":
            return self.rect.left
        elif reference_point == "center":
            return self.rect.center
        elif reference_point == "centerx":
            return self.rect.centerx
        elif reference_point == "centery":
            return self.rect.centery
        elif reference_point == "right":
            return self.rect.right
        elif reference_point == "bottomleft":
            return self.rect.bottomleft
        elif reference_point == "bottom":
            return self.rect.bottom
        elif reference_point == "bottomright":
            return self.rect.bottomright

    def get_pos_factor(self, factor, reference_point="center", decimals=0):
        """ uses the coordinate system """
        assert reference_point in ["topleft", "top", "topright",
                                   "left", "center", "centerx", "centery", "right",
                                   "bottomleft", "bottom", "bottomright"]

        if reference_point == "topleft":
            return self.__rhu__(
                self.rect.topleft[0] * factor, decimals), self.__rhu__(
                self.rect.topleft[1],
                decimals)
        elif reference_point == "top":
            return self.__rhu__(self.rect.top * factor, decimals)
        elif reference_point == "topright":
            return self.__rhu__(
                self.rect.topright[0] * factor, decimals), self.__rhu__(
                self.rect.topright[1] * factor, decimals)
        elif reference_point == "left":
            return self.__rhu__(self.rect.left * factor, decimals)
        elif reference_point == "center":
            return self.__rhu__(
                self.rect.center[0] * factor, decimals), self.__rhu__(
                self.rect.center[1] * factor, decimals)
        elif reference_point == "centerx":
            return self.__rhu__(self.rect.centerx * factor, decimals)
        elif reference_point == "centery":
            return self.__rhu__(self.rect.centery * factor, decimals)
        elif reference_point == "right":
            return self.__rhu__(self.rect.right * factor, decimals)
        elif reference_point == "bottomleft":
            return self.__rhu__(
                self.rect.bottomleft[0] * factor, decimals), self.__rhu__(
                self.rect.bottomleft[1] * factor, decimals)
        elif reference_point == "bottom":
            return self.__rhu__(self.rect.bottom * factor, decimals)
        elif reference_point == "bottomright":
            return self.__rhu__(
                self.rect.bottomright[0] * factor, decimals), self.__rhu__(
                self.rect.bottomright[1] * factor, decimals)

    def set_pos(self, xy, reference_point="center"):
        """ uses pixel \n <xy> can be either a tuple or an integer, depending on <reference_point> """
        assert type(xy) in [tuple, list, int, pygame.Vector2]
        assert type(reference_point) == str
        if reference_point in ["topleft", "topright", "center", "bottomleft", "bottomright"]:
            assert type(xy) in [
                tuple, list, int, pygame.Vector2], f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"
            assert len(xy) == 2, f"invalid length of tuple <xy> ({xy})"
        elif reference_point in ["top", "left", "centerx", "centery", "right", "bottom"]:
            assert type(
                xy) == int, f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"

        if reference_point == "topleft":
            self.rect.topleft = xy
        elif reference_point == "top":
            self.rect.top = xy
        elif reference_point == "topright":
            self.rect.topright = xy
        elif reference_point == "left":
            self.rect.left = xy
        elif reference_point == "center":
            self.rect.center = xy
        elif reference_point == "centerx":
            self.rect.centerx = xy
        elif reference_point == "centery":
            self.rect.centery = xy
        elif reference_point == "right":
            self.rect.right = xy
        elif reference_point == "bottomleft":
            self.rect.bottomleft = xy
        elif reference_point == "bottom":
            self.rect.bottom = xy
        elif reference_point == "bottomright":
            self.rect.bottomright = xy

        self.__entity_pos__ = list(self.rect.center)

    def set_pos_factor(self, xy, factor: int, reference_point="center"):
        """ uses the coordinate system if <factor> == self.__tile_sidelength__ \n <xy> can be either a tuple or an integer, depending on <reference_point> """
        assert type(xy) in [tuple, list, int]
        assert type(reference_point) == str
        # <factor> could (and should!) be automated with the side length of the current levels tiles
        if reference_point in ["topleft", "topright", "center", "bottomleft", "bottomright"]:
            assert type(xy) in [
                list, tuple], f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"
            assert len(xy) == 2, f"invalid length of tuple <xy> ({xy})"
        elif reference_point in ["top", "left", "centerx", "centery", "right", "bottom"]:
            assert type(
                xy) == int, f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"

        assert type(factor) == int, f"invalid argument for <factor> ({factor}), integer required"

        if reference_point == "topleft":
            self.rect.topleft = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "top":
            self.rect.top = xy * factor
        elif reference_point == "topright":
            self.rect.topright = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "left":
            self.rect.left = xy * factor
        elif reference_point == "center":
            self.rect.center = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "centerx":
            self.rect.centerx = xy * factor
        elif reference_point == "centery":
            self.rect.centery = xy * factor
        elif reference_point == "right":
            self.rect.right = xy * factor
        elif reference_point == "bottomleft":
            self.rect.bottomleft = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "bottom":
            self.rect.bottom = xy * factor
        elif reference_point == "bottomright":
            self.rect.bottomright = (xy[0] * factor, xy[1] * factor)

        self.__entity_pos__ = list(self.rect.center)

    def move_to(self, xy, reference_point="center"):
        """ same as self.set_pos() """
        self.set_pos(xy, reference_point)

    def set_game_map_tiles(self, tiles: list[list], do_tile_collision: bool = True):
        """ <tiles> must be a 2d list of pygame.Rect objects """
        assert type(tiles) == list, "failed to load map tiles"
        assert type(tiles[0]) == list, "failed to load map tiles"
        assert type(do_tile_collision) == bool
        self.__game_map_tiles__ = tiles
        self.__do_tile_collision__ = do_tile_collision

    def set_tile_collision(self, boolean: bool, tile_sidelength: int = None):
        assert type(boolean) == bool
        self.__do_tile_collision__ = boolean
        if boolean == True:
            assert tile_sidelength != None, "if tile_collision should be done, tile_sidelength needs to be set"
            assert type(tile_sidelength) == int
            assert tile_sidelength >= 8, "tile_sidelength must be greater or equal to 8"
            self.set_tile_sidelength(tile_sidelength)
        self.__init_check__["self.set_tile_collision"] = True

    def get_tile_sidelength(self):
        return self.__tile_sidelength__

    def set_constant_movement(self, vector2: tuple, max_vector2: tuple,
                              set_constant_movement_affection: bool = True):
        assert type(vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({vector2})"
        assert len(vector2) == 2, f"invalid vector ({vector2})"
        assert type(max_vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({max_vector2})"
        assert len(max_vector2) == 2, f"invalid vector ({max_vector2})"
        assert type(set_constant_movement_affection) == bool

        self.__constant_movement_vector__ = list(vector2)
        self.__constant_movement_max_vector__ = list(max_vector2)
        self.__constant_movement_initial_vector__ = list(vector2)
        self.set_constant_movement_affection(set_constant_movement_affection)

    def get_constant_movement(self):
        return self.__constant_movement_vector__

    def set_constant_movement_affection(self, boolean):
        assert type(boolean) == bool
        self.__constant_movement_affection__ = boolean

    def get_constant_movement_affection(self):
        return self.__constant_movement_affection__

    def set_custom_hitbox(self, rect: tuple[int, int, int, int]):
        """ sets a custom hitbox for tile collision """
        assert type(rect) in [list, tuple]
        assert len(rect) == 4

        self.__hitbox_data__ = rect
        self.__hitbox_rect__ = pygame.Rect(*rect)
        self.__adjust_hitbox_position__()

    def get_hitbox(self):
        return self.__hitbox_rect__

    def reset_hitbox(self):
        """ resets the hitbox to default (the entities 'rect') """
        self.__hitbox_data__ = self.__initial_hitbox_data__
        self.__hitbox_rect__ = pygame.Rect(*self.__hitbox_data__)
        self.__adjust_hitbox_position__()

    def set_knockback_resistance(self, knockback_resistance: float):
        """ sets the number the knockback vector will be divided by each frame, must be between 1 and 1.2 """
        assert 1 < knockback_resistance <= 1.2, "knockback_resistance must be between 1 and 1.2"
        self.__knockback_resistance__ = knockback_resistance

    def get_knockback_resistance(self):
        """ returns the number the knockback vector gets divided by """
        return self.__knockback_resistance__

    def set_knockback(self, vector2: tuple, reset_constant_movement: bool = True):
        """ applies knockback to the entity """
        assert type(vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({vector2})"
        assert len(vector2) == 2, f"invalid vector ({vector2})"
        assert self.__knockback_resistance__ != 1, "knockback_resistance must be between 1 and 1.2"

        self.__knockback_vector__ = list(vector2)
        if reset_constant_movement:
            self.__reset_constant_movement_vector__()

    def add_knockback(self, vector2: tuple):
        """ applies additional knockback on top of the current one to the entity """
        assert type(vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({vector2})"
        assert len(vector2) == 2, f"invalid vector ({vector2})"
        assert self.__knockback_resistance__ != 1, "knockback_resistance must be between 1 and 1.2 "

        self.__knockback_vector__ = [
            self.__knockback_vector__[0] + vector2[0],
            self.__knockback_vector__[1] + vector2[1]]

    def move_at_angle(self, angle, custom_speed=None):
        """ 0 degrees = right | then clockwise """
        temp_vect = self.__get_normalized_vector_from_angle__(angle)
        if custom_speed != None:
            vect = temp_vect * custom_speed
        else:
            vect = temp_vect * self.__entity_speed__

        self.__movement_vector__[0] += vect[0]
        self.__movement_vector__[1] += vect[1]

    def set_tile_sidelength(self, tile_sidelength: int):
        assert type(tile_sidelength) == int
        self.__tile_sidelength__ = tile_sidelength

    def set_platformer_status(self, is_platformer: bool, set_touching_ground_precision: int = 3):
        """ decide whether the game is a platformer or not (enables some platformer features) """
        assert type(is_platformer) == bool
        self.__is_platformer__ = is_platformer
        self.set_touching_ground_precision(set_touching_ground_precision)

    def set_touching_ground_precision(self, precision: int):
        """ higher precision means that the ground will be detected with more certainty, 
        but it takes longer to realize that the entity is not touching the ground anymore...
        this might result in the player being able to jump again mid-air \n
        note: \n
        automatically calls self.set_platformer_status
        1 <= precision <= 6 | recommended value: 3 """
        assert type(precision) == int
        assert 1 <= precision <= 6
        self.__is_platformer__ = True
        self.__is_touching_ground_precision__ = precision
        self.__data__["is_touching_ground_list"] = [False for i in range(
            self.__is_touching_ground_precision__)]  # [new, old, older, ...]

    def set_automatic_direction_control(self, boolean: bool):
        """ automatically sets the direction of the entity based on its movement """
        assert type(boolean) == bool
        self.__automatic_direction_control__ = boolean

    def set_direction(self, direction):
        """ <direction> can be either "left" and "right" or -1 and 1 """
        assert direction in ["left", "right", -1, 1]
        if direction in ["left", -1]:
            self.__data__["direction"] = "left"
            self.__direction_factor__ = -1
        elif direction in ["right", 1]:
            self.__data__["direction"] = "right"
            self.__direction_factor__ = 1

    def get_direction(self):
        return self.get_data("direction")

    def get_direction_factor(self):
        return self.__direction_factor__

    def set_rotation_point_vector(self, xy: tuple):
        """ sets the point the entity rotates around; vector starts at the center of the entity; \n
            default = center; IMPORTANT: configure for entity facing right """
        assert type(xy) in [tuple, list, pygame.Vector2]
        self.__rotation_point_right__ = tuple(xy)
        self.__rotation_point_left__ = (xy[0]*-1, xy[1])

    def get_rotation_point_right(self) -> tuple:
        """ returns the point the entity rotates around when it is facing right """
        return self.__rotation_point_right__

    def get_rotation_point_left(self) -> tuple:
        """ returns the point the entity rotates around when it is facing left """
        return self.__rotation_point_left__

    def set_rotation(self, angle):
        """ sets the entities rotation to the given angle """
        assert type(angle) in [int, float]
        self.__rotation__ = int(angle) % 360

    def get_rotation(self):
        """ returns the current rotation """
        return self.__rotation__

    def do_platformer_jump(self, factor: float):
        self.__constant_movement_vector__[1] = factor

    def add_temp_collision_rects(self, rects: list):
        """ adds a list of rectangles to the collision tiles list for ONE iteration """
        assert type(rects) in [tuple, list]
        for item in rects:
            assert type(item) == pygame.Rect
        self.__temp_collision_rects__ = rects


class Keyboard:
    def __init__(self):
        self.keys = {
            pygame.locals.K_a: "a",
            pygame.locals.K_b: "b",
            pygame.locals.K_c: "c",
            pygame.locals.K_d: "d",
            pygame.locals.K_e: "e",
            pygame.locals.K_f: "f",
            pygame.locals.K_g: "g",
            pygame.locals.K_h: "h",
            pygame.locals.K_i: "i",
            pygame.locals.K_j: "j",
            pygame.locals.K_k: "k",
            pygame.locals.K_l: "l",
            pygame.locals.K_m: "m",
            pygame.locals.K_n: "n",
            pygame.locals.K_o: "o",
            pygame.locals.K_p: "p",
            pygame.locals.K_q: "q",
            pygame.locals.K_r: "r",
            pygame.locals.K_s: "s",
            pygame.locals.K_t: "t",
            pygame.locals.K_u: "u",
            pygame.locals.K_v: "v",
            pygame.locals.K_w: "w",
            pygame.locals.K_x: "x",
            pygame.locals.K_y: "y",
            pygame.locals.K_z: "z",
            pygame.locals.K_0: "0",
            pygame.locals.K_1: "1",
            pygame.locals.K_2: "2",
            pygame.locals.K_3: "3",
            pygame.locals.K_4: "4",
            pygame.locals.K_5: "5",
            pygame.locals.K_6: "6",
            pygame.locals.K_7: "7",
            pygame.locals.K_8: "8",
            pygame.locals.K_9: "9",
            pygame.locals.K_TAB: "\t",
            pygame.locals.K_SPACE: " ",
            pygame.locals.K_SEMICOLON: ";",
            pygame.locals.K_SLASH: "/",
            pygame.locals.K_RETURN: "\n",
            pygame.locals.K_PERIOD: ".",
            pygame.locals.K_PLUS: "+",
            pygame.locals.K_PERCENT: "%",
            pygame.locals.K_MINUS: "-",
            pygame.locals.K_HASH: "#",
            pygame.locals.K_UNDERSCORE: "_",
            pygame.locals.K_LEFTBRACKET: "(",
            pygame.locals.K_RIGHTBRACKET: ")",
            pygame.locals.K_LESS: "<",
            pygame.locals.K_GREATER: ">",
            pygame.locals.K_EQUALS: "=",
            pygame.locals.K_EURO: "€",
            pygame.locals.K_EXCLAIM: "!",
            pygame.locals.K_QUESTION: "?",
            pygame.locals.K_DOLLAR: "$",
            pygame.locals.K_COLON: ":",
            pygame.locals.K_COMMA: ",",
            pygame.locals.K_BACKSLASH: "\\",
            pygame.locals.K_ASTERISK: "*",
        }
        self.shift_keys = {
            pygame.locals.K_a: "A",
            pygame.locals.K_b: "B",
            pygame.locals.K_c: "C",
            pygame.locals.K_d: "D",
            pygame.locals.K_e: "E",
            pygame.locals.K_f: "F",
            pygame.locals.K_g: "G",
            pygame.locals.K_h: "H",
            pygame.locals.K_i: "I",
            pygame.locals.K_j: "J",
            pygame.locals.K_k: "K",
            pygame.locals.K_l: "L",
            pygame.locals.K_m: "M",
            pygame.locals.K_n: "N",
            pygame.locals.K_o: "O",
            pygame.locals.K_p: "P",
            pygame.locals.K_q: "Q",
            pygame.locals.K_r: "R",
            pygame.locals.K_s: "S",
            pygame.locals.K_t: "T",
            pygame.locals.K_u: "U",
            pygame.locals.K_v: "V",
            pygame.locals.K_w: "W",
            pygame.locals.K_x: "X",
            pygame.locals.K_y: "Y",
            pygame.locals.K_z: "Z",
            pygame.locals.K_0: "=",
            pygame.locals.K_1: "!",
            pygame.locals.K_2: "\"",
            pygame.locals.K_3: "§",
            pygame.locals.K_4: "$",
            pygame.locals.K_5: "%",
            pygame.locals.K_6: "&",
            pygame.locals.K_7: "/",
            pygame.locals.K_8: "(",
            pygame.locals.K_9: ")",
            pygame.locals.K_PERIOD: ":",
            pygame.locals.K_PLUS: "*",
            pygame.locals.K_MINUS: "_",
            pygame.locals.K_HASH: "'",
            pygame.locals.K_LESS: ">",
            pygame.locals.K_COMMA: ";"
        }
        self.__forbidden_chars__ = []

    def set_custom_value(self, custom_values: dict):
        """
        Sets custom return values specified by <custom_values>.
        """
        assert type(custom_values) == dict
        for k, v in custom_values.items():
            self.keys[k] = v
            self.shift_keys[k] = v

    def set_forbidden_characters(self, characters: list):
        """
        Bans all given characters.
        """
        assert type(characters) == list, f"invalid argument for 'characters': {characters}"
        for char in characters:
            assert type(char) == str, f"invalid character '{char}'"
            assert len(char) == 1, f"invalid character '{char}'"
            if char not in self.__forbidden_chars__:
                self.__forbidden_chars__.append(char)

    def get(self, event_list):
        """
        Returns a string of all keys pressed.
        """
        string = ""
        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_LSHIFT] or keys[pygame.locals.K_RSHIFT]:
            for e in event_list:
                if e.type == pygame.KEYDOWN and e.key:
                    char = self.shift_keys.get(e.key, "")
                    if char not in self.__forbidden_chars__:
                        string += char
        else:
            for e in event_list:
                if e.type == pygame.KEYDOWN and e.key:
                    char = self.keys.get(e.key, "")
                    if char not in self.__forbidden_chars__:
                        string += char
        return string


class FileDialogElement:
    def __init__(self, surface, name: str, count: int, role: str, topleft_pos, dimensions, textsize, textcolor,
                 backgroundcolor2, borderwidth):
        self.name = name
        self.role = role

        if self.role == "dir":
            bgc = (250, 150, 70)
        elif self.role == "file":
            bgc = backgroundcolor2

        self.b_name = Button(
            surface, name, textsize, (0, count * textsize),
            "topleft", fd=(dimensions[0], textsize),
            tc=textcolor, bgc=bgc, hl=True, bR=1, tb="midleft", to=(5, 1),
            aA=(topleft_pos[0] + 0, topleft_pos[1] + textsize, dimensions[0],
                dimensions[1] - textsize - 50), bc=(0, 0, 200), bw=borderwidth, br=1)

    def update(self, mouse_events, _offset):
        if self.b_name.update(mouse_events, offset=_offset):
            return True
        return False

    def draw(self):
        self.b_name.draw()


class FileDialog:
    def __init__(
            self, surface, pygame_clock, fps, topleft_pos=(100, 50),
            dimensions=(600, 400), textsize=25,
            textcolor=(0, 0, 0),
            backgroundcolor1=(150, 180, 240),
            backgroundcolor2=(128, 128, 128)):

        self.blitting_surface = surface
        self.pygame_clock = pygame_clock
        self.fps = fps
        self.topleft_pos = topleft_pos
        assert dimensions[0] >= 200
        assert dimensions[1] >= 200
        self.dimensions = dimensions
        assert 20 <= textsize <= 40
        self.textsize = textsize
        self.textcolor = textcolor
        self.backgroundcolor1 = backgroundcolor1
        self.backgroundcolor2 = backgroundcolor2


        w, h = self.dimensions
        self.center = (self.topleft_pos[0]+w//2, self.topleft_pos[1]+h//2)
        self.surface = pygame.Surface((w, h))
        self.surface.fill(self.backgroundcolor1)
        self.messagebox = Messagebox(self.blitting_surface, self.pygame_clock, self.fps, (topleft_pos[0]+dimensions[0]//2, topleft_pos[1]+dimensions[1]//2))
        self.l_path = Label(
            self.surface, "", textsize, (0, 0),
            "topleft", tc=self.textcolor, bgc=self.backgroundcolor1, br=1, tb="midright", to=(-4, 2),
            bR=1, fd=(self.dimensions[0],
                      textsize),
            bw=1)
        self.b_back = Button(
            self.surface, "<", int(textsize*1.5), (0, 0),
            "topleft", tc=self.textcolor, fd=(textsize, textsize),
            bgc=self.backgroundcolor1, hl=True, bw=1, bR=1, to=(0, -3))

        self.b_cancel = Button(self.surface, "Cancel", textsize,
                               (11, self.dimensions[1] - int(self.textsize * 1.5) // 2),
                               "midleft", tc=self.textcolor, bgc=self.backgroundcolor1, bR=1, xad=10,
                               fh=textsize, bw=3, br=1, hl=True)
        self.l_selected = Label(self.surface, "Selected:", textsize,
                                vect_sum(self.b_cancel.midright, (10, 0)),
                                "midleft", bR=1, tc=self.textcolor, bgc=self.backgroundcolor1)
        self.l_selected_name = Label(
            self.surface, "", textsize, vect_sum(self.l_selected.midright, (10, 0)),
            "midleft", bR=1, tc=self.textcolor, bgc=self.backgroundcolor1)
        self.b_open = Button(self.surface, "Open", textsize,
                             (self.dimensions[0] - 11, self.b_cancel.rect.centery),
                             "midright", tc=self.textcolor, bgc=self.backgroundcolor1, bR=1, xad=10,
                             fh=textsize, bw=3, br=1, hl=True)

        self.b_req_ending = Button(
            self.surface, "!", textsize, vect_sum(self.b_open.midleft, (-5, 0)),
            "midright", tc=(0,0,0), bR=1, f="bauhaus", to=(0, 0),
            br=1, fd=(textsize, textsize),
            bw=3, hl=True, bgc=(255, 80, 80))

    def error(self, error_message: str):
        surface = pygame.Surface((self.textsize*10, self.textsize*4))
        surface.fill(self.backgroundcolor2)
        rect = surface.get_rect()
        rect.center = self.center

        l_error = Label(surface, "Error", self.textsize, (0, 0), "topleft",
                        bR=1, tc=self.textcolor, fh=self.textsize, to=(7, 1))
        l_error_name = Label(surface, error_message, self.textsize,
                             (surface.get_width() // 2, int(self.textsize * 1.7)),
                             "midtop", tc=self.textcolor)
        b_okay = Button(
            surface, "OK", self.textsize, (surface.get_width() - 7, surface.get_height() - 7),
            "bottomright", tc=self.textcolor, bgc=self.backgroundcolor2, hl=True, xad=5, yad=3, bR=1, bw=2,
            br=1)

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            surface.fill(self.backgroundcolor2)
            l_error.draw()
            l_error_name.draw()
            b_okay.draw()
            pygame.draw.line(surface, (0, 0, 0), (0, self.textsize), (self.dimensions[0], self.textsize), 3)
            self.blitting_surface.blit(surface, rect)
            pygame.draw.rect(self.blitting_surface, (0, 0, 0), rect, 3, 1, 1, 1, 1)

            if b_okay.update(mouse_events, offset=rect.topleft):
                run = False

            pygame.display.flip()
            self.pygame_clock.tick(self.fps)

    def ask_filename(self, starting_path, required_ending: str = None, dim_background: bool = True) -> str:
        if not os.path.exists(starting_path):
            raise Exception(f"Given path does not exist. ({starting_path})")
        if required_ending != None:
            assert type(required_ending) == str, f"invalid argument for 'required_ending': {required_ending}"

        if dim_background:
            self.blitting_surface.fill([60 for i in range(3)], special_flags=pygame.BLEND_MULT)

        current_path = starting_path
        old_path = ""
        directory_scan: list

        buttons_list = []

        scroll = 0
        max_scroll = 0
        old_selected = ["", ""]  # [path, end_of_path]
        selected = ["", ""]
        self.l_selected_name.update_text("")

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                elif max_scroll > 0 and event.type == pygame.MOUSEWHEEL:
                    scroll = max(min(max_scroll, scroll + event.y*-1*int(self.textsize*1.5)), 0)

            # update
            if current_path != old_path or selected != old_selected:
                try:
                    directory_scan = os.scandir(current_path)

                    self.l_path.update_text(current_path.replace("\\", " > "))
                    old_path = current_path
                    buttons_list = []
                    MAX_ELEMENTS = 80
                    length = min(len(os.listdir(current_path)), MAX_ELEMENTS) * self.textsize
                    dir_surf = pygame.Surface((self.dimensions[0], length))
                    for count, path in enumerate(directory_scan):
                        if count == MAX_ELEMENTS:
                            break
                        new_path = os.path.join(current_path, path)
                        if os.path.isdir(new_path):
                            role = "dir"
                        elif os.path.isfile(new_path):
                            role = "file"
                        else:
                            raise Exception(f"what is this file? ({new_path})")
                        if path.name == selected[1]:
                            bw = 3
                        else:
                            bw = 0
                        buttons_list.append(FileDialogElement(dir_surf, path.name, count, role, self.topleft_pos,
                                                              self.dimensions, self.textsize, self.textcolor, self.backgroundcolor2, bw))
                    if selected == old_selected:
                        scroll = 0
                        max_scroll = length - (self.dimensions[1]-self.textsize-int(self.textsize*1.5))
                except PermissionError:
                    self.error("Permission denied.")
                    current_path = os.path.split(current_path)[0]

            if selected != old_selected:
                old_selected = selected[:]
                self.l_selected_name.update_text(selected[1])

            # updating each button
            for element in buttons_list:
                if element.update(
                    mouse_events, _offset=(self.topleft_pos[0],
                                           self.topleft_pos[1] + self.textsize + scroll)):
                    if element.role == "dir":
                        current_path = os.path.join(current_path, element.name)
                    elif element.role == "file":
                        if required_ending == None or required_ending != None and element.name.endswith(
                                required_ending):
                            selected[0] = os.path.join(current_path, element.name)
                            selected[1] = element.name

            if self.b_cancel.update(mouse_events, offset=self.topleft_pos):
                return None

            if self.b_back.update(mouse_events, offset=self.topleft_pos):
                current_path = os.path.split(current_path)[0]

            if self.b_open.update(mouse_events, offset=self.topleft_pos):
                if selected[0] != "":
                    return selected[0]
                else:
                    return None
            
            if required_ending != None and self.b_req_ending.update(mouse_events, offset=self.topleft_pos):
                self.messagebox.show_message(f"Required file ending: '{required_ending}'", False)

            # ? DRAWING ? #
            self.surface.fill(self.backgroundcolor1)

            # drawing on dir_surf
            for button in buttons_list:
                button.draw()
            self.surface.blit(dir_surf, (0, self.textsize-scroll))
            self.l_path.draw()
            self.b_back.draw()
            pygame.draw.rect(
                self.surface, (0, 0, 0),
                (0, self.textsize, self.dimensions[0],
                 self.dimensions[1] - self.textsize - int(self.textsize * 1.5)),
                1)

            # bottom part
            pygame.draw.rect(
                self.surface, self.backgroundcolor1,
                (0, self.dimensions[1] - int(self.textsize * 1.5),
                 self.dimensions[0],
                 int(self.textsize * 1.5)))
            pygame.draw.rect(
                self.surface, (0, 0, 0),
                (0, self.dimensions[1] - int(self.textsize * 1.5),
                 self.dimensions[0],
                 int(self.textsize * 1.5)),
                1)
            self.b_cancel.draw()
            self.l_selected.draw()
            self.l_selected_name.draw()
            self.b_open.draw()
            if required_ending != None:
                self.b_req_ending.draw()

            # at the end
            self.blitting_surface.blit(self.surface, self.topleft_pos)
            pygame.draw.rect(
                self.blitting_surface, (0, 0, 0),
                (self.topleft_pos[0] - 5, self.topleft_pos[1] - 5, self.dimensions[0] + 10, self.dimensions
                 [1] + 10),
                5, 1, 1, 1, 1)

            pygame.display.flip()
            self.pygame_clock.tick(self.fps)

    def ask_foldername(self, starting_path, dim_background: bool = True) -> str:
        raise Exception("not yet implemented")


class Messagebox:
    def __init__(
            self, surface, pygame_clock: pygame.time.Clock, fps: int, screen_center: tuple, textsize=25,
            textcolor: tuple = (0, 0, 0), backgroundcolor: tuple = (128, 128, 128)):
        self.surface = surface
        self.pygame_clock = pygame_clock
        self.fps = fps
        self.screen_center = screen_center
        self.textsize = textsize
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor

        assert fps >= 10
        assert 20 <= textsize <= 40
        assert type(textcolor) in [tuple, list]
        assert type(backgroundcolor) in [tuple, list]

    def askokcancel(self, text, dim_background=True):

        if dim_background:
            self.surface.fill([60 for i in range(3)], special_flags=pygame.BLEND_MULT)

        test = Label(self.surface, text, self.textsize, (0, 0), xad=25)
        width = min(max(test.background_rect.width, 294), 900)
        height = test.rect.height * 5

        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.screen_center

        surface = pygame.Surface((width, height))
        surface.fill(self.backgroundcolor)

        width = min(max(width, 100), 150)
        height = int(test.rect.height * 1.75)
        l_text = Label(self.surface, text, self.textsize, vect_sum(
            self.screen_center, (0, -5)), "midbottom", tc=self.textcolor)

        b_cancel_premade = Button(
            self.surface, "Cancel", self.textsize, vect_sum(rect.midbottom, (3, 0)),
            "bottomright", tc=self.textcolor, bgc=Colors.dark_red, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0))
        b_cancel = Button(
            self.surface, "Cancel", self.textsize, vect_sum(rect.midbottom, (3, 0)),
            "bottomright", tc=self.textcolor, bgc=Colors.dark_red, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0),
            aA=vect_sum(b_cancel_premade.rect, (3, 3, -6, -6)))

        b_ok_premade = Button(
            self.surface, "OK", self.textsize, vect_sum(rect.midbottom, (-3, 0)),
            "bottomleft", tc=self.textcolor, bgc=Colors.green, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0))
        b_ok = Button(
            self.surface, "OK", self.textsize, vect_sum(rect.midbottom, (-3, 0)),
            "bottomleft", tc=self.textcolor, bgc=Colors.green, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0),
            aA=vect_sum(b_ok_premade.rect, (3, 3, -6, -6)))

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

            if b_cancel.update(mouse_events):
                return False
            if b_ok.update(mouse_events):
                return True

            self.surface.blit(surface, rect)
            l_text.draw()
            b_cancel.draw()
            b_ok.draw()

            pygame.draw.rect(self.surface, (0, 0, 0), rect, 4, 1, 1, 1, 1)
            pygame.display.flip()
            self.pygame_clock.tick(self.fps)

    def show_message(self, text, dim_background=True, multiline=False):

        if dim_background:
            self.surface.fill([60 for i in range(3)], special_flags=pygame.BLEND_MULT)

        if multiline:
            test = Paragraph(self.surface, text, self.textsize, (0, 0), xad=25, yad=3)
            width = min(max(test.rect.width, 200), 800)
            height = test.rect.height + 100
        else:
            test = Label(self.surface, text, self.textsize, (0, 0), xad=25)
            width = min(max(test.rect.width, 200), 800)
            height = test.rect.height * 5

        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.screen_center

        surface = pygame.Surface((width, height))
        surface.fill(self.backgroundcolor)

        height = int(test.rect.height * 1.75)
        if multiline:
            lines = len([1 for char in text if char == "\n"])
            jump = self.textsize//2
            l_text = Paragraph(self.surface, text, self.textsize, vect_sum(
                self.screen_center, (0, -lines*jump)), "midbottom", tc=self.textcolor, yad=3)
        else:
            l_text = Label(self.surface, text, self.textsize, vect_sum(
                self.screen_center, (0, -5)), "midbottom", tc=self.textcolor)

        b_ok = Button(
            self.surface, "OK", self.textsize, vect_sum(rect.bottomright, (-10, -10)),
            "bottomright", tc=self.textcolor, bgc=Colors.green, hl=True, bR=1, xad=20, yad=6, to=(0,1),
            bw=4, br=1, bc=(0, 0, 0))

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            if b_ok.update(mouse_events):
                run = False

            self.surface.blit(surface, rect)
            l_text.draw()
            b_ok.draw()

            pygame.draw.rect(self.surface, (0, 0, 0), rect, 4, 1, 1, 1, 1)
            pygame.display.flip()
            self.pygame_clock.tick(self.fps)


class Entry(Button):
    def __init__(self, surface, text, size, xy: tuple, anchor="center", **kwargs):
        """
        Click to activate, click somewhere else to deactivate.
        If active, typed letters will appear on the widget.
        An indication, that the entry widget is active, has to
        be implemented externally (use self.get_state()).

        IMPORTANT:
            - The update method takes a complete event list as
              an input, while a regular button just needs a mouse event list.
            - Entries (unlike buttons) should NOT be updated in an if-statement!

        Additional keywords:
            max_chars / mc
                maximum number of characters
                Type: int
            text_when_empty / twe
                text that appears when there is currently no other content
                Type: str
            auto_style / ast
                if text_when_empty is set, this text will appear italic,
                while the real user input will appear in the regular font style
                IMPORTANT: this mechanic breaks if the style is set manually
                after the first initialization of the widget
                Type: bool
        """

        # max_chars
        self.max_chars = kwargs.get("max_chars", None)
        if self.max_chars == None:
            self.max_chars = kwargs.get("mc", None)
        # assertion
        if self.max_chars != None:
            assert type(self.max_chars) == int, f"invalid argument for 'max_chars': {self.max_chars}"
            assert self.max_chars >= 0, f"invalid argument for 'max_chars': {self.max_chars}"

        # text_when_empty
        self.text_when_empty = kwargs.get("text_when_empty", None)
        if self.text_when_empty == None:
            self.text_when_empty = kwargs.get("twe", None)
        if self.text_when_empty != None:
            self.text_when_empty = str(self.text_when_empty)
        # assertion not needed

        # auto_style
        self.auto_style = kwargs.get("auto_style", None)
        if self.auto_style == None:
            self.auto_style = kwargs.get("ast")
        if self.auto_style == None:
            self.auto_style = False
        # assertion
        assert type(self.auto_style) == bool, f"invalid argument for 'auto_style': {self.auto_style}"
        
        

        self.__state__ = False
        self.__force__ = False # used to set state even before the update method
        self.__permanent_state__ = None
        self.__value__ = str(text)
        self.__old_value__ = str(text)

        self.__keyboard__ = Keyboard()
        self.__keyboard__.set_forbidden_characters(["\t", "\n"])




        super().__init__(surface, text, size, xy, anchor, **kwargs)

        self.bold_init = self.bold
        self.italic_init = self.italic

    def update(self, event_list, button: int = 1, offset: tuple = (0, 0), do_highlight: bool = True) -> bool:
        """
        Checks if entry has been clicked on and activates widget if so.
        Should be used with a regular event_list.
        <button> can specify a certain button (1-3).
        Also updates the text, if input is detected.
        """
        assert type(button) == int, f"invalid argument for 'button': {button}"

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = list(event.pos)
                pos[0] += offset[0]
                pos[1] += offset[1]
                if button == None:
                    if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                        self.__state__ = True
                    else:
                        self.__state__ = False

                elif 0 < button < 4:
                    if button == event.button:
                        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                            self.__state__ = True
                        else:
                            self.__state__ = False

                else:
                    raise ValueError(f"invalid argument for 'button': {button}")

        if self.__permanent_state__ != None:
            self.__state__ = self.__permanent_state__

        if self.__force__ != None:
            self.__state__ = self.__force__
            self.__force__ = None

        if do_highlight and self.highlight != None:
            try:
                pos = list(pygame.mouse.get_pos())
                if self.active_area != None and not self.active_area.collidepoint(pos):
                    if self.backgroundcolor != self.backgroundcolor_init:
                        self.backgroundcolor = self.backgroundcolor_init
                pos[0] += offset[0]
                pos[1] += offset[1]
                if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                    # ? not needed here i think
                    if self.backgroundcolor != self.highlight:
                        self.backgroundcolor = self.highlight
                else:
                    if self.backgroundcolor != self.backgroundcolor_init:
                        self.backgroundcolor = self.backgroundcolor_init
            except:
                raise Exception(f"unable to change highlight button with color '{self.highlight}'")

        if self.__state__:
            for event in event_list:
                if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_BACKSPACE:
                    self.__value__ = self.__value__[:-1]
            if self.max_chars == None or (self.max_chars != None and len(self.__value__) < self.max_chars):
                self.__value__ += self.__keyboard__.get(event_list)

            if self.__value__ != self.__old_value__:
                self.update_text(self.__value__)
                self.__old_value__ = self.__value__

            if self.text_when_empty != None and len(self.__value__) == 0:
                self.update_text(self.text_when_empty)
                if self.auto_style:
                    self.set_style(italic=True)
            else:
                if self.auto_style:
                    self.set_style(self.bold_init, self.italic_init)

    def get_state(self):
        """
        Returns boolean whether the entry is active (True) or not (False).
        """
        return self.__state__

    def get(self):
        """
        Returns the text.
        """
        return self.__value__
    
    def set_forbidden_characters(self, characters: list):
        """
        Bans all given characters.
        """
        self.__keyboard__.set_forbidden_characters(characters)

    def clear(self):
        """
        Clears the text.
        """
        self.__value__ = ""
        self.__old_value__ = ""
        self.update_text(self.__value__)

    def set_state(self, state: bool):
        """
        Sets activity state.
        """
        self.__force__ = bool(state)

    def set_permanent_state(self, state: bool):
        """
        Sets activity state permanently. Remove with self.remove_permanent_state().
        """
        assert type(state) == bool, f"invalid argument for 'state': {state}"
        self.__permanent_state__ = state

    def remove_permanent_state(self):
        """
        Removes permanent state.
        """
        self.__permanent_state__ = None
        

class ScrollableButtonList:
    def __init__(
            self, surface, target_rect: tuple[int, int, int, int], scrolling_speed: int, backgroundcolor: tuple = (0,0,0)):
        """
        target_rect specifies the area in which buttons will be visible

        to update the buttons, use: 
            for b in self.get_buttons():
                if b.update(event_list, offset=self.get_offset()):
                    ...

        also, a general update every loop is needed:
            self.update(event_list)

        it is also possible to change the buttons:
            self.clear_buttons()
            self.add_buttons(list_of_button_names)

        IMPORTANT:
        this widget has to be drawn DIRECTLY to the screen, otherwise the clicking will be messed up.
        to check the active area, use self.get_rect() and draw it to the screen
        ALSO IMPORTANT:
        the buttons might not show up if the self.update method is not constantly called. to
        fix this, just call the method once with an emtpy list after initializing the class. (self.update([]))
        """

        # only vertical scroll
        # TODO: assertions
        assert type(surface) == pygame.Surface, f"invalid argument for 'surface': {surface}"
        self.__main_surface__ = surface
        assert type(target_rect) in [tuple, list, pygame.Rect]
        if type(target_rect) in [tuple, list]:
            assert len(target_rect) == 4, f"invalid argument for 'target_rect': {target_rect}"
        self.__target_rect__ = pygame.Rect(target_rect)
        self.__surface__ = pygame.Surface((self.__target_rect__.width, 0))

        assert type(scrolling_speed) == int, f"invalid argument for 'scrolling_speed': {scrolling_speed}"
        assert scrolling_speed > 0, f"invalid argument for 'scrolling_speed': {scrolling_speed}"
        self.__scrolling_speed__ = scrolling_speed

        assert type(backgroundcolor) in [tuple, list], f"invalid argument for 'backgroundcolor': {backgroundcolor}"
        assert len(backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {backgroundcolor}"
        self.__backgroundcolor__ = backgroundcolor        

        self.__scroll__ = 0
        self.__max_scroll__ = self.__surface__.get_height() - self.__target_rect__.height #! has to be reconfigured if anything changes

        self.__button_names__: list[str] = []
        self.__old_button_names__: list[str] = []
        self.__buttons__: list[Button] = []

        self.__int_surf__ = pygame.Surface((10, 10)) # internal surface

    def set_button_style(self, size: int, **kwargs):
        """ dont forget about the backgroundcolor and the height """
        try:
            Button(self.__int_surf__, "Test", size=size, xy=(0,0), anchor="topleft", **kwargs)
            self.__size__ = size
            kwargs["bR"] = 1 # important !
            kwargs["fw"] = self.__target_rect__.width
            kwargs["aA"] = self.__target_rect__
            self.__style__ = kwargs
        except Exception as e:
            raise e

    def add_button(self, button_name: str):
        self.__button_names__.append(str(button_name))

    def add_buttons(self, button_names: list[str]):
        for button in button_names:
            self.add_button(button)

    def clear_buttons(self):
        """ removes all buttons """
        self.__button_names__ = []
    
    def reset_scroll(self):
        """ resets the scroll value """
        self.__scroll__ = 0

    def set_buttons(self, button_names: list[str]):
        self.__button_names__ = []
        self.add_buttons(button_names)

    def update_surface(self):
        """ updates the surface if something has changed """

        if self.__old_button_names__ != self.__button_names__:
            self.__old_button_names__ = self.__button_names__[:]
            self.__buttons__ = []
            borderwidth = 0
            for count, name in enumerate(self.__button_names__):
                if count == 0:
                    self.__buttons__.append(
                        Button(self.__int_surf__, name, self.__size__, (0,0), "topleft", **self.__style__)
                    )
                    borderwidth = self.__buttons__[0].borderwidth
                else:
                    self.__buttons__.append(
                        Button(self.__int_surf__, name, self.__size__, (self.__buttons__[count-1].left, self.__buttons__[count-1].bottom-borderwidth), "topleft", **self.__style__)
                    )

            # determining the surface height
            if len(self.__buttons__) > 0:
                lowest = self.__buttons__[-1].bottom
            else:
                lowest = 0
            self.__surface__ = pygame.Surface((self.__target_rect__.width, lowest))
            
            self.__max_scroll__ = self.__surface__.get_height() - self.__target_rect__.height
            if self.__max_scroll__ > 0 and self.__scroll__ > self.__max_scroll__:
                self.__scroll__ = self.__max_scroll__
            elif self.__max_scroll__ <= 0:
                self.__scroll__ = 0

    def update_scroll(self, event_list):
        """ updates the scroll value """
        
        if self.__max_scroll__ > 0:
            for event in event_list:
                if event.type == pygame.MOUSEWHEEL:
                    self.__scroll__ = max(
                        min(self.__max_scroll__, self.__scroll__ + event.y*-1*self.__scrolling_speed__), 0)

    def update(self, event_list):
        """ updates surface and scroll """
        self.update_surface()
        self.update_scroll(event_list)

    def draw(self):
        self.__surface__.fill(self.__backgroundcolor__)
        for button in self.__buttons__:
            button.draw_to(self.__surface__)
        tr = self.__target_rect__
        pygame.draw.rect(self.__main_surface__, self.__backgroundcolor__, tr)
        if self.__surface__.get_height() > tr.height:
            self.__main_surface__.blit(self.__surface__.subsurface(
                (0, self.__scroll__, tr[2], tr[3])), self.__target_rect__.topleft)
        else:
            self.__main_surface__.blit(self.__surface__, self.__target_rect__.topleft)

    def get_buttons(self):
        return self.__buttons__

    def get_offset(self):
        return self.__target_rect__[0], self.__target_rect__[1] - self.__get_scroll__()

    def __get_scroll__(self):
        return self.__scroll__

    def get_rect(self):
        return self.__target_rect__


class OneClickManager:
    def __init__(self):
        self.clicked = False
        self.hovering = False

    def update(self):
        self.clicked = False
        self.hovering = False

    def get_clicked(self):
        return self.clicked

    def get_hovering(self):
        return self.hovering
    
    def set_clicked(self, status=True):
        self.clicked = bool(status)

    def set_hovering(self, status=True):
        self.hovering = bool(status)


class C:
    def __init__(self, *values, mo=False):
        """
        vector class - works very similar to c(...) in the language R
        automatically turns into a list if <mo> (="more_operations") is False,
        if True returns another C-class for further mathematical operations

        NOTE:
        if operations like +=, -=, ... are used, the object will
        always stay a C-class!
        """
        for value in values:
            assert (isinstance(value, int) or isinstance(value, float)), \
                f"values have to be int or float, received: '{value}' (type: {type(value)})"
        assert len(values) > 0, f"list of values can not be empty"

        self.__value = list(values)
        self.__more_operations = bool(mo)

    def __repr__(self):
        return self.__value

    def __round__(self, ndigits=0):
        self.round(ndigits)
        return self

    def round(self, decimals=0):
        assert isinstance(decimals, int), f"invalid argument for 'decimals': {decimals}"
        multiplier = 10 ** decimals
        if decimals == 0:
            for i in range(len(self.__value)):
                self.__value[i] = int(math.floor(self.__value[i]*multiplier + 0.5) / multiplier)
        else:
            for i in range(len(self.__value)):
                self.__value[i] = math.floor(self.__value[i]*multiplier + 0.5) / multiplier

    def __add__(self, other):
        if self.__more_operations:
            return C(*[v + other for v in self.__value])
        else:
            return [v + other for v in self.__value]

    def __iadd__(self, other):
        self.__value = [v + other for v in self.__value]
        return self

    def __sub__(self, other):
        if self.__more_operations:
            return C(*[v - other for v in self.__value])
        else:
            return [v - other for v in self.__value]

    def __isub__(self, other):
        self.__value = [v - other for v in self.__value]
        return self

    def __mul__(self, other):
        if self.__more_operations:
            return C(*[v * other for v in self.__value])
        else:
            return [v * other for v in self.__value]

    def __imul__(self, other):
        self.__value = [v * other for v in self.__value]
        return self

    def __truediv__(self, other):
        if self.__more_operations:
            return C(*[v / other for v in self.__value])
        else:
            return [v / other for v in self.__value]

    def __itruediv__(self, other):
        self.__value = [v / other for v in self.__value]
        return self

    def __floordiv__(self, other):
        if self.__more_operations:
            return C(*[v // other for v in self.__value])
        else:
            return [v // other for v in self.__value]

    def __ifloordiv__(self, other):
        self.__value = [v // other for v in self.__value]
        return self

    def __iter__(self):
        self.__count = 0
        self.__max = len(self.__value)
        return self

    def __next__(self):
        if self.__count < self.__max:
            v = self.__value[self.__count]
            self.__count += 1
            return v
        else:
            raise StopIteration

    def __len__(self):
        return len(self.__value)

    def value(self):
        return self.__value


class Function:
    def __init__(self, min_: int = 0, max_: int = 1, function_variable: str = "x"):
        """ scales everything to a function between min_ and max_ (on the y axis) """
        self.__min = min_
        self.__max = max_
        self.__function_variable = function_variable
        self.__length = 0
        self.__funcs = [
            # every func except last:
                # [from (including), to (excluding), f_from, f_to, func, x_dist, y_dist]
            # last func:
                # [from (including), to (including), f_from, f_to, func, x_dist, y_dist]
        ]

        assert isinstance(function_variable, str) and function_variable.isalpha(), \
            f"invalid argument for 'function_variable': {function_variable}"
        
        self.__val_before = None
        self.__val_after = None

    def add_const(self, constant: float, length: float = 1):
        """ add a constant value """
        assert length > 0, f"<length> as to be greater than 0"
        assert isinstance(constant, float) or isinstance(constant, int), f"invalid argument for 'constant': {constant}"
        self.__funcs.append(
            {
                # i_... = internal_... -> regarding the internal function that is being constructed
                # f_... = function_... -> regarding the function that is given by <func>
                "value": constant,
                "i_from": self.__length,
                "i_to": self.__length + length,
                "is_constant": True,
            }
        )
        self.__length += length

    def add_func(self, func: str, f_from: float, f_to: float, length: float = 1, start_at = "min"):
        """ use the <function_variable> (by default 'x'), eg. '-x**2'; use 'math.' for the math library;
        <start_at> can be either 'min' or 'max' """

        assert isinstance(eval(func, {self.__function_variable: 0, "math": math}), int) or \
            isinstance(eval(func, {self.__function_variable: 0, "math": math}), float), \
                f"invalid argument for 'func': {func} | error: does not return integer or float"
        assert f_from < f_to, f"<f_from> can not be greater than or equal to <f_to>"
        assert length > 0, f"<length> as to be greater than 0"
        assert start_at in ("min", "max"), f"invalid argument for 'start_at': {start_at}"
        # assert (start_at in ["min", "max"] or isinstance(start_at, int) or isinstance(start_at, float)), \
        #     f"invalid argument for 'start_at': {start_at}"
        self.__funcs.append(
            {
                # i_... = internal_... -> regarding the internal function that is being constructed
                # f_... = function_... -> regarding the function that is given by <func>
                "func": func,
                "i_from": self.__length,
                "i_to": self.__length + length,
                "i_xdist": length,
                "i_ydist": self.__max - self.__min,
                "f_from": f_from,
                "f_to": f_to,
                "f_xdist": f_to - f_from,
                "f_ydist": abs(eval(func, {"x":f_to, "math": math}) - eval(func, {"x":f_from, "math": math})),
                "start_at": start_at,
                "is_constant": False,
            }
        )
        self.__length += length

    def __round_half_up(self, n, decimals):
        if isinstance(n, int):
            return n
        multiplier = 10 ** decimals
        if decimals == 0:
            return int(math.floor(n*multiplier + 0.5) / multiplier)
        else:
            return math.floor(n*multiplier + 0.5) / multiplier

    def get(self, x, decimals=None):
        """ return the value of the function at <x> """

        if not 0 <= x <= self.__length:
            if self.__val_before is not None and x < 0:
                return self.__val_before
            elif self.__val_after is not None and x > self.__length:
                return self.__val_after
            else:   
                raise ValueError(f"<x> is out of range! Function length: {self.__length}")
        
        # finding the correct function (setting to 'f')
        for count, func in enumerate(self.__funcs):

            # if last function
            if count == len(self.__funcs)-1:
                if func["i_from"] <= x <= func["i_to"]:
                    f = func
                    break

            # every function but the last
            else:
                if func["i_from"] <= x < func["i_to"]:
                    f = func
                    break
        


        # now we have 'f' as the correct function
        if f["is_constant"] == False:
            actual_x = x - func["i_from"]
            percent = actual_x / func["i_xdist"]

            new_x_dist = func["f_xdist"]
            filling = percent * new_x_dist
            f_x = func["f_from"] + filling


            y_val = eval(f["func"],  
                {self.__function_variable: f_x, "math": math})

            y_min = eval(f["func"],
                {self.__function_variable: func["f_from"], "math": math})    
            y_max = eval(f["func"],
                {self.__function_variable: func["f_to"], "math": math})
            g = abs(y_max - y_min)
            a = y_val - y_min
            factor = a/g

            if f["start_at"] == "min":
                start = self.__min
                end = self.__max
            elif f["start_at"] == "max":
                start = self.__max
                end = self.__min
            # else:
            #     start = f["start_at"]


            filling = factor * abs(end - start)
            value = start + filling
        
        elif f["is_constant"] == True:
            value = f["value"]

        if decimals != None:
            return self.__round_half_up(value, decimals)
        else:
            return value

    def set_outer_values(self, value_before: float, value_after: float):
        assert isinstance(value_before, int) or isinstance(value_before, float), f"invalid argument for 'value_before': {value_before}"
        assert isinstance(value_after, int) or isinstance(value_after, float), f"invalid argument for 'value_after': {value_after}"
        self.__val_before = value_before
        self.__val_after = value_after

    def show(self, show_every_value = False):
        """ display the current function in a window """

        if self.__length == 0:
            raise Exception("Can not draw function because the length is zero.")

        # creating the dots # ! improvement needed # TODO
        dots = []
        dots_count = 200
        step = self.__length / dots_count
        x = 0
        while x <= self.__length:
            dots.append(
                (x, self.get(x))
            )
            x += step

        d_min = min([d[1] for d in dots])
        d_max = max([d[1] for d in dots])

        if show_every_value:
            MIN = d_min
            MAX = d_max
        else:
            MIN = self.__min
            MAX = self.__max
        

        pygame.init()
        screen = pygame.display.set_mode((900,500))
        fpsclock = pygame.time.Clock()
        fps = 60

        col = [160 for i in range(3)]

        l_y_max = Label(screen, self.__round_half_up(MAX, 2), 20, (50,50), "midright", xad=10, tc=col)
        l_y_min = Label(screen, self.__round_half_up(MIN, 2), 20, (50,450), "midright", xad=10, tc=col)
        l_y_max.draw()
        l_y_min.draw()

        # if show_every_value: also draw self.__min and self.__max marks
        if show_every_value:
            l_mark_max_percent = (self.__max - MIN) / (MAX - MIN)
            l_mark_max_height = 450 - 400*l_mark_max_percent
            if self.__max != MAX:
                l_y_max_mark = Label(screen, self.__round_half_up(self.__max, 3), 20, (50,l_mark_max_height), "midright", xad=10, tc=col)
                l_y_max_mark.draw()
            
            l_mark_min_percent = (self.__min - MIN) / (MAX - MIN)
            l_mark_min_height = 450 - 400*l_mark_min_percent
            if self.__min != MIN:
                l_y_min_mark = Label(screen, self.__round_half_up(self.__min, 3), 20, (50,l_mark_min_height), "midright", xad=10, tc=col)
                l_y_min_mark.draw()
            

        l_x_min = Label(screen, 0, 20, (50,450), "midtop", yad=10, tc=col)
        l_x_max = Label(screen, self.__length, 20, (850,450), "midtop", yad=10, tc=col)
        l_x_min.draw()
        l_x_max.draw()

        # drawing the lines
        pygame.draw.line(screen, col, (50,50), (50,450), 1)
        if show_every_value:
            pygame.draw.line(screen, (255,0,0), (50,l_mark_max_height), (850,l_mark_max_height), 1)
            pygame.draw.line(screen, (255,0,0), (50,l_mark_min_height), (850,l_mark_min_height), 1)
        else:
            pygame.draw.line(screen, (255,0,0), (50,450), (850,450), 1)
            pygame.draw.line(screen, (255,0,0), (50,50), (850,50), 1)

        # drawing the dots
        for dot in dots:
            min_percent = (self.__min - MIN) / (MAX - MIN)
            min_height = 400*min_percent
            pygame.draw.circle(screen, (0,0,255), (50+dot[0]*(800/self.__length), 450-min_height-dot[1]*(400/(MAX-MIN))), 2)
        
        incr_size_img = pygame.image.load(r"C:\Users\marce\Desktop\gamedev_stuff\buttons\increase_size.png")
        incr_size_img.set_colorkey((255,255,255))
        decr_size_img = pygame.image.load(r"C:\Users\marce\Desktop\gamedev_stuff\buttons\decrease_size.png")
        decr_size_img.set_colorkey((255,255,255))

        if show_every_value:
            button = Button(screen, "", 10, (22,22), "center", fd=(32,32), img=decr_size_img)
        else:
            button = Button(screen, "", 10, (22,22), "center", fd=(32,32), img=incr_size_img)
        button.draw()

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

            if button.update(event_list):
                self.show(not show_every_value)
            
            pygame.display.flip()
            fpsclock.tick(fps)
        
    def reset(self):
        """ deletes all previously added functions """
        self.__length = 0
        self.__funcs = []

    def example_function(self):
        """ show the example function """
        self.__min = 0
        self.__max = 1
        self.__function_variable = "x"
        self.__length = 0
        self.__funcs = []
        self.add_func("(-math.sin(x*3))/math.cos(x/2)", 0.5, 4.5, 10)
        print("Function: (-math.sin(x*3))/math.cos(x/2)")
        self.show()

