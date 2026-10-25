
import pygame
import sys
import time

from algorithms import astar, bfs

# Initialize Pygame
pygame.init()

# Window settings
CELL_SIZE = 30
ROWS = 20
COLS = 20
HEADER_HEIGHT = 90

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + HEADER_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Robot Navigation and Path Planning")

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
GREEN = (50, 200, 100)
RED = (230, 70, 70)
BLUE = (70, 130, 255)
YELLOW = (255, 200, 0)
PURPLE = (160, 80, 220)

# Fonts
font = pygame.font.SysFont("Arial", 17)
small_font = pygame.font.SysFont("Arial", 15)

# Start and destination
start = (0, 0)
goal = (ROWS - 1, COLS - 1)

# Project state
obstacles = set()
path = []
robot_pos = [start]
algorithm_name = "A*"
status = "Select obstacles, then press SPACE"
results = {}

clock = pygame.time.Clock()


def draw_grid():
    screen.fill(WHITE)

    # Instructions
    message = font.render(
        "Click: Obstacles | SPACE: Compare | A: A* | B: BFS",
        True,
        BLACK
    )
    screen.blit(message, (8, 8))

    message2 = font.render(
        "R: Reset | ESC: Quit",
        True,
        BLACK
    )
    screen.blit(message2, (8, 32))

    message3 = small_font.render(status, True, PURPLE)
    screen.blit(message3, (8, 57))

    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):

            cell = (row, col)
            x = col * CELL_SIZE
            y = row * CELL_SIZE + HEADER_HEIGHT

            if cell in obstacles:
                color = BLACK
            elif cell == start:
                color = GREEN
            elif cell == goal:
                color = RED
            elif cell in path:
                color = BLUE
            else:
                color = WHITE

            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                GRAY,
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

    # Draw moving robot
    row, col = robot_pos[0]

    center = (
        col * CELL_SIZE + CELL_SIZE // 2,
        row * CELL_SIZE + HEADER_HEIGHT + CELL_SIZE // 2
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        center,
        CELL_SIZE // 3
    )

    pygame.display.flip()


def animate_robot(found_path):
    """Animate the robot along a calculated path."""

    global running, status

    for cell in found_path:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return False

        robot_pos[0] = cell
        draw_grid()
        pygame.time.delay(100)

    return True


def run_algorithm(name):
    """Run one algorithm and display its result."""

    global path, algorithm_name, status

    if name == "A*":
        algorithm = astar
    else:
        algorithm = bfs

    start_time = time.perf_counter()

    found_path = algorithm(
        start, goal, ROWS, COLS, obstacles
    )

    elapsed = time.perf_counter() - start_time

    path = found_path
    algorithm_name = name
    robot_pos[0] = start

    results[name] = {
        "path_length": len(found_path) - 1 if found_path else None,
        "time": elapsed
    }

    if found_path:
        status = f"{name}: path found, {len(found_path) - 1} moves"
        print(f"\n{name} results")
        print("Path length:", len(found_path) - 1, "moves")
        print(f"Execution time: {elapsed:.6f} seconds")

        draw_grid()
        return animate_robot(found_path)

    status = f"{name}: no path found"
    print(f"\n{name}: No path found.")

    draw_grid()
    return True


def compare_algorithms():
    """Compare A* and BFS on the same grid."""

    global path, robot_pos, algorithm_name, status

    print("\n========== ALGORITHM COMPARISON ==========")

    for name, algorithm in [("A*", astar), ("BFS", bfs)]:

        start_time = time.perf_counter()

        found_path = algorithm(
            start, goal, ROWS, COLS, obstacles
        )

        elapsed = time.perf_counter() - start_time

        results[name] = {
            "path_length": len(found_path) - 1 if found_path else None,
            "time": elapsed
        }

        print(f"\n{name}")
        print("Path length:",
              len(found_path) - 1 if found_path else "No path")
        print(f"Execution time: {elapsed:.6f} seconds")

    # Animate A* path after comparing both algorithms
    path = astar(
        start, goal, ROWS, COLS, obstacles
    )

    algorithm_name = "A*"
    robot_pos[0] = start

    if path:
        status = "Comparison complete: animating A*"
        draw_grid()

        if not animate_robot(path):
            return

        status = "A* reached the destination"
    else:
        status = "No path exists for either algorithm"

    draw_grid()


running = True

while running:

    draw_grid()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                obstacles.clear()
                path.clear()
                robot_pos[0] = start
                results.clear()
                status = "Grid reset"
                print("\nGrid reset.")

            elif event.key == pygame.K_SPACE:
                compare_algorithms()

            elif event.key == pygame.K_a:
                run_algorithm("A*")

            elif event.key == pygame.K_b:
                run_algorithm("BFS")

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            if mouse_y >= HEADER_HEIGHT:

                col = mouse_x // CELL_SIZE
                row = (mouse_y - HEADER_HEIGHT) // CELL_SIZE

                cell = (row, col)

                if (
                    0 <= row < ROWS
                    and 0 <= col < COLS
                    and cell != start
                    and cell != goal
                ):

                    if cell in obstacles:
                        obstacles.remove(cell)
                    else:
                        obstacles.add(cell)

                    path.clear()
                    robot_pos[0] = start
                    status = "Obstacles changed; run an algorithm"

    clock.tick(60)

pygame.quit()
sys.exit()
