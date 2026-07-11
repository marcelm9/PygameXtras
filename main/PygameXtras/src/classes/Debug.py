import pygame

from .Label import Label


class Debug:
    label = Label(
        surface=None,
        text="",
        xy=(5, 5),
        anchor="topleft",
        size=14,
        tc=(255, 255, 255),
        font="consola",
    )
    y_distance = 15
    messages: list[str] = []

    @staticmethod
    def log(message: str) -> None:
        print(f"[DEBUG]: {message}")

    @staticmethod
    def show(message) -> None:
        Debug.messages.append(message)

    @staticmethod
    def render(screen: pygame.Surface) -> None:
        for i, message in enumerate(Debug.messages, 1):
            Debug.label.update_pos((5, 5 + i * Debug.y_distance))
            Debug.label.update_text(f"{message}")
            Debug.label.draw_to(screen)
        Debug.messages.clear()
