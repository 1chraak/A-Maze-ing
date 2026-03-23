"""
Module for displaying the maze and handling user interaction.
Enhanced with Full Block rendering for the '42' pattern.
"""

import os
from mazegen.mazegen import MazeGenerator
from utils.pathfinder import path as get_path

# ANSI color codes
RESET = "\033[0m"

THEMES = [
    {"wall": "\033[97m", "path": "\033[92m", "special": "\033[95m"}, # White / Green / Magenta
    {"wall": "\033[94m", "path": "\033[93m", "special": "\033[91m"}, # Blue / Yellow / Red
    {"wall": "\033[96m", "path": "\033[95m", "special": "\033[93m"}, # Cyan / Magenta / Yellow
]

theme_index = 0

def get_path_coords(maze: MazeGenerator, path_directions: list[str]) -> set[tuple[int, int]]:
    """Convert directions into (x, y) coordinates."""
    x, y = maze.entry
    coords = {(x, y)}
    for move in path_directions:
        if move == "N": y -= 1
        elif move == "S": y += 1
        elif move == "E": x += 1
        elif move == "W": x -= 1
        coords.add((x, y))
    return coords


def render_maze(maze: MazeGenerator, show_path: bool = False, custom_coords: set | None = None) -> None:
    """Render the maze with large solid blocks for the '42' pattern."""
    global theme_index
    theme = THEMES[theme_index]
    wall_c = theme["wall"]
    path_c = theme["path"]
    special_c = theme["special"]

    w = maze.width
    h = maze.height
    grid = maze.maze
    
    path_coords = set()
    if custom_coords is not None:
        path_coords = custom_coords
    elif show_path:
        path_directions = get_path(maze)
        path_coords = get_path_coords(maze, path_directions)

    # Top border
    print(wall_c + "┏" + "━━━┳" * (w - 1) + "━━━┓" + RESET)

    for y in range(h):
        line = wall_c + "┃" + RESET

        for x in range(w):
            cell = grid[y * w + x]

            if (x, y) == maze.entry:
                content = path_c + " S " + RESET
            elif (x, y) == maze.exit:
                content = path_c + " E " + RESET
            elif (x, y) in path_coords:
                content = path_c + " • " + RESET
            # --- Rendering the large '42' blocks ---
            elif hasattr(cell, 'forbidden') and cell.forbidden:
                # الرمز '█' كيعمر البلاصة كاملة وكيبان كبيير
                content = special_c + "███" + RESET 
            # ---------------------------------------
            else:
                content = "   "

            line += content

            if cell.right:
                line += wall_c + "┃" + RESET
            else:
                # إذا كان ممر ديال 42 مفتوح من الجنب، كنلونوا حتى الفراغ باش يبان متصل
                if hasattr(cell, 'forbidden') and cell.forbidden:
                    line += special_c + " " + RESET
                else:
                    line += " "

        print(line)

        # Bottom walls
        if y < h - 1:
            line = wall_c + "┣"
            for x in range(w):
                cell = grid[y * w + x]
                if cell.down:
                    line += "━━━"
                else:
                    line += "   "

                if x < w - 1:
                    line += "╋"
                else:
                    line += "┫"
            print(line + RESET)

    # Bottom border
    print(wall_c + "┗" + "━━━┻" * (w - 1) + "━━━┛" + RESET)


def menu_loop(maze: MazeGenerator) -> str:
    """Interactive loop."""
    global theme_index
    show_path = True

    while True:
        os.system("clear")
        print("\n=== MAZE VIEW ===")    
        render_maze(maze, show_path)
        print("\n[r] regenerate | [p] Show/Hide Path | [a] Animate | [c] Theme | [q] Quit")
        try:
            choice = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if choice == "p":
            show_path = not show_path
        elif choice == "a":
            from display.animation import animate_solution
            animate_solution(maze, get_path(maze))
        elif choice == "c":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "q":
            return "quit"
        elif choice == "r":
            return "regenerate"
