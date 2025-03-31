import pygame
import sys
import math
from robot import Robot
from ui import create_buttons, ColorSwatches
from movement import MovementPattern

# 📍 เริ่มต้น Pygame เพื่อใช้งานกราฟิกและการโต้ตอบ
pygame.init()

# 📍 กำหนดขนาดหน้าจอเริ่มต้นและสร้างหน้าต่างที่ปรับขนาดได้
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Robot Movement Simulation")  # 🖼️ ตั้งชื่อหน้าต่าง

# 📍 กำหนดสีพื้นฐานที่ใช้ในโปรแกรม
WHITE = (255, 255, 255)
BG_COLOR = (20, 30, 40)
DARK_BLUE = (44, 62, 80)
TECH_BLUE = (100, 150, 200)
GLOW_COLOR = (150, 200, 255)

# 📍 โหลดฟอนต์และกำหนดขนาดสำหรับข้อความ
FONT_PATH = "assets/Orbitron/static/Orbitron-Bold.ttf"
FONT = pygame.font.Font(FONT_PATH, 64) 
FONT_SMALL = pygame.font.Font(FONT_PATH, 40)
FONT_TINY = pygame.font.Font(FONT_PATH, 24)

# 📍 สร้างอ็อบเจ็กต์หุ่นยนต์สำหรับการจำลอง
robot = Robot()

# 📍 กำหนดขนาดกรอบสำหรับคำนวณรูปทรงการเคลื่อนที่
WIDTH = 150
HEIGHT = 150

# 📍 คำนวณขนาดของแต่ละรูปทรงให้อยู่ในกรอบ WIDTH x HEIGHT
circle_radius = min(WIDTH / 2, HEIGHT / 2)  # รัศมีวงกลม
oval_a = WIDTH / 2  # แกน x ของวงรี
oval_b = oval_a / 1.5  # แกน y ของวงรี
radius = min(WIDTH / 2, HEIGHT / 2)  # รัศมีพื้นฐานสำหรับรูปหลายเหลี่ยม
triangle_side = 2 * radius * math.tan(math.pi / 3)  # ความยาวด้านสามเหลี่ยม
square_side = 2 * radius  # ความยาวด้านสี่เหลี่ยม
pentagon_side = 2 * radius * math.tan(math.pi / 5)  # ความยาวด้านห้าเหลี่ยม
hexagon_side = 2 * radius * math.tan(math.pi / 6)  # ความยาวด้านหกเหลี่ยม
heptagon_side = 2 * radius * math.tan(math.pi / 7)  # ความยาวด้านเจ็ดเหลี่ยม
octagon_side = 2 * radius * math.tan(math.pi / 8)  # ความยาวด้านแปดเหลี่ยม
straight_length = WIDTH  # ความยาวเส้นตรง

# 📍 สร้างลิสต์ของรูปแบบการเคลื่อนที่ (patterns) สำหรับหุ่นยนต์
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
    MovementPattern("Colors"),  # ปุ่มพิเศษสำหรับเลือกสี
]

# 📍 สร้างปุ่มควบคุมจาก patterns และเชื่อมโยงกับหุ่นยนต์
buttons = create_buttons(robot, patterns)
swatches = None  # 🎨 ตัวแปรสำหรับจานสี (เริ่มต้นเป็น None)

# 📍 โหลดภาพพื้นหลัง (ถ้ามี) หรือตั้งเป็น None ถ้าโหลดไม่สำเร็จ
try:
    background_image = pygame.image.load(
        "assets/network_background.png"
    ).convert_alpha()
except:
    background_image = None


# 📍 ฟังก์ชันสำหรับวาดข้อความพร้อมเอฟเฟกต์เรืองแสง
def draw_text_with_glow(text, x, y, font, screen, text_color, glow_color):
    text_surface = font.render(text, True, text_color)
    glow_surface = font.render(text, True, glow_color)
    for i in range(1, 2):  # วาดเอฟเฟกต์เรืองแสงรอบข้อความ
        for dx, dy in [(-i, 0), (i, 0), (0, -i), (0, i)]:
            screen.blit(glow_surface, (x + dx, y + dy))
    screen.blit(text_surface, (x, y))


