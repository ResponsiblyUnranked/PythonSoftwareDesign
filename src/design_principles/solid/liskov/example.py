# violation of Liskov
class Rectangle:
    width: float
    height: float

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, value: float) -> None:
        self.width = value

    def set_height(self, value: float) -> None:
        self.height = value


class Square(Rectangle):
    def set_width(self, value: float) -> None:
        self.width = value
        self.height = value

    def set_height(self, value: float) -> None:
        self.height = value
        self.width = value


def double_shape_size(shape: Rectangle) -> Rectangle:
    shape.set_width(2 * shape.width)
    shape.set_height(2 * shape.height)
    return shape
