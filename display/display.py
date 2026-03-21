"""Module for displaying the maze and handling user interaction."""

from mazegen.mazegen import MazeGenerator
from utils.pathfinder import path as get_path

# ANSI color codes for terminal display
RESET = "\033[0m"

THEMES = [
    {"wall": "\033[97m", "path": "\033[92m", "special": "\033[95m"}, # White / Green
    {"wall": "\033[94m", "path": "\033[93m", "special": "\033[91m"}, # Blue / Yellow
    {"wall": "\033[96m", "path": "\033[95m", "special": "\033[93m"}, # Cyan / Magenta
]

theme_index = 0

def get_path_coords(maze: MazeGenerator, path_directions: list[str]) -> set[tuple[int, int]]:
    """Convert a list of directions (N, S, E, W) into (x, y) coordinates."""
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
    """Render the maze in the terminal using ASCII/Unicode characters."""
    global theme_index
    theme = THEMES[theme_index]
    wall_c = theme["wall"]
    path_c = theme["path"]

    w = maze.width
    h = maze.height
    grid = maze.maze
    
    # Determine the path coordinates to display
    path_coords = set()
    if custom_coords is not None:
        path_coords = custom_coords
    elif show_path:
        path_directions = get_path(maze)
        path_coords = get_path_coords(maze, path_directions)

    # Top border (Ceiling of the maze)
    print(wall_c + "┏" + "━━━┳" * (w - 1) + "━━━┓" + RESET)

    for y in range(h):
        line = wall_c + "┃" + RESET

        for x in range(w):
            cell = grid[y * w + x]

            # Set cell content (Start, Exit, Path, or Empty space)
            if (x, y) == maze.entry:
                content = path_c + " S " + RESET
            elif (x, y) == maze.exit:
                content = path_c + " E " + RESET
            elif (x, y) in path_coords:
                content = path_c + " • " + RESET
            else:
                content = "   "

            line += content

            # Right wall (East)
            if cell.right:
                line += wall_c + "┃" + RESET
            else:
                line += " "

        print(line)

        # Bottom walls (South)
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

    # Bottom border (Floor of the maze)
    print(wall_c + "┗" + "━━━┻" * (w - 1) + "━━━┛" + RESET)


def menu_loop(maze: MazeGenerator) -> None:
    """Run the interactive loop for user commands."""
    global theme_index
    show_path = False

    while True:
        print("\n=== MAZE VIEW ===")
        render_maze(maze, show_path)
        
        print("\n[p] Show/Hide Path | [a] Animate | [c] Theme | [q] Quit")
        try:
            choice = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if choice == "p":
            show_path = not show_path
        elif choice == "a":
            # Import locally to avoid circular dependencies
            from display.animation import animate_solution
            directions = get_path(maze)
            animate_solution(maze, directions)
        elif choice == "c":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "q":
            break
        else:
            print("Invalid input! Please choose a valid option.")