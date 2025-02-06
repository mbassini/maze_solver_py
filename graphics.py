from tkinter import Tk, BOTH, Canvas

class Window:
	def __init__(self, width, height):
		self.__root= Tk()
		self.__root.title = "Maze Solver"
		self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
		self.__canvas.pack(fill=BOTH, expand=1)
		self.__running = False
		self.__root.protocol("WM_DELETE_WINDOW", self.close)

	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()

	def wait_for_close(self):
		self.__running= True
		while self.__running:
			self.redraw()

	def close(self):
		self.__running = False
		
	def draw_line(self, line, fill_color = "black"):
		line.draw(self.__canvas, fill_color)

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Line:
	def __init__(self, p1, p2):
		self.__p1 = p1
		self.__p2 = p2

	def draw(self, canvas, fill_color):
		canvas.create_line(self.__p1.x, self.__p1.y, self.__p2.x, self.__p2.y, fill=fill_color, width=2)

class Cell:
	def __init__(self, window = None):
		self.has_left_wall = True 
		self.has_top_wall = True
		self.has_right_wall = True
		self.has_bottom_wall = True
		self._x1 = None
		self._x2 = None
		self._y1 = None
		self._y2 = None
		self._window = window
		self.visited = False

	def draw(self, x1, y1, x2, y2):
		if not self._window:
			return

		self._x1 = x1
		self._x2 = x2
		self._y1 = y1
		self._y2 = y2

		if self.has_left_wall:
			line = Line(Point(x1, y1), Point(x1, y2))
			self._window.draw_line(line)
		if self.has_top_wall:
			line = Line(Point(x1, y1), Point(x2, y1))
			self._window.draw_line(line)
		if self.has_bottom_wall:
			line = Line(Point(x1, y2), Point(x2, y2))
			self._window.draw_line(line)
		if self.has_right_wall:
			line = Line(Point(x2, y1), Point(x2, y2))
			self._window.draw_line(line)	

	def draw_move(self, to_cell, undo = False):
		from_x = (self._x1 + self._x2) / 2
		from_y = (self._y1 + self._y2) / 2
		to_x = (to_cell._x1 + to_cell._x2) / 2
		to_y = (to_cell._y1 + to_cell._y2) / 2

		line = Line(Point(from_x,from_y), Point(to_x,to_y))
		fill_color = "red" if not undo else "grey"
		self._window.draw_line(line, fill_color)
