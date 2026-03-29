from dataclasses import dataclass
from typing import List, Optional
import random
import sys


@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int]


class Cell:
    '''The class that defines cells as 4 walls'''

    def __init__(self, column: int, line: int) -> None:
        self.line = line
        self.column = column
        self.up = True
        self.right = True
        self.down = True
        self.left = True
        self.forbidden = False
        self.visited = False
        self.step = -1

    def neighbors(self, grid: List, width: int, height: int) -> List:
        neighbors = []

        if self.line > 0:
            neighbors.append(grid[(self.line - 1)
                                  * width + self.column])   # up

        if self.line < height - 1:
            neighbors.append(grid[(self.line + 1)
                                  * width + self.column])   # down

        if self.column > 0:
            neighbors.append(grid[self.line
                                  * width + (self.column - 1)])   # left

        if self.column < width - 1:
            neighbors.append(grid[self.line
                                  * width + (self.column + 1)])   # right

        return neighbors

    '''This method (closed_neighbors) is specifically for defining
        the neighbors that have a closed wall, it will be used for
        opening extra walls to make the maze NOT perfect'''

    def closed_neighbors(self, grid: List, width: int, height: int) -> List:
        neighbors = []

        if self.line > 0 and self.up:
            neighbors.append(grid[(self.line - 1)
                                  * width + self.column])   # up

        if self.line < height - 1 and self.down:
            neighbors.append(grid[(self.line + 1)
                                  * width + self.column])   # down

        if self.column > 0 and self.left:
            neighbors.append(grid[self.line
                                  * width + (self.column - 1)])   # left

        if self.column < width - 1 and self.right:
            neighbors.append(grid[self.line
                                  * width + (self.column + 1)])   # right

        return neighbors

    def diagonal_neighbors(self, grid: List, width: int, height: int) -> List:
        neighbors = []

        if self.line > 0 and self.column < width - 1:
            neighbors.append(grid[(self.line - 1)
                                  * width + self.column + 1])   # up-right

        if self.line < height - 1 and self.column < width - 1:
            neighbors.append(grid[(self.line + 1)
                                  * width + self.column + 1])   # down-right

        if self.column > 0 and self.line > 0:
            neighbors.append(grid[(self.line - 1)
                                  * width + (self.column - 1)])   # up-left

        if self.column > 0 and self.line < height - 1:
            neighbors.append(grid[(self.line + 1)
                                  * width + (self.column - 1)])   # down-left

        return neighbors


class MazeGenerator:
    '''The class for maze generation and treatment'''
    def __init__(self, configuration: Config) -> None:
        self.width = configuration.width
        self.height = configuration.height
        self.entry = configuration.entry
        self.exit = configuration.exit
        self.perfect = configuration.perfect
        self.maze: list[Cell] = []
        self.seed = configuration.seed
    '''Placing the 42 logo at the center by marking those cells as forbidden'''
    def shape_42(self, grid: List[Cell],
                 width: int, height: int) -> List[Cell]:
        head_column = (width - 7) // 2
        head_line = (height - 5) // 2
        forbidden_shape = [(head_line, head_column),
                           (head_line, head_column + 4),
                           (head_line, head_column + 5),
                           (head_line, head_column + 6),
                           (head_line + 1, head_column),
                           (head_line + 1, head_column + 6),
                           (head_line + 2, head_column),
                           (head_line + 2, head_column + 1),
                           (head_line + 2, head_column + 2),
                           (head_line + 2, head_column + 4),
                           (head_line + 2, head_column + 5),
                           (head_line + 2, head_column + 6),
                           (head_line + 3, head_column + 2),
                           (head_line + 3, head_column + 4),
                           (head_line + 4, head_column + 2),
                           (head_line + 4, head_column + 4),
                           (head_line + 4, head_column + 5),
                           (head_line + 4, head_column + 6)]

        if (self.entry[1], self.entry[0]) in forbidden_shape:  # changed order
            print("Entry coordinates fall within the forbidden shape")
            sys.exit()
        if (self.exit[1], self.exit[0]) in forbidden_shape:
            print("Exit coordinates fall within the forbidden shape")
            sys.exit()

        for cell in grid:
            if (cell.line, cell.column) in forbidden_shape:
                cell.forbidden = True
                cell.visited = True
        return grid

    def remove_wall(self, cell1: Cell, cell2: Cell) -> None:
        if cell1.line == cell2.line:
            if cell1.column < cell2.column:
                cell1.right = False
                cell2.left = False
            else:
                cell1.left = False
                cell2.right = False

        elif cell1.column == cell2.column:
            if cell1.line < cell2.line:
                cell1.down = False
                cell2.up = False
            else:
                cell1.up = False
                cell2.down = False

    def generate(self) -> None:
        if self.seed:
            random.seed(self.seed)
        grid = []
        for i in range(self.height):
            for j in range(self.width):
                grid.append(Cell(j, i))

        grid = self.shape_42(grid, self.width, self.height)

        '''The hunt and kill algorithm implementation'''
        while True:
            current: Cell | None  # To shut mypy up
            current = random.choice(grid)
            if current.forbidden:
                continue
            else:
                break
        current.visited = True

        while current:
            collection = current.neighbors(grid, self.width, self.height)
            unvisited_neighbors = [cell for cell in collection
                                   if not cell.visited and not cell.forbidden]

            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                self.remove_wall(current, neighbor)
                current = neighbor
                current.visited = True

            else:
                current = None
                for cell in grid:
                    if cell.visited is False:
                        coll = cell.neighbors(grid, self.width, self.height)
                        visited_neighbors = [block for block in coll
                                             if block.visited
                                             and not block.forbidden]

                        if visited_neighbors:
                            neighbor = random.choice(visited_neighbors)
                            self.remove_wall(cell, neighbor)
                            cell.visited = True
                            current = cell
                            break

        if not self.perfect:
            extra_open = int(self.width * self.height * 0.05)
            opened: List[Cell] = []

            for _ in range(extra_open):
                line = random.randrange(self.height)
                column = random.randrange(self.width)

                cell = grid[line * self.width + column]

                if cell not in opened and not cell.forbidden:
                    cl = cell.closed_neighbors(grid, self.width, self.height)
                    closed_neighbors = [neigh for neigh in cl
                                        if not neigh.forbidden]

                    if closed_neighbors:
                        to_open = random.choice(closed_neighbors)
                        self.remove_wall(cell, to_open)
                        opened = opened + [cell]  # Never touch the cell again

                        n = cell.neighbors(grid, self.width, self.height)
                        opened = opened + n  # Remove neighbors

                        d = cell.diagonal_neighbors(grid, self.width,
                                                    self.height)
                        opened = opened + d  # Remove diagonal neighbors

        self.maze = grid
