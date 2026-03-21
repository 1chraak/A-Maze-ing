from mazegen.mazegen import Cell, MazeGenerator
from typing import List


def convert_hex(cell: Cell) -> str:
    hex = ['0', '1', '2', '3', '4', '5', '6', '7',
           '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    rep = [cell.up, cell.right, cell.down, cell.left]

    sum = 0
    for i in range(4):
        sum = sum + (rep[i] * (2 ** i))

    return (hex[sum % 16])


def hex_file(generated: MazeGenerator, path: List[str],
             file_name: str) -> None:
    try:
        with open(file_name, "w") as f:
            for line in range(generated.height):
                for column in range(generated.width):
                    cell = generated.maze[generated.width * line + column]
                    char = convert_hex(cell)
                    f.write(char)
                f.write("\n")
            f.write("\n")

            entry = f"{generated.entry[0]},{generated.entry[1]}"
            f.write(entry)
            f.write("\n")

            exit = f"{generated.exit[0]},{generated.exit[1]}"
            f.write(exit)
            f.write("\n")

            for dir in path:
                f.write(dir)
            f.write("\n")

    except Exception as e:
        print(f"ERROR: {e}")
