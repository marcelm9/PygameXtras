from ..classes.Label import Label

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
