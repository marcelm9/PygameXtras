import pygame
from ..classes.Button import Button
from ..classes.Keyboard import Keyboard

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
            strict_input / si
                only allow numeric ("int", "float") or alphabetic ("str") input
                Type: str
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
            self.auto_style = kwargs.get("ast", None)
        if self.auto_style == None:
            self.auto_style = False
        # assertion
        assert type(self.auto_style) == bool, f"invalid argument for 'auto_style': {self.auto_style}"

        # strict_input
        self.strict_input = kwargs.get("strict_input", None)
        if self.strict_input == None:
            self.strict_input = kwargs.get("si", None)
        # assertion
        assert self.strict_input is None or self.strict_input in ["int", "float", "str"], f"invalid argument for 'strict_input': {self.strict_input}"
        
        

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

    def update(self, event_list, button: int = 1, offset: tuple = (0, 0)) -> bool:
        """
        Checks if entry has been clicked on and activates widget if so.
        Should be used with a regular event_list.
        <button> can specify a certain button (1-3).
        Also updates the text, if input is detected.
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
                        self.__state__ =  True
                    else:
                        self.__state__ = False

                elif 0 < button < 4:
                    if button == event.button:
                        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                            if self.one_click_manager != None:
                                self.one_click_manager.set_clicked()
                            self.__state__ =  True
                        else:
                            self.__state__ = False

                else:
                    raise ValueError(f"invalid argument for 'button': {button}")

        if self.__permanent_state__ != None:
            self.__state__ = self.__permanent_state__

        if self.__force__ != None:
            self.__state__ = self.__force__
            self.__force__ = None

        # managing the hovering (highlight)
        pos = list(pygame.mouse.get_pos())
        if self.active_area != None and not self.active_area.collidepoint(pos):
            self.__is_touching__ = False
            self.__state__ = False
        pos[0] -= offset[0]
        pos[1] -= offset[1]
        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
            if self.highlight != None:
                self.__is_touching__ = True
            if self.one_click_manager != None:
                self.one_click_manager.set_hovering()
        else:
            self.__is_touching__ = False

        if self.__state__:

            # deleting chars
            for event in event_list:
                # if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_BACKSPACE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.__value__ = self.__value__[:-1]

            # adding chars
            val = self.__keyboard__.get(event_list)
            new_val: str = self.__value__ + val

            # checks for self.strict_input and sets val to "" if condition does not apply
            if self.strict_input is not None and val != "":

                if new_val == "-":
                    self.__value__ = new_val
                elif new_val.startswith("-"):
                    if (self.strict_input == "int"     and new_val[1:].isnumeric()) or \
                       (self.strict_input == "float"   and "".join(new_val[1:].split(".", 1)).isnumeric()) or \
                       (self.strict_input == "str"     and new_val[1:].isalpha()):
                        self.__value__ = new_val
                else:
                    if (self.strict_input == "int"     and new_val.isnumeric()) or \
                       (self.strict_input == "float"   and "".join(new_val.split(".", 1)).isnumeric()) or \
                       (self.strict_input == "str"     and new_val.isalpha()):
                        self.__value__ = new_val
                        
            else:
                self.__value__ = new_val

            # dealing with self.max_chars
            if self.max_chars is not None:
                self.__value__ = self.__value__[:self.max_chars]

            if self.__value__ != self.__old_value__:
                self.__refresh_text()

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

    def set(self, value):
        """
        Sets the value of the Entry.
        """
        self.__value__ = str(value)
        self.__refresh_text()

    def set_forbidden_characters(self, characters: list):
        """
        Bans all given characters.
        """
        self.__keyboard__.set_forbidden_characters(characters)

    def set_forbidden_characters_for_filename(self):
        forbidden_chars_in_filenames = "<>:\"/\\|?* \n\t\r,.;"
        self.set_forbidden_characters(list(forbidden_chars_in_filenames))

    def clear(self):
        """
        Clears the text.
        """
        self.__value__ = ""
        self.__refresh_text()

    def set_state(self, state: bool):
        """
        Sets activity state.
        """
        self.__force__ = bool(state)

    def set_permanent_state(self, state: bool):
        """
        Sets activity state permanently. Remove with self.remove_permanent_state().
        """
        self.__permanent_state__ = bool(state)

    def remove_permanent_state(self):
        """
        Removes permanent state.
        """
        self.__permanent_state__ = None
    
    def __refresh_text(self):
        self.update_text(self.__value__)
        self.__old_value__ = self.__value__

