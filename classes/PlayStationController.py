import pygame
import math
from Pygame_Engine.classes.Functions import round_half_up

class PlayStationController:
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
