from pygame import Surface, draw
from utils import Position, Color, DisplayMode, Dimension


class Polygon:
    """ Pygame polygon """
    positions: [Position]
    """ Vertex Positions of the polygon """
    color: Color
    """ Color of the polygon """
    thickness: int
    """ Thickness of the polygon """

    def __init__(self, positions: [Position], color: Color, thickness: int = 0):
        self.positions = positions
        self.color = color
        self.thickness = thickness

    def display(self, screen: Surface, _: DisplayMode):
        vertexes = []
        for position in self.positions:
            vertexes.append(position.to_tuple())

        draw.polygon(
            screen,
            self.color.toRGB(),
            vertexes,
            self.thickness
        )


class Line(Polygon):
    points: list[Position]
    origin: Position
    overflow_point: Dimension
    zoom: float

    def __init__(
            self,
            points: list[float],
            color: Color,
            origin: Position = Position(0, 0),
            overflow_point=Dimension(0, 0),
            zoom: float = 1
    ):
        self.points = []
        for i in range(0, len(points)):
            self.points += [Position.from_tuple((i+1, points[i]))]
        self.origin = origin
        self.color = color
        self.overflow_point = overflow_point
        self.zoom = zoom
        super().__init__(self.points, self.color)

    def add_point(self, x: float):
        self.points += [
            Position.from_tuple((len(self.points), x))
        ]

    def draw(self, window_dimension: Dimension):
        self.positions = [
            Position(0, window_dimension.height)
            .offset_new(self.origin.x, -self.origin.y)
        ]
        self.positions += list(map(
            lambda x: x
            .multiplier_new(self.zoom, -self.zoom)
            .offset_new(self.origin.x, window_dimension.height - self.origin.y),
            self.points
        ))
        self.positions += [
            Position(self.points[-1].x if len(self.points) >= 1 else 0, window_dimension.height)
            .multiplier_new(self.zoom, 1)
            .offset_new(self.origin.x, -self.origin.y)
        ]
        if len(self.points) == 0:  # to add least 3 points for the polygon
            self.positions += [Position(self.origin.x+1, window_dimension.height - self.origin.y)]

        # x - overflow
        overflow = self.positions[-1].x - window_dimension.width + self.overflow_point.width
        if overflow >= 0:
            for position in self.positions:
                position.offset(-overflow, 0)

        # y - overflow
        overflow = self.positions[-2].y
        if overflow <= self.overflow_point.height or overflow >= window_dimension.height - self.overflow_point.height:
            self.zoom *= 0.9
