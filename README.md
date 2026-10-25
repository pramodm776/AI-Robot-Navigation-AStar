# AI Robot Navigation

A small Pygame grid visualization for comparing A* search and Breadth-First Search (BFS). Place obstacles on the grid, choose an algorithm, and watch the robot move from the top-left start cell to the bottom-right goal.

## Features

- 20 × 20 grid with interactive obstacles
- A* search using Manhattan distance
- BFS for comparison
- Animated path display
- Path length and execution time printed in the terminal

## Requirements

- Python 3
- Pygame

## Setup and run

From the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pygame
python .\main.py
```

The `.venv` directory is the Python environment used to install and run the application. It is separate from the application source files and is ignored by Git.

## Controls

| Input | Action |
| --- | --- |
| Click a grid cell | Add or remove an obstacle |
| `A` | Find and animate a path with A* |
| `B` | Find and animate a path with BFS |
| `Space` | Compare A* and BFS, then animate the A* path |
| `R` | Reset the grid and results |
| `Esc` | Quit |

The start cell is green, the goal is red, obstacles are black, the calculated path is blue, and the robot is yellow. If obstacles block every possible route, the application reports that no path was found.
