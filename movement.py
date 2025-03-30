import math

class MovementPattern:
    def __init__(self, pattern_type, **kwargs):
        self.pattern_type = pattern_type
        self.params = kwargs

    def get_movement(self, robot):
        if self.pattern_type == "straight":
            return self.straight_line(robot, self.params.get("length", 300), self.params.get("steps", 400))
        elif self.pattern_type == "circle":
            return self.circle(robot, self.params.get("radius", 47.75), self.params.get("steps", 400))
        elif self.pattern_type == "oval":
            return self.oval(robot, self.params.get("a", 57.30), self.params.get("b", 38.20), self.params.get("steps", 400))
        elif self.pattern_type == "triangle":
            return self.triangle(robot, self.params.get("side_length", 100), self.params.get("steps", 400))
        elif self.pattern_type == "square":
            return self.square(robot, self.params.get("side_length", 75), self.params.get("steps", 400))
        elif self.pattern_type == "pentagon":
            return self.pentagon(robot, self.params.get("side_length", 60), self.params.get("steps", 400))
        elif self.pattern_type == "hexagon":
            return self.hexagon(robot, self.params.get("side_length", 50), self.params.get("steps", 400))
        elif self.pattern_type == "heptagon":
            return self.heptagon(robot, self.params.get("side_length", 42.86), self.params.get("steps", 400))
        elif self.pattern_type == "octagon":
            return self.octagon(robot, self.params.get("side_length", 37.5), self.params.get("steps", 400))
        else:
            raise ValueError(f"Unknown pattern type: {self.pattern_type}")

    @staticmethod
    def dda_line(robot, x1, y1, x2, y2, steps):
        """อัลกอริทึม DDA สำหรับการเคลื่อนที่เป็นเส้นตรงจาก (x1, y1) ไป (x2, y2)"""
        dx = x2 - x1
        dy = y2 - y1
        # คำนวณจำนวนก้าว (steps) ตาม DDA
        step = max(abs(dx), abs(dy))
        if step == 0:
            step = 1  # ป้องกันการหารด้วย 0
        x_inc = dx / step
        y_inc = dy / step
        x, y = x1, y1
        for _ in range(int(step)):
            # คำนวณระยะห่างระหว่างจุดปัจจุบันและจุดถัดไป
            next_x = x + x_inc
            next_y = y + y_inc
            distance = math.sqrt((next_x - x)**2 + (next_y - y)**2)
            # ปรับมุมของหุ่นยนต์ให้ชี้ไปยังจุดถัดไป
            robot.angle = math.atan2(next_y - y, next_x - x)
            robot.move_forward(distance)
            x, y = next_x, next_y
            yield

    @staticmethod
    def polygon(robot, sides, side_length, steps=400):
        robot.set_draw_path(True)
        robot.set_circular(False)
        angle_step = 2 * math.pi / sides  # มุมระหว่างด้าน
        steps_per_side = steps // sides
        current_angle = robot.angle
        start_x, start_y = robot.x, robot.y
        for _ in range(sides):
            # คำนวณตำแหน่งปลายของด้านถัดไป
            end_x = start_x + side_length * math.cos(current_angle)
            end_y = start_y + side_length * math.sin(current_angle)
            # ใช้ DDA เพื่อเคลื่อนที่เป็นเส้นตรง
            yield from MovementPattern.dda_line(robot, start_x, start_y, end_x, end_y, steps_per_side)
            # อัพเดตตำแหน่งเริ่มต้นสำหรับด้านถัดไป
            start_x, start_y = end_x, end_y
            # หมุนมุมสำหรับด้านถัดไป
            current_angle += angle_step
            robot.angle = current_angle

    @staticmethod
    def triangle(robot, side_length, steps=400):
        return MovementPattern.polygon(robot, 3, side_length, steps)

    @staticmethod
    def square(robot, side_length, steps=400):
        return MovementPattern.polygon(robot, 4, side_length, steps)

    @staticmethod
    def pentagon(robot, side_length, steps=400):
        return MovementPattern.polygon(robot, 5, side_length, steps)

    @staticmethod
    def hexagon(robot, side_length, steps=400):
        return MovementPattern.polygon(robot, 6, side_length, steps)

    @staticmethod
    def heptagon(robot, side_length, steps=400):
        return MovementPattern.polygon(robot, 7, side_length, steps)

    @staticmethod
    def octagon(robot, side_length, steps=400):
        return MovementPattern.polygon(robot, 8, side_length, steps)

    @staticmethod
    def oval(robot, a, b, steps=400):
        robot.set_draw_path(True)
        robot.set_circular(True)
        robot.clear_circle_path()
        start_x, start_y = robot.x, robot.y
        angle_step = 2 * math.pi / steps
        # คำนวณเส้นรอบวงคร่าวๆ เพื่อหาความยาวในแต่ละขั้นตอน
        perimeter = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))  # สูตรประมาณสำหรับวงรี
        step_distance = perimeter / steps
        for i in range(steps + 1):
            theta = i * angle_step
            # คำนวณพิกัดปัจจุบัน
            x = start_x + a * math.cos(theta)
            y = start_y + b * math.sin(theta)
            # คำนวณมุมที่หุ่นยนต์ควรหันหน้าไป
            next_theta = (i + 1) * angle_step
            next_x = start_x + a * math.cos(next_theta)
            next_y = start_y + b * math.sin(next_theta)
            robot.angle = math.atan2(next_y - y, next_x - x)
            # เคลื่อนที่ไปข้างหน้า
            robot.move_forward(step_distance)
            yield

    @staticmethod
    def circle(robot, radius, steps=400):
        robot.set_draw_path(True)
        robot.set_circular(True)
        robot.clear_circle_path()
        start_x, start_y = robot.x, robot.y
        circumference = 2 * math.pi * radius
        step_distance = circumference / steps
        angle_step = 2 * math.pi / steps
        for _ in range(steps + 1):
            robot.move_forward(step_distance)
            robot.rotate(angle_step)
            yield

    @staticmethod
    def straight_line(robot, distance, steps=400):
        robot.set_draw_path(True)
        robot.set_circular(False)
        start_x, start_y = robot.x, robot.y
        end_x = start_x + distance * math.cos(robot.angle)
        end_y = start_y + distance * math.sin(robot.angle)
        yield from MovementPattern.dda_line(robot, start_x, start_y, end_x, end_y, steps)