# 📍 ฟังก์ชันสำหรับวาดหุ่นยนต์แบบง่ายในหน้าจอเริ่มต้น
def draw_simple_robot(screen, center_x, center_y, scale=1):
    robot_color = (150, 200, 255)  # สีฟ้าอ่อนสำหรับหุ่นยนต์
    eye_color = (255, 255, 255)  # สีขาวสำหรับตา
    antenna_color = (200, 200, 200)  # สีเทาสำหรับเสาอากาศ
    head_size = 60 * scale  # ขนาดหัว
    head_rect = pygame.Rect(
        center_x - head_size // 2, center_y - head_size // 2, head_size, head_size
    )
    pygame.draw.rect(screen, robot_color, head_rect)  # วาดหัวเป็นสี่เหลี่ยม
    eye_radius = 10 * scale
    eye_offset_x = 15 * scale
    left_eye_pos = (center_x - eye_offset_x, center_y)
    right_eye_pos = (center_x + eye_offset_x, center_y)
    pygame.draw.circle(screen, eye_color, left_eye_pos, eye_radius)  # วาดตาซ้าย
    pygame.draw.circle(screen, eye_color, right_eye_pos, eye_radius)  # วาดตาขวา
    ear_radius = 25 * scale
    left_ear_pos = (center_x - head_size // 2, center_y)
    right_ear_pos = (center_x + head_size // 2, center_y)
    pygame.draw.circle(
        screen,
        robot_color,
        left_ear_pos,
        ear_radius,
        0,
        draw_top_left=True,
        draw_bottom_left=True,
    )  # วาดหูซ้าย
    pygame.draw.circle(
        screen,
        robot_color,
        right_ear_pos,
        ear_radius,
        0,
        draw_top_right=True,
        draw_bottom_right=True,
    )  # วาดหูขวา
    antenna_height = 20 * scale
    pygame.draw.line(
        screen,
        antenna_color,
        (center_x, center_y - head_size // 2),
        (center_x, center_y - head_size // 2 - antenna_height),
        3,
    )  # วาดเสาอากาศ
    pygame.draw.circle(
        screen, antenna_color, (center_x, center_y - head_size // 2 - antenna_height), 5
    )  # วาดจุดบนเสาอากาศ
    leg_width = 20 * scale
    leg_height = 30 * scale
    leg_pos = (center_x - leg_width // 2, center_y + head_size // 2)
    leg_points = [
        (leg_pos[0], leg_pos[1]),
        (leg_pos[0] + leg_width, leg_pos[1]),
        (leg_pos[0] + leg_width // 2, leg_pos[1] + leg_height),
    ]
    pygame.draw.polygon(screen, robot_color, leg_points)  # วาดขาเป็นสามเหลี่ยม


# 📍 ฟังก์ชันสำหรับแสดงหน้าจอเริ่มต้น
def start_screen():
    global screen, background_image, FONT, FONT_SMALL, FONT_TINY, SCREEN_WIDTH, SCREEN_HEIGHT
    running = True
    while running:
        # 📍 ปรับขนาดฟอนต์และหุ่นยนต์ให้เข้ากับขนาดหน้าจอ
        font_scale = min(SCREEN_WIDTH / 800, SCREEN_HEIGHT / 600)
        scale = min(SCREEN_WIDTH / 800, SCREEN_HEIGHT / 600)
        FONT = pygame.font.Font(FONT_PATH, int(64 * font_scale))
        FONT_SMALL = pygame.font.Font(FONT_PATH, int(40 * font_scale))
        FONT_TINY = pygame.font.Font(FONT_PATH, int(24 * font_scale))
        start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - int(120 * font_scale),
            int(SCREEN_HEIGHT * 0.75),
            int(240 * font_scale),
            int(70 * font_scale),
        )

        # 📍 เริ่มลูปเพื่อจัดการเหตุการณ์ในหน้าจอเริ่มต้น
        for event in pygame.event.get():
            # 🚪 ตรวจสอบว่าผู้ใช้กดปิดหน้าต่างหรือไม่ ถ้ากดจะหยุดโปรแกรม
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 📏 ตรวจจับการปรับขนาดหน้าต่าง เพื่ออัพเดตขนาดหน้าจอและภาพพื้นหลัง
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
                )
                if background_image:
                    background_image_scaled = pygame.transform.smoothscale(
                        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
                    )  # 🖼️ ปรับขนาดภาพพื้นหลัง
            # 🖱️ ตรวจจับการคลิกเมาส์ เพื่อเริ่มการจำลองเมื่อคลิกปุ่ม "START"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return False  # 🚪 ออกจากหน้าจอเริ่มต้นเมื่อคลิก "START"

        # 📍 วาดพื้นหลังและข้อความในหน้าจอเริ่มต้น
        if background_image:
            screen.blit(
                (
                    background_image_scaled
                    if "background_image_scaled" in locals()
                    else background_image
                ),
                (0, 0),
            )
        else:
            screen.fill(BG_COLOR)
        robot_text = "ROBOT"
        robot_surface = FONT.render(robot_text, True, WHITE)
        robot_x = SCREEN_WIDTH // 2 - robot_surface.get_width() // 2
        robot_y = int(SCREEN_HEIGHT * 0.2)
        draw_text_with_glow(
            robot_text, robot_x, robot_y, FONT, screen, WHITE, GLOW_COLOR
        )  # ✍️ วาดข้อความ "ROBOT"
        robot_pos_y = int(SCREEN_HEIGHT * 0.45)
        draw_simple_robot(screen, SCREEN_WIDTH // 2, robot_pos_y, scale)  # 🤖 วาดหุ่นยนต์
        subtitle_text = "Robot Movement Simulation"
        subtitle_surface = FONT_TINY.render(subtitle_text, True, TECH_BLUE)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle_surface.get_width() // 2
        subtitle_y = robot_pos_y + int(80 * scale)
        draw_text_with_glow(
            subtitle_text,
            subtitle_x,
            subtitle_y,
            FONT_TINY,
            screen,
            TECH_BLUE,
            GLOW_COLOR,
        )  # ✍️ วาดคำบรรยาย
        mouse_pos = pygame.mouse.get_pos()
        mouse_hover = start_button.collidepoint(mouse_pos)
        pygame.draw.rect(
            screen,
            (150, 200, 255) if mouse_hover else TECH_BLUE,
            start_button,
            border_radius=10,
        )  # 🎨 วาดปุ่ม "START" พร้อมเอฟเฟกต์ hover
        start_text = "START"
        start_surface = FONT_SMALL.render(start_text, True, WHITE)
        start_x = start_button.centerx - start_surface.get_width() // 2
        start_y = start_button.centery - start_surface.get_height() // 2
        draw_text_with_glow(
            start_text, start_x, start_y, FONT_SMALL, screen, WHITE, GLOW_COLOR
        )  # ✍️ วาดข้อความ "START"
        pygame.display.flip()  # 🔄 อัพเดตหน้าจอ

    return True


# 📍 เริ่มลูปหลักของโปรแกรม
show_start = True  # 🚪 ตัวแปรควบคุมการแสดงหน้าจอเริ่มต้น
running = True
clock = pygame.time.Clock()  # ⏱️ ควบคุมเฟรมเรท
while running:
    clock.tick(60)  # ⏱️ จำกัดเฟรมเรทที่ 60 FPS
    screen.fill(BG_COLOR)  # 🖼️ เติมสีพื้นหลัง

    # 📍 ตรวจสอบว่าต้องแสดงหน้าจอเริ่มต้นหรือไม่
    if show_start:
        show_start = start_screen()  # 🚪 เรียกฟังก์ชันหน้าจอเริ่มต้น
    else:
        # 📍 วาดปุ่มและอัพเดตหุ่นยนต์ในโหมดควบคุม
        for button in buttons:
            button.draw(screen)  # 🎨 วาดปุ่มควบคุม
        robot.update()  # 🤖 อัพเดตตำแหน่งและการเคลื่อนที่ของหุ่นยนต์
        robot.draw(screen)  # 🤖 วาดหุ่นยนต์และเส้นทาง
        if swatches:
            swatches.draw(screen)  # 🎨 วาดจานสีถ้ามี

    pygame.display.flip()  # 🔄 อัพเดตหน้าจอทั้งหมด

    # 📍 เริ่มลูปเพื่อจัดการเหตุการณ์ทั้งหมดที่ผู้ใช้ทำ (เช่น คลิกเมาส์, กดคีย์บอร์ด, ปิดหน้าต่าง)
    for event in pygame.event.get():
        # 🚪 ตรวจสอบว่าผู้ใช้กดปิดหน้าต่างหรือไม่ ถ้ากดจะหยุดโปรแกรม
        if event.type == pygame.QUIT:
            running = False

        # 🖱️ ตรวจจับการเคลื่อนไหวของเมาส์ เพื่อเปลี่ยนสีปุ่มเมื่อเมาส์ชี้ (hover)
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.check_hover(event.pos)  # 🎨 อัพเดตสถานะ hover ของปุ่ม

        # 🖱️ ตรวจจับการคลิกเมาส์ เพื่อให้ผู้ใช้โต้ตอบกับปุ่มหรือย้ายหุ่นยนต์
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_on_button = False

            # 🎨 ถ้ามีจานสี (swatches) แสดงอยู่ ให้จัดการการเลือกสี
            if swatches:
                if swatches.handle_event(event, robot):  # 🤖 อัพเดตสีเส้นทางของหุ่นยนต์
                    swatches = None  # 🚫 ซ่อนจานสีหลังจากเลือกสีเสร็จ
                continue

            # 🔄 ตรวจสอบว่าผู้ใช้คลิกปุ่มควบคุม (เช่น "Circle", "Square") หรือไม่
            for button in buttons:
                if button.is_clicked(event.pos):
                    clicked_on_button = True
                    for other_button in buttons:
                        if other_button != button:
                            other_button.release()  # 🖱️ รีเซ็ตสถานะปุ่มอื่น ๆ

                    # 🎨 ถ้าคลิกปุ่ม "Colors" ให้แสดงจานสี
                    if button.text == "Colors":
                        swatches = ColorSwatches(200, 100, 5, 4)  # 🎨 สร้างจานสี 5x4
                    else:
                        # 🛤️ ถ้าคลิกปุ่มรูปทรง (เช่น "Circle") ให้เริ่มการเคลื่อนที่
                        movement = button.action()
                        if movement:
                            print(
                                f"Running movement: {button.text}"
                            )  # 📜 แสดงชื่อการเคลื่อนที่ในคอนโซล
                            robot.reset_position(
                                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                            )  # 📍 รีเซ็ตตำแหน่งหุ่นยนต์ไปกึ่งกลาง
                            robot.set_movement(movement)  # 🛠️ ตั้งค่าการเคลื่อนที่ใหม่
                            robot.set_current_movement(
                                button.action
                            )  # 🔢 บันทึกการเคลื่อนที่เพื่อนับการกดซ้ำ
                            robot.set_visible(True)  # 👀 ทำให้หุ่นยนต์มองเห็นได้
                    break

            # 📍 ถ้าไม่ได้คลิกปุ่ม ให้ย้ายหุ่นยนต์ไปที่ตำแหน่งที่คลิก
            if not clicked_on_button:
                robot.move_to(mouse_pos[0], mouse_pos[1])  # 🤖 ย้ายหุ่นยนต์ไปตำแหน่งที่คลิก
                robot.set_visible(True)  # 👀 ทำให้หุ่นยนต์มองเห็นได้

        # 🖱️ ตรวจจับการปล่อยเมาส์ เพื่อรีเซ็ตสถานะปุ่ม
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.release()  # 🖱️ รีเซ็ตสถานะปุ่มเมื่อปล่อยเมาส์

        # ⌨️ ตรวจจับการกดคีย์บอร์ด เพื่อปรับทิศทางหัวหุ่นยนต์ (W, A, S, D)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                robot.angle = -math.pi / 2  # 📐 ชี้ขึ้น
            elif event.key == pygame.K_s:
                robot.angle = math.pi / 2  # 📐 ชี้ลง
            elif event.key == pygame.K_a:
                robot.angle = math.pi  # 📐 ชี้ซ้าย
            elif event.key == pygame.K_d:
                robot.angle = 0  # 📐 ชี้ขวา

        # 📏 ตรวจจับการปรับขนาดหน้าต่าง เพื่ออัพเดตขนาดหน้าจอและภาพพื้นหลัง
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
            )  # 📏 อัพเดตขนาดหน้าจอ
            if background_image:
                background_image_scaled = pygame.transform.smoothscale(
                    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )  # 🖼️ ปรับขนาดภาพพื้นหลังให้เข้ากับหน้าจอใหม่

# 🚪 ปิด Pygame และหยุดโปรแกรมเมื่อออกจากลูปหลัก
pygame.quit()
