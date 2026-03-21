from mazegen.mazegen import Cell, MazeGenerator
from typing import List


def direct(cell1: Cell, cell2: Cell) -> str:
    if cell1.line - cell2.line == 0:
        if cell1.column - cell2.column > 0:
            return "W"
        else:
            return "E"
    if cell1.column - cell2.column == 0:
        if cell1.line - cell2.line > 0:
            return "N"
        else:
            return "S"
    return "mypy is even more annoying than flake"


def path(generated: MazeGenerator) -> List[str]:
    path = []
    grid = generated.maze

    # changed the order here:
    entry = grid[generated.entry[1] * generated.width + generated.entry[0]]
    entry.step = 0  # The entry becomes 0, first cell

    exit = grid[generated.exit[1] * generated.width + generated.exit[0]]

    level = 0
    while True:
        layer = [cell for cell in grid if cell.step == level]
        for cell in layer:
            n = cell.neighbors(grid, generated.width, generated.height)
            c_n = cell.closed_neighbors(grid,
                                        generated.width, generated.height)
            neighbors = [neigh for neigh in n
                         if neigh not in c_n
                         and neigh.step == -1]
            if neighbors:
                if exit in neighbors:
                    exit.step = level + 1
                    break
                for block in neighbors:
                    block.step = level + 1
        if exit.step != -1:
            break

        level += 1

    level = exit.step
    path.append(exit)
    current = exit
    while current.step:
        nei = current.neighbors(grid, generated.width, generated.height)
        c = current.closed_neighbors(grid, generated.width, generated.height)
        next_cell = [cell for cell in nei
                     if cell not in c
                     and cell.step == current.step - 1]
        path.append(next_cell[0])
        current = next_cell[0]

    path.reverse()
    directions = []
    for i in range(len(path) - 1):
        way = direct(path[i], path[i + 1])
        directions.append(way)

    return directions
