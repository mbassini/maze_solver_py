import random
import time

from graphics import Cell


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            window=None,
            seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = window
        self.seed = seed
        if seed is None:
            random.seed(seed)

        self._create_cells()
        self._draw_maze()

    def _create_cells(self):
        self._cells = []

        for _ in range(self._num_cols):
            column = []
            for _ in range(self._num_rows):
                cell = Cell(self._window)
                column.append(cell)
            self._cells.append(column)

        self._break_entrance_and_exit()
        # Start breaking walls from the entrance
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_maze(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if not self._window:
            return

        cell = self._cells[i][j]

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._window.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False

        i = self._num_cols - 1
        j = self._num_rows - 1
        exit_cell = self._cells[i][j]
        exit_cell.has_bottom_wall = False

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True

        possible_moves = ["up", "right", "left", "down"]
        random.shuffle(possible_moves)

        for move in possible_moves:
            x, y = None, None
            match move:
                case "up":
                    x = i
                    y = j - 1
                case "right":
                    x = i + 1
                    y = j
                case "left":
                    x = i - 1
                    y = j
                case "down":
                    x = i
                    y = j + 1

            in_scope = (0 <= x < self._num_cols) and (0 <= y < self._num_rows)
            if not in_scope or self._cells[x][y].visited:
                continue

            neighbor = self._cells[x][y]
            self._break_wall(move, current, neighbor)
            self._break_walls_r(x, y)

    def _break_wall(self, move, current, neighbor):
        match move:
            case "up":
                current.has_top_wall = False
                neighbor.has_bottom_wall = False
            case "right":
                current.has_right_wall = False
                neighbor.has_left_wall = False
            case "left":
                current.has_left_wall = False
                neighbor.has_right_wall = False
            case "down":
                current.has_bottom_wall = False
                neighbor.has_top_wall = False

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        is_exit = (i == self._num_cols - 1) and (j == self._num_rows - 1)
        if is_exit:
            return True

        directions = ["up", "right", "left", "down"]
        for direction in directions:
            x, y, blocking_wall = None, None, True
            match direction:
                case "up":
                    x = i
                    y = j - 1
                    blocking_wall = current_cell.has_top_wall
                case "right":
                    x = i + 1
                    y = j
                    blocking_wall = current_cell.has_right_wall
                case "left":
                    x = i - 1
                    y = j
                    blocking_wall = current_cell.has_left_wall
                case "down":
                    x = i
                    y = j + 1
                    blocking_wall = current_cell.has_bottom_wall

            in_scope = (0 <= x < self._num_cols) and (0 <= y < self._num_rows)

            if not in_scope or self._cells[x][y].visited or blocking_wall:
                continue

            next_cell = self._cells[x][y]
            current_cell.draw_move(next_cell)
            success = self._solve_r(x, y)
            if not success:
                current_cell.draw_move(next_cell, True)
            else:
                return True

        return False