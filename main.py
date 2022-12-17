from line import Line
from window import Window
from utils import Position, Color, DisplayMode, Dimension, probability
from random import randint

window = Window("Simulation", DisplayMode.CENTER, Dimension(1000, 500))
graph = Line([], Color.from_hex("#7ec592"), Position(100, 250), Dimension(100, 10), 2)
window.addObj(graph)
marker = randint(3, 6)


def main():
    global marker

    if probability(50):
        marker += randint(0, 5)
    else:
        marker -= randint(0, 5)

    graph.add_point(marker)

    if marker > 0:
        graph.color = Color.from_hex("#87e657")
    else:
        graph.color = Color.from_hex("#eb4034")

    return True


window.display(main)
