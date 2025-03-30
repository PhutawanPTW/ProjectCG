import pygame
import colorsys  # เพิ่มการนำเข้า colorsys เพื่อสร้างจานสี
from movement import MovementPattern

pygame.font.init()
FONT_PATH = "assets/Orbitron/static/Orbitron-Bold.ttf"
FONT_SIZE = 20
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

WHITE = (255, 255, 255)
DARK_BLUE = (44, 62, 80)
LIGHT_BLUE = (200, 220, 240)
HOVER_COLOR = (220, 230, 245)
BUTTON_PRESSED_COLOR = (150, 180, 200)

# คลาสสำหรับจัดการปุ่มใน UI
class Button:
    def __init__(self, x, y, w, h, text, action):
        # x, y: ตำแหน่งของปุ่ม (มุมซ้ายบน)
        # w, h: ความกว้างและความสูงของปุ่ม
        # text: ข้อความที่จะแสดงบนปุ่ม
        # action: ฟังก์ชันที่จะเรียกเมื่อกดปุ่ม
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.is_hovered = False  # สถานะเมื่อเมาส์ชี้อยู่บนปุ่ม
        self.is_pressed = False  # สถานะเมื่อปุ่มถูกกด

    def draw(self, screen):
        # วาดปุ่มลงบนหน้าจอ
        # เปลี่ยนสีตามสถานะ: กด (BUTTON_PRESSED_COLOR), ชี้ (HOVER_COLOR), ปกติ (LIGHT_BLUE)
        color = BUTTON_PRESSED_COLOR if self.is_pressed else (HOVER_COLOR if self.is_hovered else LIGHT_BLUE)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        # วาดข้อความบนปุ่ม
        text_surface = FONT.render(self.text, True, DARK_BLUE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        # ตรวจสอบว่าเมาส์ชี้อยู่บนปุ่มหรือไม่
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        # ตรวจสอบว่าปุ่มถูกคลิกหรือไม่
        if self.rect.collidepoint(pos):
            self.is_pressed = True
            return True
        return False

    def release(self):
        # รีเซ็ตสถานะเมื่อปล่อยปุ่ม
        self.is_pressed = False

class ColorSwatches:
    def __init__(self, x, y, cols, rows):
        self.x = x
        self.y = y
        self.cols = cols  # จำนวนคอลัมน์ของจานสี
        self.rows = rows  # จำนวนแถวของจานสี
        self.swatch_size = 30  # ขนาดของแต่ละช่องสี
        self.padding = 5  # ระยะห่างระหว่างช่องสี
        # สร้างจานสีโดยใช้ colorsys
        self.colors = self.generate_color_palette(cols * rows)

    def generate_color_palette(self, num_colors):
        # สร้างจานสีโดยใช้ colorsys
        colors = []
        for i in range(num_colors):
            # ใช้ Hue ที่เปลี่ยนไปเรื่อย ๆ (0 ถึง 1) เพื่อให้ได้สีที่หลากหลาย
            hue = i / num_colors
            # แปลง HSV เป็น RGB (Saturation และ Value คงที่เพื่อให้สีสดใส)
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            # แปลงค่า RGB จาก (0-1) เป็น (0-255)
            colors.append(tuple(int(255 * x) for x in rgb))
        return colors

    def draw(self, screen):
        # วาดจานสีลงบนหน้าจอ
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                if index >= len(self.colors):
                    break
                color = self.colors[index]
                swatch_rect = pygame.Rect(
                    self.x + col * (self.swatch_size + self.padding),
                    self.y + row * (self.swatch_size + self.padding),
                    self.swatch_size,
                    self.swatch_size
                )
                pygame.draw.rect(screen, color, swatch_rect)
                pygame.draw.rect(screen, DARK_BLUE, swatch_rect, 1)

    def handle_event(self, event, robot):
        # จัดการเหตุการณ์เมื่อผู้ใช้เลือกสี
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for row in range(self.rows):
                for col in range(self.cols):
                    index = row * self.cols + col
                    if index >= len(self.colors):
                        break
                    swatch_rect = pygame.Rect(
                        self.x + col * (self.swatch_size + self.padding),
                        self.y + row * (self.swatch_size + self.padding),
                        self.swatch_size,
                        self.swatch_size
                    )
                    if swatch_rect.collidepoint(pos):
                        robot.set_path_color(self.colors[index])
                        return True
        return False

# ฟังก์ชันสำหรับสร้างปุ่มใน UI
def create_buttons(robot, patterns):
    buttons = []
    for i, pattern in enumerate(patterns):
        # สร้างปุ่มสำหรับแต่ละรูปแบบการเคลื่อนที่
        # i: ดัชนีของปุ่ม (ใช้คำนวณตำแหน่ง y)
        # pattern: อ็อบเจ็กต์ MovementPattern ที่กำหนดรูปแบบการเคลื่อนที่
        action = lambda p=pattern: p.get_movement(robot)  # ฟังก์ชันที่จะเรียกเมื่อกดปุ่ม
        if pattern.pattern_type == "Colors":
            action = lambda: None  # ปุ่ม Colors ไม่เรียกการเคลื่อนที่
        buttons.append(Button(10, 10 + i * 60, 150, 50, pattern.pattern_type.capitalize(), action))
    return buttons