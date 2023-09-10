import sys
import math
import pygame
from ..classes.OneClickManager import OneClickManager

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
                Type: pygame.Surface
            text
                the text displayed on the label / button
                Type: Any
            size
                refers to the size of text in pixels
                Type: int
            xy
                refers to the position of the anchor
                Type:
                    tuple[int, int]
                    tuple[tuple[int, int], tuple[int, int]] -> performs sum of vectors (v1[0] + v2[0], v1[1] + v2[1])
                    list[...]
                    list[list[...]]
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
            stay_within_surface # TODO (not implemented yet)
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
            padding (NOT IMPLEMENTED YET)
                decreases the size of the widget without affecting the position
                Type: int

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
            "bold": "bo",
            "italic": "it",
            "underline": "ul",
            "one_click_manager": "ocm",
            "template": "t",
            "padding": "p"
        }
        assert len(set(self.ABBREVIATIONS.values())) == len(list(self.ABBREVIATIONS.values())), "it seems like two arguments share the same abbreviation"

        self.__errors = []

        # inserting template (if exists)
        template = kwargs.get("template", None)
        if template is None:
            template = kwargs.get(self.ABBREVIATIONS["template"], None)
        if template is not None:
            self.__test_type("template", template, dict)
            for k in template.keys():
                if not k in kwargs.keys():
                    kwargs[k] = template[k]

        self.__is_touching__ = False # if cursor is touching the rect, only for buttons
        self.__has_hl_image__ = False

        self.surface = surface
        self.text = str(text)

        self.size = size
        self.__test_type("size", size, (int, float))
        self.size = int(self.size)

        self.__test_type("xy", xy, (tuple, list))
        self.__test_len("xy", xy, "=", 2)
        try:
            if isinstance(xy[0], (int, float)) and isinstance(xy[1], (int, float)):
                self.xy = int(xy[0]), int(xy[1])
            elif isinstance(xy[0], (tuple, list)) and isinstance(xy[1], (tuple, list)):
                t1 = xy[0]
                t2 = xy[1]
                self.__test_len("xy", t1, "=", 2)
                self.__test_len("xy", t1, "=", 2)
                self.__test_type("xy", t1[0], (int, float))
                self.__test_type("xy", t1[1], (int, float))
                self.__test_type("xy", t2[0], (int, float))
                self.__test_type("xy", t2[1], (int, float))
                self.xy = (int(t1[0] + t2[0]), int(t1[1] + t2[1]))
            else:
                self.__collect_error("xy", self.xy)
        except:
            self.__collect_error("xy", self.xy)

        self.anchor = anchor
        if "anchor" in kwargs.keys():
            self.anchor = kwargs["anchor"]
        self.__test_match("anchor", self.anchor, "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(","))

        kw = kwargs

        # textcolor
        self.textcolor = kw.get("textcolor", None)
        if self.textcolor == None:
            self.textcolor = kw.get(self.ABBREVIATIONS["textcolor"], None)
        if self.textcolor == None:
            self.textcolor = (0,0,0)
        # assertion
        if self.textcolor != None:
            self.__test_type("textcolor", self.textcolor, (tuple, list))
            self.__test_len("textcolor", self.textcolor, "=", 3)

        # backgroundcolor
        self.backgroundcolor = kw.get("backgroundcolor", None)
        if self.backgroundcolor == None:
            self.backgroundcolor = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion
        if self.backgroundcolor != None:
            self.__test_type("backgroundcolor", self.backgroundcolor, (tuple, list))
            self.__test_len("backgroundcolor", self.backgroundcolor, "=", 3)

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
        self.antialias = bool(self.antialias)

        # font
        self.font = kw.get("font", None)
        if self.font == None:
            self.font = kw.get(self.ABBREVIATIONS["font"], None)
        if self.font == None:
            self.font = ""
        # assertion
        if self.font != None:
            self.__test_type("font", self.font, str)

        # x_axis_addition
        self.x_axis_addition = kw.get("x_axis_addition", None)
        if self.x_axis_addition == None:
            self.x_axis_addition = kw.get(self.ABBREVIATIONS["x_axis_addition"], None)
        if self.x_axis_addition == None:
            self.x_axis_addition = 0
        # assertion
        if self.x_axis_addition != None:
            self.__test_type("x_axis_addition", self.x_axis_addition, int)
            self.__test_value("x_axis_addition", self.x_axis_addition, ">=", 0)

        # y_axis_addition
        self.y_axis_addition = kw.get("y_axis_addition", None)
        if self.y_axis_addition == None:
            self.y_axis_addition = kw.get(self.ABBREVIATIONS["y_axis_addition"], None)
        if self.y_axis_addition == None:
            self.y_axis_addition = 0
        # assertion
        if self.y_axis_addition != None:
            self.__test_type("y_axis_addition", self.y_axis_addition, int)
            self.__test_value("y_axis_addition", self.y_axis_addition, ">=", 0)

        # borderwidth
        self.borderwidth = kw.get("borderwidth", None)
        if self.borderwidth == None:
            self.borderwidth = kw.get(self.ABBREVIATIONS["borderwidth"], None)
        if self.borderwidth == None:
            self.borderwidth = 0
        # assertion
        if self.borderwidth != None:
            self.__test_type("borderwidth", self.borderwidth, int)
            self.__test_value("borderwidth", self.borderwidth, ">=", 0)

        # bordercolor
        self.bordercolor = kw.get("bordercolor", None)
        if self.bordercolor == None:
            self.bordercolor = kw.get(self.ABBREVIATIONS["bordercolor"], None)
        if self.bordercolor == None:
            self.bordercolor = (0, 0, 0)
        # assertion
        if self.bordercolor != None:
            self.__test_type("bordercolor", self.bordercolor, (tuple, list))
            self.__test_len("bordercolor", self.bordercolor, "=", 3)

        # force_width
        self.force_width = kw.get("force_width", None)
        if self.force_width == None:
            self.force_width = kw.get(self.ABBREVIATIONS["force_width"], None)
        # assertion
        if self.force_width != None:
            self.__test_type("force_width", self.force_width, int)
            self.__test_value("force_width", self.force_width, ">", 0)

        # force_height
        self.force_height = kw.get("force_height", None)
        if self.force_height == None:
            self.force_height = kw.get(self.ABBREVIATIONS["force_height"], None)
        # assertion
        if self.force_height != None:
            self.__test_type("force_height", self.force_height, int)
            self.__test_value("force_height", self.force_height, ">", 0)

        # force_dim
        force_dim = kw.get("force_dim", None)
        if force_dim == None:
            force_dim = kw.get(self.ABBREVIATIONS["force_dim"], None)
        # assertion
        if force_dim != None:
            self.__test_type("force_dim", force_dim, (tuple, list))
            self.__test_len("force_dim", force_dim, "=", 2)
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
        self.__test_match("binding_rect", self.binding_rect, (0, 1))

        # borderradius
        self.borderradius = kw.get("borderradius", None)
        if self.borderradius == None:
            self.borderradius = kw.get(self.ABBREVIATIONS["borderradius"], None)
        if self.borderradius == None:
            self.borderradius = (1, 1, 1, 1)
        # assertion
        elif type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) in [tuple, list]:
            self.__test_len("borderradius", self.borderradius, "=", 4)
        else:
            self.__collect_error("borderradius", self.borderradius)

        # text_offset
        self.text_offset = kw.get("text_offset", None)
        if self.text_offset == None:
            self.text_offset = kw.get(self.ABBREVIATIONS["text_offset"], None)
        if self.text_offset == None:
            self.text_offset = (0, 0)
        # assertion
        if self.text_offset != None:
            self.__test_type("text_offset", self.text_offset, (tuple, list))
            self.__test_len("text_offset", self.text_offset, "=", 2)

        # image
        self.image = kw.get("image", None)
        if self.image == None:
            self.image = kw.get(self.ABBREVIATIONS["image"], None)
        # assertion
        if self.image != None:
            self.__test_type("image", self.image, pygame.Surface)
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
            self.__test_match("text_binding", self.text_binding, "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(","))

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
                    if not self.backgroundcolor != None:
                        self.__collect_error_directly(f"'backgroundcolor' (currently: {self.backgroundcolor}) must be defined when using 'highlight' (currently: {self.highlight})")
            else:
                self.__collect_error("highlight", self.highlight)

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
            self.__test_type("active_area", self.active_area, (tuple, list, pygame.Rect))
            self.__test_len("active_area", self.active_area, "=", 4)
            self.active_area = pygame.Rect(self.active_area)

        # bold
        self.bold = kw.get("bold", None)
        if self.bold == None:
            self.bold = kw.get(self.ABBREVIATIONS["bold"], None)
        if self.bold == None:
            self.bold = False
        # assertion
        self.bold = bool(self.bold)

        # italic
        self.italic = kw.get("italic", None)
        if self.italic == None:
            self.italic = kw.get(self.ABBREVIATIONS["italic"], None)
        if self.italic == None:
            self.italic = False
        # assertion
        self.italic = bool(self.italic)

        # underline
        self.underline = kw.get("underline", None)
        if self.underline == None:
            self.underline = kw.get(self.ABBREVIATIONS["underline"], None)
        if self.underline == None:
            self.underline = False
        # assertion
        self.underline = bool(self.underline)

        # one_click_manager
        self.one_click_manager = kw.get("one_click_manager", None)
        if self.one_click_manager == None:
            self.one_click_manager = kw.get(self.ABBREVIATIONS["one_click_manager"], None)
        # assertion
        if self.one_click_manager != None:
            self.__test_type("one_click_manager", self.one_click_manager, OneClickManager)

        # padding
        self.padding = kw.get("padding", None)
        if self.padding == None:
            self.padding = kw.get(self.ABBREVIATIONS["padding"], None)
        if self.padding == None:
            self.padding = 0
        # assertion
        if self.padding != None:
            self.__test_type("padding", self.padding, int)
            self.__test_value("padding", self.padding, ">=", 0)

        self.__create__()

    def __create__(self):
        self.__show_errors()

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
        else:
            w = self.force_width

        if self.force_height == None:
            pass
        else:
            h = self.force_height

        # creating the background rect
        self.background_rect = pygame.Rect(sx, sy, w, h)

        # putting everything in correct position
        self.update_pos(self.xy, self.anchor)

    def __test_type(self, variable_name, variable_value, applicable_types: tuple):
        try:
            if not isinstance(variable_value, applicable_types):
                self.__collect_error(variable_name, variable_value)
        except:
            self.__collect_generic_error(variable_name, variable_value)

    def __test_len(self, variable_name, variable_value, _type: str, value):
        assert _type in ">,<,=,>=,<=".split(",")
        try:
            if _type == "<" and not len(variable_value) < value or \
               _type == "<=" and not len(variable_value) <= value or \
               _type == ">" and not len(variable_value) > value or \
               _type == ">=" and not len(variable_value) >= value or \
               _type == "=" and not len(variable_value) == value:
                self.__collect_error(variable_name, variable_value)
        except:
            self.__collect_generic_error(variable_name, variable_value)

    def __test_value(self, variable_name, variable_value, _type: str, value):
        assert _type in ">,<,=,>=,<=".split(",")
        try:
            if _type == "<" and not variable_value < value or \
               _type == "<=" and not variable_value <= value or \
               _type == ">" and not variable_value > value or \
               _type == ">=" and not variable_value >= value or \
               _type == "=" and not variable_value == value:
                self.__collect_error(variable_name, variable_value)
        except:
            self.__collect_generic_error(variable_name, variable_value)

    def __test_match(self, variable_name, variable_value, applicable_values: tuple):
        assert isinstance(applicable_values, (tuple, list))
        if not variable_value in applicable_values:
            self.__collect_error(variable_name, variable_value)

    def __format_error(self, variable_name, variable_value):
        return f"invalid argument for '{variable_name}': {variable_value} ({type(variable_value)})"
    
    def __format_generic_error(self, variable_name, variable_value):
        return f"generic error for '{variable_name}': {variable_value} ({type(variable_value)})"

    def __collect_error(self, variable_name, variable_value):
        error = self.__format_error(variable_name, variable_value)
        if error not in self.__errors:
            self.__errors.append(
                error
            )

    def __collect_generic_error(self, variable_name, variable_value):
        error = self.__format_generic_error(variable_name, variable_value)
        if error not in self.__errors:
            self.__errors.append(
                error
            )

    def __collect_error_directly(self, error):
        self.__errors.append(
            error
        )

    def __show_errors(self):
        if len(self.__errors) == 0:
            return
        
        longest_line = 0
        for line in self.__errors:
            longest_line = max(len(line), longest_line)

        char = "#"
        side = [3, 2] # [char, " "]

        def print_solid_line():
            print(char * (longest_line + side[0] * 2 + side[1] * 2))

        def print_empty_line():
            print(char * side[0] + " " * (longest_line + side[1] * 2) + char * side[0])

        def print_text_line(text):
            print(char * side[0] + " " * side[1] + text + " " * (longest_line - len(text)) + " " * side[1] + char * side[0])

        def print_text_line_centered(text):
            print(char * side[0] + " " * side[1] + " " * math.floor((longest_line - len(text)) / 2) + text + " " * math.ceil((longest_line - len(text)) / 2) + " " * side[1] + char * side[0])


        print_solid_line()
        print_empty_line()
        print_text_line_centered("INVALID ARGUMENT INPUT FOR WIDGET")
        print_text_line_centered("(TEXT: " + self.text + ")")
        print_empty_line()
        for error in self.__errors:
            print_text_line(error)
        print_empty_line()
        print_solid_line()

        raise Exception("An error occurred. See terminal output for more details.")

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
        assert type(surface) == pygame.Surface, self.__format_error("surface", surface)

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
            if not type(textcolor) in [
                tuple, list]: self.__collect_error("textcolor", textcolor)
            if not len(textcolor) == 3: self.__collect_error("textcolor", textcolor)
            self.textcolor = textcolor
            self.__create__()
        if backgroundcolor != None and backgroundcolor != self.backgroundcolor:
            if not type(backgroundcolor) in [
                tuple, list]: self.__collect_error("backgroundcolor", backgroundcolor)
            if not len(
                backgroundcolor) == 3: self.__collect_error("backgroundcolor", backgroundcolor)
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
            if not type(bordercolor) in [
                tuple, list]: self.__collect_error("bordercolor", bordercolor)
            if not len(bordercolor) == 3: self.__collect_error("bordercolor", bordercolor)
            self.bordercolor = bordercolor

    def update_borderwidth(self, borderwidth: int):
        """
        Updates the borderwidth of the widget. Call
        this method before drawing to the screen.
        """
        if not type(borderwidth) == int: self.__collect_error("borderwidth", borderwidth)
        if not borderwidth >= 0: self.__collect_error("borderwidth", borderwidth)
        self.borderwidth = borderwidth

    def update_pos(self, xy, anchor=None):
        """
        Changes the widgets position. Call this
        method before drawing to the screen.
        """
        if not isinstance(xy, (tuple, list)): self.__collect_error("xy", xy)
        if not len(xy) == 2: self.__collect_error("xy", xy)
        self.xy = xy
        if not anchor in ["topleft", "topright", "bottomleft", "bottomright",
                                   "center", "midtop", "midright", "midbottom", "midleft", None]:
            self.__collect_error("anchor", anchor)
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
    
    def set_style(self, bold: bool = None, italic: bool = None, underline: bool = None):
        old_bold = self.bold
        if bold != None:
            self.bold = bool(bold)
        old_italic = self.italic
        if italic != None:
            self.italic = bool(italic)
        old_underline = self.underline
        if underline != None:
            self.underline = bool(underline)
        if old_bold != self.bold or old_italic != self.italic or old_underline != self.underline:
            self.__create__()

    def get_rect(self) -> pygame.Rect:
        return self.rect
