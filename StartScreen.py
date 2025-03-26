import pygame
import sys
from ui import create_buttons
from robot import Robot  # นำเข้าหุ่นยนต์จาก robot.py
from movement import MovementPattern  # นำเข้าการเคลื่อนที่จาก movement.py

# เริ่มต้น Pygame
pygame.init()

# โหลดฟอนต์
FONT_PATH = "assets/Orbitron/static/Orbitron-Bold.ttf"
FONT_SIZE = 64
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
FONT_SMALL = pygame.font.Font(FONT_PATH, 40)

# สีที่ใช้
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)  # สีฟ้าอ่อน
DARK_BLUE = (44, 62, 80)  # สีเงาหรือขอบ
BG_COLOR = (20, 20, 20)  # สีพื้นหลัง
HOVER_COLOR = (150, 200, 220)  # สีฟ้าจางลงเมื่อ Hover
BUTTON_PRESSED_COLOR = (100, 100, 255)  # สีปุ่มเมื่อถูกกด

# ตั้งค่าหน้าต่าง
WIDTH, HEIGHT = 800, 600


def draw_text_with_outline(text, x, y, font, screen, text_color, outline_color):
    """ฟังก์ชันวาดข้อความพร้อมขอบเงา"""
    text_surface = font.render(text, True, text_color)

    # วาดขอบ
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        shadow_surface = font.render(text, True, outline_color)
        screen.blit(shadow_surface, (x + dx, y + dy))

    # วาดข้อความหลัก
    screen.blit(text_surface, (x, y))


def draw_robot(screen):
    """ฟังก์ชันการวาดหุ่นยนต์"""
    body_color = LIGHT_BLUE
    eye_color = DARK_BLUE
    # ตัวหุ่นยนต์
    pygame.draw.rect(
        screen, body_color, (WIDTH // 2 - 40, HEIGHT // 2 - 100, 80, 80)
    )  # ตัวหุ่นยนต์
    pygame.draw.circle(
        screen, body_color, (WIDTH // 2, HEIGHT // 2 - 110), 10
    )  # เสาอากาศ
    pygame.draw.line(
        screen,
        body_color,
        (WIDTH // 2, HEIGHT // 2 - 110),
        (WIDTH // 2, HEIGHT // 2),
        3,
    )  # เสาเชื่อม
    # ตา
    pygame.draw.rect(
        screen, eye_color, (WIDTH // 2 - 20, HEIGHT // 2 - 50, 15, 15)
    )  # ตาซ้าย
    pygame.draw.rect(
        screen, eye_color, (WIDTH // 2 + 5, HEIGHT // 2 - 50, 15, 15)
    )  # ตาขวา
    pygame.draw.rect(
        screen, (100, 100, 100), (WIDTH // 2 - 35, HEIGHT // 2 + 20, 70, 5)
    )  # เงาด้านล่าง


def show_movement_screen():
    """ฟังก์ชันสำหรับเปลี่ยนไปยังหน้าควบคุมหุ่นยนต์ (แต่ไม่มีการวาดอะไร)"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Robot Movement")

    buttons = create_buttons(None, [])  # ปุ่มควบคุมหุ่นยนต์
    running = True
    while running:
        screen.fill(BG_COLOR)  # พื้นหลังสีดำ

        # วาดปุ่ม
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        button.action()

            for button in buttons:
                button.check_hover(pygame.mouse.get_pos())


def show_start_screen():
    """ฟังก์ชันหน้าจอเริ่มต้น"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Start Screen")

    START_BUTTON = pygame.Rect(800 // 2 - 120, 600 // 2 + 100, 240, 70)  # ปุ่ม START

    # สร้างปุ่มจากฟังก์ชัน create_buttons
    buttons = create_buttons(None, [])  # ส่งค่าพารามิเตอร์ให้เป็นค่าว่าง เพราะไม่มีการใช้งานในกรณีนี้

    running = True
    while running:
        screen.fill(BG_COLOR)  # พื้นหลังสีดำ

        # วาดข้อความ "ROBOT."
        draw_text_with_outline(
            "ROBOT",
            800 // 2 - 135,
            600 // 2 - 210,
            FONT,
            screen,
            LIGHT_BLUE,
            DARK_BLUE,
        )

        # วาดหุ่นยนต์
        draw_robot(screen)

        mouse_pos = pygame.mouse.get_pos()
        mouse_hover = START_BUTTON.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # ออกจากฟังก์ชัน
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_hover:
                print("Start Game!")  # สามารถใส่โค้ดเปิดเกมได้
                show_movement_screen()  # เปลี่ยนไปยังหน้าควบคุมหุ่นยนต์
                return True  # ออกจากหน้าจอเริ่มต้น

        # วาดปุ่ม START
        if mouse_hover:
            pygame.draw.rect(screen, HOVER_COLOR, START_BUTTON, border_radius=10)
        else:
            pygame.draw.rect(screen, LIGHT_BLUE, START_BUTTON, border_radius=10)

        draw_text_with_outline(
            "START",
            800 // 2 - 85,
            600 // 2 + 110,
            FONT_SMALL,
            screen,
            DARK_BLUE,
            BG_COLOR,
        )

        pygame.display.flip()

        # รับเหตุการณ์จากผู้ใช้
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        button.action()

    pygame.quit()
