# PygameXtras
PygameXtras is a library designed to make programming with pygame easier. It supplies classes that aim at reducing the time and effort that go into everyday tasks like displaying text, creating buttons, managing entry forms, etc.

### example
```python
import pygame
import PygameXtras as px

pygame.init()
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()

circle_center = (350, 350)
circle_radius = 50

mouse_radius = 70
color = "blue"

line_y = 260

buttons = [
    px.Button(
        screen,
        c,
        25,
        (15 + i * 140, 15),
        "topleft",
        fd=(125, 40),
        bw=3,
        br=10,
        hl=True,
        bgc=c,
    )
    for i, c in enumerate(("purple", "green", "blue"))
]

label_touching = px.Label(screen, "not touching", 16, (0, 0), tc="red")
label_distance = px.Label(screen, "distance: n/a", 30, (25, 75), "topleft", tc=0)

entry = px.Entry(
    screen,
    "",
    25,
    (15, 135),
    "topleft",
    fd=(200, 40),
    bgc=150,
    bw=3,
    br=10,
    twe="custom color",
    ast=True,
)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for button in buttons:
        if button.update(events):
            color = button.backgroundcolor

    entry.update(events)
    if entry.get_state():
        entry.update_colors(bordercolor="blue")
    else:
        entry.update_colors(bordercolor="black")
    if entry.get() != "":
        try:
            color = px.parsers.Color.parse(entry.get())
        except:
            pass

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0], max(line_y, mouse_pos[1]))
    if px.Collisions.circle_circle(
        mouse_pos, mouse_radius, circle_center, circle_radius
    ):
        label_touching.update_text("touching")
        label_touching.update_colors(textcolor="lime")
    else:
        label_touching.update_text("not touching")
        label_touching.update_colors(textcolor="red")
    label_touching.update_pos(mouse_pos)
    label_distance.update_text(
        f"distance: {max(0, round(px.get_distance(mouse_pos, circle_center) - mouse_radius - circle_radius, 1))} px"
    )

    screen.fill((20, 90, 20))
    pygame.draw.circle(screen, (128, 128, 128), circle_center, circle_radius)
    pygame.draw.circle(screen, color, mouse_pos, mouse_radius)
    pygame.draw.line(
        screen, (0, 0, 0), (0, line_y - mouse_radius), (500, line_y - mouse_radius)
    )
    label_touching.draw()
    label_distance.draw()
    for button in buttons:
        button.draw()
    entry.draw()

    pygame.display.flip()
    clock.tick(120)
```