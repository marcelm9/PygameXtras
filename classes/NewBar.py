import pygame

class NewBar:
    def __init__(self, surface, width_height: tuple, xy: tuple, anchor="center", **kwargs):
        """
        Creates a bar.

        Instructions:
            - To create a label, create an instance of this class before
            the mainloop of the game.
            - To make the label appear, call the method 'self.draw()' in
            every loop of the game.
            - To update the fill percentage of the bar, call the
            self.update() method before drawing to the screen.

        Example (simplified):
            bar = Bar(screen, (100, 20), (100, 100))
            health = 20
            max_health = 100
            while True:
                bar.update(health, max_health)
                bar.draw()

        Arguments:
            surface
                the surface the object will be drawn onto
                Type: pygame.Surface, pygame.display.set_mode
            width_height
                specifies the width / height of the bar
                Type: tuple, list
            xy
                refers to the position of the anchor
                Type: tuple, list
            anchor
                the anchor of the object:   topleft,    midtop,    topright,
                                            midleft,    center,    midright,
                                            bottomleft, midbottom, bottomright
                Type: str
            backgroundcolor
                color of the background in rgb
                Type: None, tuple, list
            fillcolor
                color of the filling
                Type: tuple, list
            bordercolor
                color of the border
                Type: tuple, list
            borderwidth
                width of the border
                Type: int
            borderradius
                used to round the corners of the background_rect; use int for all corners or other types for individual corners
                Type: int, tuple, list
            info
                can store any kind of data; usage of dict recommended
                Type: Any
            fill_start
                from which side of the bar to start filling: left (default), right, top, bottom
                Type: str

        All custom arguments can also be used in their short form (eg. "aa" instead of "antialias").
        To see what all the short forms look like, inspect the self.ABBREVIATIONS attribute.
        """

        self.ABBREVIATIONS = {
            "backgroundcolor": "bgc",
            "fillcolor": "fc",
            "bordercolor": "bc",
            "borderwidth": "bw",
            "borderradius": "br",
            "info": "info",
            "fill_start": "fs"
        }

        self.__surface = surface
        self.__width_height = width_height
        self.__xy = xy
        self.__anchor = anchor

        # backgroundcolor
        self.backgroundcolor = kwargs.get("backgroundcolor", None)
        if self.backgroundcolor == None:
            self.backgroundcolor = kwargs.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion
        assert isinstance(self.backgroundcolor, (None, tuple, list)), f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"

        # fillcolor
        self.fillcolor = kwargs.get("fillcolor", None)
        if self.fillcolor == None:
            self.fillcolor = kwargs.get(self.ABBREVIATIONS["fillcolor"], None)
        # assertion
        assert isinstance(self.fillcolor, (tuple, list)),f"invalid argument for 'fillcolor': {self.fillcolor}"

        # bordercolor
        self.bordercolor = kwargs.get("bordercolor", None)
        if self.bordercolor == None:
            self.bordercolor = kwargs.get(self.ABBREVIATIONS["bordercolor"], None)
        # assertion
        assert isinstance(self.bordercolor, (None, tuple, list)), f"invalid argument for 'bordercolor': {self.bordercolor}"

        # borderwidth
        self.borderwidth = kwargs.get("borderwidth", None)
        if self.borderwidth == None:
            self.borderwidth = kwargs.get(self.ABBREVIATIONS["borderwidth"], None)
        # assertion
        assert isinstance(self.borderwidth, int), f"invalid argument for 'borderwidth': {self.borderwidth}"

        # borderradius
        self.borderradius = kwargs.get("borderradius", None)
        if self.borderradius == None:
            self.borderradius = kwargs.get(self.ABBREVIATIONS["borderradius"], None)
        # assertion
        assert isinstance(self.borderradius, int) or (isinstance(self.borderradius, (tuple, list)) and len(self.borderradius) == 4), f"ininvalid argument for 'borderradius': {self.borderradius}"
        
        
