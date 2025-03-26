import pygame
from robot import Robot
from ui import create_buttons
from StartScreen import show_start_screen

points = []
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Movement Simulation")

WHITE = (255, 255, 255)
GRID_COLOR = (200, 200, 200)

robot = Robot(
    SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
    SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE,
)
buttons = create_buttons(robot, points)


def draw_grid():
    """Draw the grid lines on screen"""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))


show_start = True
start_button = show_start_screen()

running = True
while running:
    screen.fill(WHITE)
    draw_grid()

    if show_start:
        mouse_pos = pygame.mouse.get_pos()
        mouse_hover = start_button.collidepoint(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_hover:
                show_start = False
        pygame.draw.rect(
            screen,
            HOVER_COLOR if mouse_hover else LIGHT_BLUE,
            start_button,
            border_radius=10,
        )
        draw_text_with_outline(
            "START",
            SCREEN_WIDTH // 2 - 85,
            SCREEN_HEIGHT // 2 + 110,
            FONT_SMALL,
            screen,
            DARK_BLUE,
            BG_COLOR,
        )
    else:
        for button in buttons:
            button.draw(screen)
        robot.update()
        robot.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if show_start:
                start_button.check_hover(event.pos)
            else:
                for button in buttons:
                    button.check_hover(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_start and start_button.is_clicked(event.pos):
                show_start = False
            elif not show_start:
                for button in buttons:
                    if button.is_clicked(
                        event.pos
                    ):  # No need to pass buttons here anymore
                        movement = button.action()
                        if movement:
                            print(f"Running movement: {button.text}")
                            robot.set_movement(movement)
        elif event.type == pygame.MOUSEBUTTONUP:
            # Release button when mouse button is released
            for button in buttons:
                button.release()

pygame.quit()
