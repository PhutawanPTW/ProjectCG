import pygame
import sys
import math
from robot import Robot
from ui import create_buttons, ColorSwatches
from movement import MovementPattern

pygame.init()

# กำหนดตัวแปรระดับโมดูล
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Robot Movement Simulation")

WHITE = (255, 255, 255)
BG_COLOR = (20, 30, 40)
DARK_BLUE = (44, 62, 80)
TECH_BLUE = (100, 150, 200)
GLOW_COLOR = (150, 200, 255)

FONT_PATH = "assets/Orbitron/static/Orbitron-Bold.ttf"
FONT = pygame.font.Font(FONT_PATH, 64)
FONT_SMALL = pygame.font.Font(FONT_PATH, 40)
FONT_TINY = pygame.font.Font(FONT_PATH, 24)

robot = Robot()

# กำหนดขนาดกรอบของรูปทรง (ความกว้างและความสูงเท่ากัน)
WIDTH = 200  # ความกว้างของกรอบ (พิกเซล)
HEIGHT = 200  # ความสูงของกรอบ (พิกเซล)

# คำนวณขนาดสำหรับแต่ละรูปทรงให้อยู่ในกรอบขนาด WIDTH x HEIGHT
circle_radius = min(WIDTH / 2, HEIGHT / 2)  # = 100 พิกเซล
oval_a = WIDTH / 2  # = 100 พิกเซล
oval_b = oval_a / 1.5  # ≈ 66.67 พิกเซล
radius = min(WIDTH / 2, HEIGHT / 2)  # = 100 พิกเซล
triangle_side = 2 * radius * math.tan(math.pi / 3)  # ≈ 346.41 พิกเซล
square_side = 2 * radius  # = 200 พิกเซล
pentagon_side = 2 * radius * math.tan(math.pi / 5)  # ≈ 137.64 พิกเซล
hexagon_side = 2 * radius * math.tan(math.pi / 6)  # ≈ 115.47 พิกเซล
heptagon_side = 2 * radius * math.tan(math.pi / 7)  # ≈ 101.15 พิกเซล
octagon_side = 2 * radius * math.tan(math.pi / 8)  # ≈ 90.51 พิกเซล
straight_length = WIDTH  # = 200 พิกเซล

# สร้างลิสต์ patterns สำหรับแต่ละรูปทรง
patterns = [
    MovementPattern("straight", length=straight_length, steps=400),
    MovementPattern("circle", radius=circle_radius, steps=400),
    MovementPattern("oval", a=oval_a, b=oval_b, steps=400),
    MovementPattern("triangle", side_length=triangle_side, steps=400),
    MovementPattern("square", side_length=square_side, steps=400),
    MovementPattern("pentagon", side_length=pentagon_side, steps=400),
    MovementPattern("hexagon", side_length=hexagon_side, steps=400),
    MovementPattern("heptagon", side_length=heptagon_side, steps=400),
    MovementPattern("octagon", side_length=octagon_side, steps=400),
    MovementPattern("Colors"),
]

# ส่ง patterns ไปยัง create_buttons
buttons = create_buttons(robot, patterns)
swatches = None

try:
    background_image = pygame.image.load("assets/network_background.png").convert_alpha()
except:
    background_image = None

def draw_text_with_glow(text, x, y, font, screen, text_color, glow_color):
    text_surface = font.render(text, True, text_color)
    glow_surface = font.render(text, True, glow_color)
    for i in range(1, 2):
        for dx, dy in [(-i, 0), (i, 0), (0, -i), (0, i)]:
            screen.blit(glow_surface, (x + dx, y + dy))
    screen.blit(text_surface, (x, y))

