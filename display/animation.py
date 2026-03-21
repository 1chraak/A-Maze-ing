"""Module for animating the maze solutions."""

import time
import os
from mazegen.mazegen import MazeGenerator
from display.display import render_maze

def clear_screen() -> None:
    """Clear the terminal screen to create an animation effect."""
    os.system("cls" if os.name == "nt" else "clear")

def animate_solution(maze: MazeGenerator, path_directions: list[str], delay: float = 0.05) -> None:
    """
    Animate the solution path step by step.
    """
    x, y = maze.entry
    current_coords = {(x, y)}

    # Display the very first frame of the animation
    clear_screen()
    render_maze(maze, custom_coords=current_coords)
    time.sleep(delay)

    # Add the path points one by one
    for move in path_directions:
        if move == "N":
            y -= 1
        elif move == "S":
            y += 1
        elif move == "E":
            x += 1
        elif move == "W":
            x -= 1

        current_coords.add((x, y))

        # Clear the screen, redraw with the new point, and wait
        clear_screen()
        render_maze(maze, custom_coords=current_coords)
        time.sleep(delay)