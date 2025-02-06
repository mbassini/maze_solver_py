import sys
import os

from graphics import Window, Cell, Point
from maze import Maze

def main():
	window = Window(800, 600)

	maze = Maze(100, 100, 10, 10, 50, 50, window)
	maze.solve()
	window.wait_for_close()

main()
