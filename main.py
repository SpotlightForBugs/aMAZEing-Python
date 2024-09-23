from os import environ

# TODO: bounding box explodes upon MAZE_SIZE_X != MAZE_SIZE_Y
# TODO P2: visual indicator for start_pos and end_pos should scale with blablabla(CELL_SIZE_X, CELL_SIZE_Y)

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import math
import random
import sys

import pygame
from pygame.locals import *

# config
SCREEN_SIZE_X = 1920
SCREEN_SIZE_Y = 1080

MAZE_SIZE_X = 13
MAZE_SIZE_Y = 13
CELL_SIZE_X = 40
CELL_SIZE_Y = 40

TOP_LEFT_X = (SCREEN_SIZE_X - MAZE_SIZE_X * CELL_SIZE_X) / 2
TOP_LEFT_Y = (SCREEN_SIZE_Y - MAZE_SIZE_Y * CELL_SIZE_Y) / 2


class Cell:
    def __init__(self, up: bool, right: bool):
        self.up = up
        self.right = right

    def set_walls(self, up="unset", right="unset"):
        self.up = up if type(up) != str else self.up
        self.right = right if type(right) != str else self.right

    def get_up(self):
        return self.up

    def get_right(self):
        return self.right

    def print_self(self):
        print(f"{self.up=},{self.right=}")


def update(dt):
    # Called once per frame.
    # dt is the amount of time passed since last frame.

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == QUIT:
            pygame.quit()  # Opposite of pygame.init
            sys.exit()  # Not including this line crashes the script on Windows. Possibly


def draw(screen, maze: list | bool = False,
         pathfindingPositions: tuple[tuple[int, int], tuple[int, int]] | bool = False):
    screen.fill((0, 0, 0))  # Fill the screen with the blood of my enemies.
    if maze:
        drawMaze(maze)
        if pathfindingPositions:
            findPath(maze, pathfindingPositions[0], pathfindingPositions[1])

    pygame.display.flip()


def getEuclideanDistance(pos1: [float, float], pos2: [float, float]) -> float:
    return math.sqrt(math.pow((pos2[0] - pos1[0]), 2) + math.pow((pos2[1] - pos1[1]), 2))


def drawPixel(color: tuple[int, int, int], pos: tuple[float, float]):
    pygame.draw.line(globals().get("screen"), color, pos, pos, 1)


def drawLine(color: tuple[int, int, int], pos1: tuple[float, float], pos2: tuple[float, float]):
    pygame.draw.line(globals().get("screen"), color, pos1, pos2, 1)


def transformMazeToScreenSpace(pos: tuple[float, float]) -> tuple[float, float]:
    return int(TOP_LEFT_X + pos[0] * CELL_SIZE_X), int(TOP_LEFT_Y + pos[1] * CELL_SIZE_Y)


def incrementTupleBy(pTuple: tuple[float, float], scalar1: float, scalar2: float) -> tuple[float, float]:
    return pTuple[0] + scalar1, pTuple[1] + scalar2


def findPath(maze: list, startPos: tuple[int, int], endPos: tuple[int, int]):
    screen = globals().get("screen")
    pygame.draw.circle(screen, (0, 0, 255), incrementTupleBy(transformMazeToScreenSpace(startPos), CELL_SIZE_X*.5, -CELL_SIZE_Y*.5), 15)
    pygame.draw.circle(screen, (0, 255, 0), incrementTupleBy(transformMazeToScreenSpace(endPos), CELL_SIZE_X*.5, -CELL_SIZE_Y*.5), 15)


def drawMaze(maze: list):
    screen = globals().get("screen")

    dx = 0
    dy = 0
    for row in maze:
        for cell in row:
            cellX = TOP_LEFT_X + dx * CELL_SIZE_X
            cellY = TOP_LEFT_Y + dy * CELL_SIZE_Y

            drawCell(cell, (cellX, cellY))
            dy += 1
        dx += 1
        dy = 0
    topLeftBoundingBoxX = TOP_LEFT_X - CELL_SIZE_X
    topLeftBoundingBoxY = TOP_LEFT_Y - CELL_SIZE_Y
    drawLine((255, 0, 0), (topLeftBoundingBoxX, topLeftBoundingBoxY),
             (topLeftBoundingBoxX + (MAZE_SIZE_X + 1) * CELL_SIZE_X, topLeftBoundingBoxY))
    drawLine((255, 0, 0), (topLeftBoundingBoxX, topLeftBoundingBoxY),
             (topLeftBoundingBoxX, topLeftBoundingBoxY + (MAZE_SIZE_Y + 1) * CELL_SIZE_Y))
    drawLine((255, 0, 0), (TOP_LEFT_X + MAZE_SIZE_X * CELL_SIZE_X, topLeftBoundingBoxY),
             (TOP_LEFT_X + MAZE_SIZE_X *
              CELL_SIZE_X, TOP_LEFT_Y + MAZE_SIZE_Y * CELL_SIZE_Y))
    drawLine((255, 0, 0), (topLeftBoundingBoxX, TOP_LEFT_Y + MAZE_SIZE_X * CELL_SIZE_X),
             (topLeftBoundingBoxX + (MAZE_SIZE_X + 1) *
              CELL_SIZE_X, TOP_LEFT_Y + MAZE_SIZE_Y * CELL_SIZE_Y))


def drawCell(cell: Cell, pos: [float, float]):
    if cell.get_up():
        drawLine((255, 0, 0), pos, (pos[0] + CELL_SIZE_X, pos[1]))
    if cell.get_right():
        drawLine((255, 0, 0), pos, (pos[0], pos[1] + CELL_SIZE_Y))


def runPyGame():
    # Initialise PyGame.
    pygame.init()

    startPos = (random.randint(0, MAZE_SIZE_X), random.randint(0, MAZE_SIZE_Y))
    endPos = (random.randint(0, MAZE_SIZE_X), random.randint(0, MAZE_SIZE_Y))

    maze = [[Cell(True, True) for _ in range(MAZE_SIZE_X)] for _ in range(MAZE_SIZE_Y)]
    for row in maze:
        for cell in row:
            if random.randint(0, 1) == 0:
                cell.set_walls(up=False)
            else:
                cell.set_walls(right=False)

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    fps_clock = pygame.time.Clock()

    # Set up the window.
    width, height = SCREEN_SIZE_X, SCREEN_SIZE_Y
    screen = pygame.display.set_mode((width, height))
    globals()["screen"] = screen

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    while True:  # Loop forever!
        update(dt)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen, maze, (startPos, endPos))

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    runPyGame()

"""
# PyGame template by https://gist.github.com/MatthewJA/7544830/raw/4c579eb08a3c5190b028e96fb3705719b6241c5d/pygame-beginner-template.py

"""
