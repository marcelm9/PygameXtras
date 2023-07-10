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
        if isinstance(xy[0], (int, float)) and isinstance(xy[1], (int, float)):
            self.xy = int(xy[0]), int(xy[1])
        elif isinstance(xy[0], (tuple, list)) and isinstance(xy[1], (tuple, list)):
            t1 = xy[0]
            t2 = xy[1]
            assert all([
                len(t1) == 2,
                len(t2) == 2,
                isinstance(t1[0], int),
                isinstance(t1[1], int),
                isinstance(t2[0], int),
                isinstance(t2[1], int)
            ]), f"invalid argument for 'xy': {xy}"
            self.xy = (t1[0] + t2[0], t1[1] + t2[1])
        else:
            raise AssertionError(f"invalid argument for 'xy': {xy}")

        assert anchor in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
            ","), f"invalid argument for 'anchor': {anchor}"
        self.anchor = anchor

        kw = kwargs

        # textcolor
        self.textcolor = kw.get("textcolor", None)
        if self.textcolor == None:
            self.textcolor = kw.get(self.ABBREVIATIONS["textcolor"], None)
        if self.textcolor == None:
            self.textcolor = (0,0,0)
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
        assert isinstance(xy, (tuple, list)), f"invalid argument for 'xy': {xy}"
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

    def get_rect(self):
        return self.rect
