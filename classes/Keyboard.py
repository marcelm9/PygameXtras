import pygame

class Keyboard:
    def __init__(self):
        # self.keys = { #! somehow seems to be deprecated, leaving this here for some time (1.4.2023)
        #     pygame.locals.K_a: "a",
        #     pygame.locals.K_b: "b",
        #     pygame.locals.K_c: "c",
        #     pygame.locals.K_d: "d",
        #     pygame.locals.K_e: "e",
        #     pygame.locals.K_f: "f",
        #     pygame.locals.K_g: "g",
        #     pygame.locals.K_h: "h",
        #     pygame.locals.K_i: "i",
        #     pygame.locals.K_j: "j",
        #     pygame.locals.K_k: "k",
        #     pygame.locals.K_l: "l",
        #     pygame.locals.K_m: "m",
        #     pygame.locals.K_n: "n",
        #     pygame.locals.K_o: "o",
        #     pygame.locals.K_p: "p",
        #     pygame.locals.K_q: "q",
        #     pygame.locals.K_r: "r",
        #     pygame.locals.K_s: "s",
        #     pygame.locals.K_t: "t",
        #     pygame.locals.K_u: "u",
        #     pygame.locals.K_v: "v",
        #     pygame.locals.K_w: "w",
        #     pygame.locals.K_x: "x",
        #     pygame.locals.K_y: "y",
        #     pygame.locals.K_z: "z",
        #     pygame.locals.K_0: "0",
        #     pygame.locals.K_1: "1",
        #     pygame.locals.K_2: "2",
        #     pygame.locals.K_3: "3",
        #     pygame.locals.K_4: "4",
        #     pygame.locals.K_5: "5",
        #     pygame.locals.K_6: "6",
        #     pygame.locals.K_7: "7",
        #     pygame.locals.K_8: "8",
        #     pygame.locals.K_9: "9",
        #     pygame.locals.K_TAB: "\t",
        #     pygame.locals.K_SPACE: " ",
        #     pygame.locals.K_SEMICOLON: ";",
        #     pygame.locals.K_SLASH: "/",
        #     pygame.locals.K_RETURN: "\n",
        #     pygame.locals.K_PERIOD: ".",
        #     pygame.locals.K_PLUS: "+",
        #     pygame.locals.K_PERCENT: "%",
        #     pygame.locals.K_MINUS: "-",
        #     pygame.locals.K_HASH: "#",
        #     pygame.locals.K_UNDERSCORE: "_",
        #     pygame.locals.K_LEFTBRACKET: "(",
        #     pygame.locals.K_RIGHTBRACKET: ")",
        #     pygame.locals.K_LESS: "<",
        #     pygame.locals.K_GREATER: ">",
        #     pygame.locals.K_EQUALS: "=",
        #     pygame.locals.K_EURO: "€",
        #     pygame.locals.K_EXCLAIM: "!",
        #     pygame.locals.K_QUESTION: "?",
        #     pygame.locals.K_DOLLAR: "$",
        #     pygame.locals.K_COLON: ":",
        #     pygame.locals.K_COMMA: ",",
        #     pygame.locals.K_BACKSLASH: "\\",
        #     pygame.locals.K_ASTERISK: "*",
        # }
        # self.shift_keys = {
        #     pygame.locals.K_a: "A",
        #     pygame.locals.K_b: "B",
        #     pygame.locals.K_c: "C",
        #     pygame.locals.K_d: "D",
        #     pygame.locals.K_e: "E",
        #     pygame.locals.K_f: "F",
        #     pygame.locals.K_g: "G",
        #     pygame.locals.K_h: "H",
        #     pygame.locals.K_i: "I",
        #     pygame.locals.K_j: "J",
        #     pygame.locals.K_k: "K",
        #     pygame.locals.K_l: "L",
        #     pygame.locals.K_m: "M",
        #     pygame.locals.K_n: "N",
        #     pygame.locals.K_o: "O",
        #     pygame.locals.K_p: "P",
        #     pygame.locals.K_q: "Q",
        #     pygame.locals.K_r: "R",
        #     pygame.locals.K_s: "S",
        #     pygame.locals.K_t: "T",
        #     pygame.locals.K_u: "U",
        #     pygame.locals.K_v: "V",
        #     pygame.locals.K_w: "W",
        #     pygame.locals.K_x: "X",
        #     pygame.locals.K_y: "Y",
        #     pygame.locals.K_z: "Z",
        #     pygame.locals.K_0: "=",
        #     pygame.locals.K_1: "!",
        #     pygame.locals.K_2: "\"",
        #     pygame.locals.K_3: "§",
        #     pygame.locals.K_4: "$",
        #     pygame.locals.K_5: "%",
        #     pygame.locals.K_6: "&",
        #     pygame.locals.K_7: "/",
        #     pygame.locals.K_8: "(",
        #     pygame.locals.K_9: ")",
        #     pygame.locals.K_PERIOD: ":",
        #     pygame.locals.K_PLUS: "*",
        #     pygame.locals.K_MINUS: "_",
        #     pygame.locals.K_HASH: "'",
        #     pygame.locals.K_LESS: ">",
        #     pygame.locals.K_COMMA: ";"
        # }
        self.keys = {
            pygame.K_a: "a",
            pygame.K_b: "b",
            pygame.K_c: "c",
            pygame.K_d: "d",
            pygame.K_e: "e",
            pygame.K_f: "f",
            pygame.K_g: "g",
            pygame.K_h: "h",
            pygame.K_i: "i",
            pygame.K_j: "j",
            pygame.K_k: "k",
            pygame.K_l: "l",
            pygame.K_m: "m",
            pygame.K_n: "n",
            pygame.K_o: "o",
            pygame.K_p: "p",
            pygame.K_q: "q",
            pygame.K_r: "r",
            pygame.K_s: "s",
            pygame.K_t: "t",
            pygame.K_u: "u",
            pygame.K_v: "v",
            pygame.K_w: "w",
            pygame.K_x: "x",
            pygame.K_y: "y",
            pygame.K_z: "z",
            pygame.K_0: "0",
            pygame.K_1: "1",
            pygame.K_2: "2",
            pygame.K_3: "3",
            pygame.K_4: "4",
            pygame.K_5: "5",
            pygame.K_6: "6",
            pygame.K_7: "7",
            pygame.K_8: "8",
            pygame.K_9: "9",
            pygame.K_TAB: "\t",
            pygame.K_SPACE: " ",
            pygame.K_SEMICOLON: ";",
            pygame.K_SLASH: "/",
            pygame.K_RETURN: "\n",
            pygame.K_PERIOD: ".",
            pygame.K_PLUS: "+",
            pygame.K_PERCENT: "%",
            pygame.K_MINUS: "-",
            pygame.K_HASH: "#",
            pygame.K_UNDERSCORE: "_",
            pygame.K_LEFTBRACKET: "(",
            pygame.K_RIGHTBRACKET: ")",
            pygame.K_LESS: "<",
            pygame.K_GREATER: ">",
            pygame.K_EQUALS: "=",
            pygame.K_EURO: "€",
            pygame.K_EXCLAIM: "!",
            pygame.K_QUESTION: "?",
            pygame.K_DOLLAR: "$",
            pygame.K_COLON: ":",
            pygame.K_COMMA: ",",
            pygame.K_BACKSLASH: "\\",
            pygame.K_ASTERISK: "*",
        }
        self.shift_keys = {
            pygame.K_a: "A",
            pygame.K_b: "B",
            pygame.K_c: "C",
            pygame.K_d: "D",
            pygame.K_e: "E",
            pygame.K_f: "F",
            pygame.K_g: "G",
            pygame.K_h: "H",
            pygame.K_i: "I",
            pygame.K_j: "J",
            pygame.K_k: "K",
            pygame.K_l: "L",
            pygame.K_m: "M",
            pygame.K_n: "N",
            pygame.K_o: "O",
            pygame.K_p: "P",
            pygame.K_q: "Q",
            pygame.K_r: "R",
            pygame.K_s: "S",
            pygame.K_t: "T",
            pygame.K_u: "U",
            pygame.K_v: "V",
            pygame.K_w: "W",
            pygame.K_x: "X",
            pygame.K_y: "Y",
            pygame.K_z: "Z",
            pygame.K_0: "=",
            pygame.K_1: "!",
            pygame.K_2: "\"",
            pygame.K_3: "§",
            pygame.K_4: "$",
            pygame.K_5: "%",
            pygame.K_6: "&",
            pygame.K_7: "/",
            pygame.K_8: "(",
            pygame.K_9: ")",
            pygame.K_PERIOD: ":",
            pygame.K_PLUS: "*",
            pygame.K_MINUS: "_",
            pygame.K_HASH: "'",
            pygame.K_LESS: ">",
            pygame.K_COMMA: ";"
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
        # if keys[pygame.locals.K_LSHIFT] or keys[pygame.locals.K_RSHIFT]:
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
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
