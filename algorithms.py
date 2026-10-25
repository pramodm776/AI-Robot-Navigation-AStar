
import heapq
from collections import deque


def heuristic(cell, goal):
    """Calculate Manhattan distance."""
    row1, col1 = cell
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


def get_neighbors(cell, rows, cols, obstacles):
    """Get valid neighboring cells."""
    row, col = cell

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    neighbors = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbor = (new_row, new_col)

            if neighbor not in obstacles:
                neighbors.append(neighbor)

    return neighbors


def reconstruct_path(came_from, current):
    """Reconstruct the path from goal to start."""
    path = []

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


def astar(start, goal, rows, cols, obstacles):
    """Find a shortest path using A*."""

    if start in obstacles or goal in obstacles:
        return []

    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(start, goal), start))

    came_from = {start: None}
    g_score = {start: 0}

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(
            current, rows, cols, obstacles
        ):
            new_cost = g_score[current] + 1

            if new_cost < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = new_cost

                f_score = new_cost + heuristic(neighbor, goal)

                heapq.heappush(
                    priority_queue,
                    (f_score, neighbor)
                )

    return []


def bfs(start, goal, rows, cols, obstacles):
    """Find a shortest path using Breadth-First Search."""

    if start in obstacles or goal in obstacles:
        return []

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(
            current, rows, cols, obstacles
        ):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    return []
