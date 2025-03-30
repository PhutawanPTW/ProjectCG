import pygame
import math

class Robot:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else 400
        self.y = y if y is not None else 300
        self.initial_x = self.x
        self.initial_y = self.y
        self.angle = 0
        self.path = [(self.x, self.y)]
        self.circle_path = []
        self.movement_generator = None
        self.is_visible = False
        self.draw_path = True
        self.is_circular = False
        self.current_movement = None
        self.path_color = (200, 200, 200)
        self.moving_along_path = False
        self.path_index = 0
        self.direction = 1
        self.speed = 1
        self.last_movement = None
        self.movement_press_count = 0

    def set_visible(self, visible):
        self.is_visible = visible

    def set_draw_path(self, draw):
        self.draw_path = draw

    def set_circular(self, circular):
        self.is_circular = circular

    def clear_circle_path(self):
        self.circle_path = []

    def record_path(self):
        if self.is_circular:
            self.circle_path.append((self.x, self.y))
        else:
            self.path.append((self.x, self.y))

    def move_forward(self, distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        self.record_path()

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 2 * math.pi

    def set_movement(self, movement_generator):
        if movement_generator:
            self.movement_generator = iter(movement_generator)
            self.moving_along_path = False

    def set_current_movement(self, movement_func):
        if self.last_movement == movement_func:
            self.movement_press_count += 1
            if self.movement_press_count % 2 == 1:  # กดครั้งที่ 1, 3, 5, ... (หยุด)
                self.x = self.initial_x
                self.y = self.initial_y
                self.movement_generator = None
                self.moving_along_path = False
                self.path = [(self.x, self.y)]
                self.circle_path = []
                self.angle = -math.pi / 2  # รีเซ็ตหัวให้ชี้ขึ้นเมื่อหยุด
            else:  # กดครั้งที่ 2, 4, 6, ... (เคลื่อนที่ต่อ)
                self.set_movement(movement_func())
        else:
            self.last_movement = movement_func
            self.current_movement = movement_func
            self.movement_press_count = 0
            self.set_movement(movement_func())

    def set_path_color(self, color):
        self.path_color = color

    def start_moving_along_path(self):
        self.moving_along_path = True
        self.path_index = 0
        self.direction = 1
        if self.is_circular and self.circle_path:
            self.x, self.y = self.circle_path[0]
        elif self.path:
            self.x, self.y = self.path[0]

    def reset_position(self, center_x, center_y):
        """รีเซ็ตตำแหน่งของหุ่นยนต์ไปที่กึ่งกลางหน้าจอ"""
        self.x = center_x
        self.y = center_y
        self.initial_x = self.x
        self.initial_y = self.y
        self.path = [(self.x, self.y)]
        self.circle_path = []
        self.movement_generator = None
        self.moving_along_path = False
        self.angle = -math.pi / 2  # รีเซ็ตหัวให้ชี้ขึ้น

    def update(self):
        if self.movement_generator and not self.moving_along_path:
            try:
                next(self.movement_generator)
            except StopIteration:
                self.movement_generator = None
                self.start_moving_along_path()
        elif self.moving_along_path:
            path_to_follow = self.circle_path if self.is_circular else self.path
            if not path_to_follow:
                return

            target_index = self.path_index
            if 0 <= target_index < len(path_to_follow):
                target_x, target_y = path_to_follow[target_index]
                dx = target_x - self.x
                dy = target_y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance > 0:
                    self.angle = math.atan2(dy, dx)

                if distance <= self.speed:
                    self.x, self.y = target_x, target_y
                    self.path_index += self.direction
                else:
                    self.x += self.speed * math.cos(self.angle)
                    self.y += self.speed * math.sin(self.angle)

                if self.path_index >= len(path_to_follow) - 1:
                    if self.is_circular:
                        self.path_index = 0
                    else:
                        self.direction = -1
                        self.path_index = len(path_to_follow) - 1
                elif self.path_index <= 0:
                    self.direction = 1
                    self.path_index = 0

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.path = [(self.x, self.y)]
        self.circle_path = []
        self.movement_generator = None
        self.moving_along_path = False

    def draw(self, screen):
        if not self.is_visible:
            return

        if self.draw_path:
            if self.is_circular and len(self.circle_path) > 1:
                if self.moving_along_path:
                    pygame.draw.lines(screen, self.path_color, False, self.circle_path, 2)
                else:
                    pygame.draw.lines(screen, self.path_color, False, self.circle_path, 2)
            elif not self.is_circular and len(self.path) > 1:
                pygame.draw.lines(screen, self.path_color, False, self.path, 2)

        body_color = (100, 150, 200)
        eye_color = (255, 255, 255)
        radius = 15
        pygame.draw.circle(screen, body_color, (int(self.x), int(self.y)), radius)
        eye_offset = radius - 3
        eye_x = self.x + eye_offset * math.cos(self.angle)
        eye_y = self.y + eye_offset * math.sin(self.angle)
        pygame.draw.circle(screen, eye_color, (int(eye_x), int(eye_y)), 3)