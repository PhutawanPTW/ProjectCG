import pygame
from movement import MovementPattern

# Initialize fonts and colors
pygame.font.init()
FONT_PATH = "assets/Mali/Mali-Light.ttf"
FONT_SIZE = 20
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

WHITE = (255, 255, 255)
DARK_BLUE = (25, 42, 86)
LIGHT_BLUE = (52, 152, 219)
HOVER_COLOR = (41, 128, 185)
SHADOW_COLOR = (0, 0, 0, 100)
BUTTON_PRESSED_COLOR = (100, 100, 255)  # Color for pressed button


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.is_pressed = False  # Track if the button is pressed

    def draw(self, screen):
        color = (
            BUTTON_PRESSED_COLOR
            if self.is_pressed
            else (HOVER_COLOR if self.is_hovered else LIGHT_BLUE)
        )
        shadow_rect = self.rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=5)  # Shadow
        pygame.draw.rect(screen, color, self.rect, border_radius=5)

        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        """Check if mouse is hovering over the button"""
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        """Check if the button is clicked"""
        if self.rect.collidepoint(pos):
            self.is_pressed = True  # Set the button to pressed
            return True
        return False

    def release(self):
        """Reset button to unpressed state"""
        self.is_pressed = False


def get_click_position():
    """Function to get mouse click position."""
    running = True
    position = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                running = False
        pygame.display.flip()

    return position


def on_shape_button_click(robot, shape_type, points):
    pass  # No functionality for drawing shapes anymore


def create_buttons(robot, points):
    """Create buttons to control robot movement"""
    return [
        Button(
            50,
            50 + i * 60,
            220,
            50,
            shape,
            lambda shape=shape: on_shape_button_click(robot, shape, points),
        )
        for i, shape in enumerate(
            [
                "Circle",
                "Triangle",
                "Square",
                "Pentagon",
                "Hexagon",
                "Heptagon",
                "Octagon",
            ]
        )
    ]
