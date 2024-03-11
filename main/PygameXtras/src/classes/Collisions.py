class Collisions:
    # summarized from https://www.jeffreythompson.org/collision-detection/table_of_contents.php

    @staticmethod
    def circle_circle(c1_center: tuple, c1_radius: float, c2_center: tuple, c2_radius: float) -> bool:
        return (c1_radius + c2_radius) ** 2 <= (c2_center[0] - c1_center[0]) ** 2 + (c2_center[1] - c1_center[1]) ** 2

    # NOT TESTED
    @staticmethod
    def rect_rect(rect1: tuple, rect2: tuple) -> bool:
        return (
            rect1[0] + rect1[2] >= rect2[0] and
            rect1[0] <= rect2[0] + rect2[2] and
            rect1[1] + rect2[3] >= rect2[1] and
            rect1[1] <= rect2[1] + rect2[3]
        )

    @staticmethod
    def circle_rect(circle_center: tuple, circle_radius: float, rect: tuple) -> bool:
        pass

    @staticmethod
    def line_circle(line_pos1: tuple, line_pos2: tuple, circle_center: tuple, circle_radius: float) -> bool:
        pass

    @staticmethod
    def line_line(l1_pos1: tuple, l1_pos2: tuple, l2_pos1: tuple, l2_pos2: tuple) -> bool:
        pass

    @staticmethod
    def line_rect(line_pos1: tuple, line_pos2: tuple, rect: tuple) -> bool:
        pass

    @staticmethod
    def polygon_circle(polygon: tuple, circle_center: tuple, circle_radius: float) -> bool:
        pass

    @staticmethod
    def polygon_rect(polygon: tuple, rect: tuple) -> bool:
        pass

    @staticmethod
    def polygon_line(polygon: tuple, line_pos1: tuple, line_pos2: tuple) -> bool:
        pass

    @staticmethod
    def polygon_polygon(polygon1: tuple, polygon2: tuple) -> bool:
        pass