def draw_simple_robot(screen, x, y, scale=1.0):
    head_width = int(60 * scale)
    head_height = int(50 * scale)
    eye_size = int(8 * scale)
    ear_size = int(20 * scale)
    leg_size = int(20 * scale)
    antenna_height = int(20 * scale)
    antenna_tip_size = int(5 * scale)

    head_rect = pygame.Rect(x - head_width // 2, y - head_height // 2, head_width, head_height)
    pygame.draw.rect(screen, TECH_BLUE, head_rect, border_radius=10)

    pygame.draw.line(screen, TECH_BLUE, (x, y - head_height // 2), (x, y - head_height // 2 - antenna_height), 2)
    pygame.draw.circle(screen, TECH_BLUE, (x, y - head_height // 2 - antenna_height), antenna_tip_size)

    eye_offset_x = int(15 * scale)
    eye_y = y - int(5 * scale)
    pygame.draw.circle(screen, WHITE, (x - eye_offset_x, eye_y), eye_size)
    pygame.draw.circle(screen, WHITE, (x + eye_offset_x, eye_y), eye_size)

    pygame.draw.circle(screen, TECH_BLUE, (x - head_width // 2 - ear_size // 2, y - head_height // 2), ear_size, draw_top_left=True, draw_bottom_left=True)
    pygame.draw.circle(screen, TECH_BLUE, (x + head_width // 2 + ear_size // 2, y - head_height // 2), ear_size, draw_top_right=True, draw_bottom_right=True)

    leg_y_offset = int(5 * scale)
    pygame.draw.circle(screen, TECH_BLUE, (x - head_width // 4, y + head_height // 2 + leg_y_offset), leg_size, draw_bottom_left=True, draw_bottom_right=True)
    pygame.draw.circle(screen, TECH_BLUE, (x + head_width // 4, y + head_height // 2 + leg_y_offset), leg_size, draw_bottom_left=True, draw_bottom_right=True)

def start_screen():
    global screen, background_image, FONT, FONT_SMALL, FONT_TINY, SCREEN_WIDTH, SCREEN_HEIGHT

    running = True
    while running:
        # คำนวณ scale และ font_scale ใหม่ทุกครั้งในลูป
        font_scale = min(SCREEN_WIDTH / 800, SCREEN_HEIGHT / 600)
        scale = min(SCREEN_WIDTH / 800, SCREEN_HEIGHT / 600)

        # อัพเดตขนาดฟอนต์
        FONT = pygame.font.Font(FONT_PATH, int(64 * font_scale))
        FONT_SMALL = pygame.font.Font(FONT_PATH, int(40 * font_scale))
        FONT_TINY = pygame.font.Font(FONT_PATH, int(24 * font_scale))

        # อัพเดตตำแหน่งและขนาดของปุ่ม START
        start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - int(120 * font_scale),
            int(SCREEN_HEIGHT * 0.75),
            int(240 * font_scale),
            int(70 * font_scale)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                if background_image:
                    background_image_scaled = pygame.transform.smoothscale(
                        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
                    )
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return False

        # วาดภาพพื้นหลัง
        if background_image:
            screen.blit(background_image_scaled if 'background_image_scaled' in locals() else background_image, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # วาดข้อความ "ROBOT"
        robot_text = "ROBOT"
        robot_surface = FONT.render(robot_text, True, WHITE)
        robot_x = SCREEN_WIDTH // 2 - robot_surface.get_width() // 2
        robot_y = int(SCREEN_HEIGHT * 0.2)
        draw_text_with_glow(robot_text, robot_x, robot_y, FONT, screen, WHITE, GLOW_COLOR)

        # วาดหุ่นยนต์
        robot_pos_y = int(SCREEN_HEIGHT * 0.45)
        draw_simple_robot(screen, SCREEN_WIDTH // 2, robot_pos_y, scale)

        # วาดข้อความ "Robot Movement Simulation"
        subtitle_text = "Robot Movement Simulation"
        subtitle_surface = FONT_TINY.render(subtitle_text, True, TECH_BLUE)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle_surface.get_width() // 2
        subtitle_y = robot_pos_y + int(80 * scale)
        draw_text_with_glow(subtitle_text, subtitle_x, subtitle_y, FONT_TINY, screen, TECH_BLUE, GLOW_COLOR)

        # วาดปุ่ม "START"
        mouse_pos = pygame.mouse.get_pos()
        mouse_hover = start_button.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (150, 200, 255) if mouse_hover else TECH_BLUE, start_button, border_radius=10)
        start_text = "START"
        start_surface = FONT_SMALL.render(start_text, True, WHITE)
        start_x = start_button.centerx - start_surface.get_width() // 2
        start_y = start_button.centery - start_surface.get_height() // 2
        draw_text_with_glow(start_text, start_x, start_y, FONT_SMALL, screen, WHITE, GLOW_COLOR)

        pygame.display.flip()

    return True

# ลูปหลัก
show_start = True
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    if show_start:
        show_start = start_screen()
    else:
        for button in buttons:
            button.draw(screen)
        robot.update()
        robot.draw(screen)

        if swatches:
            swatches.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_on_button = False
            if swatches:
                if swatches.handle_event(event, robot):
                    swatches = None
                continue

            for button in buttons:
                if button.is_clicked(event.pos):
                    clicked_on_button = True
                    for other_button in buttons:
                        if other_button != button:
                            other_button.release()
                    if button.text == "Colors":
                        swatches = ColorSwatches(200, 100, 5, 4)
                    else:
                        movement = button.action()
                        if movement:
                            print(f"Running movement: {button.text}")
                            # รีเซ็ตตำแหน่งหุ่นยนต์ไปที่กึ่งกลางหน้าจอ
                            robot.reset_position(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            robot.set_movement(movement)
                            robot.set_current_movement(button.action)
                            robot.set_visible(True)
                    break
            
            if not clicked_on_button:
                robot.move_to(mouse_pos[0], mouse_pos[1])
                robot.set_visible(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.release()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                robot.angle = -math.pi / 2  # ชี้ขึ้น
            elif event.key == pygame.K_s:
                robot.angle = math.pi / 2   # ชี้ลง
            elif event.key == pygame.K_a:
                robot.angle = math.pi       # ชี้ซ้าย
            elif event.key == pygame.K_d:
                robot.angle = 0             # ชี้ขวา
        elif event.type == pygame.VIDEORESIZE:
            # อัพเดตขนาดหน้าจอเมื่อมีการปรับขนาด
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            if background_image:
                background_image_scaled = pygame.transform.smoothscale(
                    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )

pygame.quit()