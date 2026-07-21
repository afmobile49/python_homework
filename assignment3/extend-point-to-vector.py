# Task 5

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance(self, other):
        return math.sqrt(
            (other.x - self.x) ** 2
            + (other.y - self.y) ** 2
        )


class Vector(Point):
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
        )


if __name__ == "__main__":
    point1 = Point(1, 2)
    point2 = Point(1, 2)
    point3 = Point(4, 6)

    print(point1)
    print(point3)
    print(point1 == point2)
    print(point1.distance(point3))

    vector1 = Vector(2, 3)
    vector2 = Vector(4, 5)
    vector3 = vector1 + vector2

    print(vector1)
    print(vector2)
    print(vector3)