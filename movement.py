import math


class MovementPattern:
    @staticmethod
    def polygon(robot, sides, radius, steps=100):
        angle_step = 2 * math.pi / sides
        side_length = 2 * radius * math.sin(math.pi / sides)
        for _ in range(sides):
            for _ in range(steps // sides):
                robot.move_forward(side_length / (steps // sides))
                yield
            robot.rotate(angle_step)

    @staticmethod
    def triangle(robot, side_length, steps=100):
        return MovementPattern.polygon(robot, 3, side_length / math.sqrt(3), steps)

    @staticmethod
    def square(robot, side_length, steps=100):
        return MovementPattern.polygon(robot, 4, side_length / math.sqrt(2), steps)

    @staticmethod
    def pentagon(robot, radius, steps=100):
        return MovementPattern.polygon(robot, 5, radius, steps)

    @staticmethod
    def hexagon(robot, radius, steps=100):
        return MovementPattern.polygon(robot, 6, radius, steps)

    @staticmethod
    def heptagon(robot, radius, steps=100):
        return MovementPattern.polygon(robot, 7, radius, steps)

    @staticmethod
    def octagon(robot, radius, steps=100):
        return MovementPattern.polygon(robot, 8, radius, steps)

    @staticmethod
    def oval(robot, a, b, steps=100):
        angle_step = 2 * math.pi / steps
        start_x, start_y = robot.x, robot.y
        for i in range(steps):
            theta = i * angle_step
            robot.x = start_x + a * math.cos(theta)
            robot.y = start_y + b * math.sin(theta)
            robot.angle = theta + math.pi / 2
            robot.record_path()
            yield
