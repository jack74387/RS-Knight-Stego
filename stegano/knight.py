# knight_path.py

import random

class KnightTour:
    moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

    def __init__(self, width: int, height: int, seed: int = None):
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)

    def _valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def generate_path(self, start_x: int, start_y: int, length: int, used: set = None, max_attempts: int = 1000) -> list:
        if used is None:
            used = set()

        attempts = 0
        while attempts < max_attempts:
            path = []
            visited = set()
            x, y = start_x, start_y
            path.append((x, y))
            visited.add((x, y))
            for _ in range(length - 1):
                neighbors = [
                    (x+dx, y+dy) for dx, dy in self.moves
                    if self._valid(x+dx, y+dy)
                    and (x+dx, y+dy) not in visited
                    and (x+dx, y+dy) not in used
                ]
                if not neighbors:
                    break
                neighbors.sort(key=lambda pos: self._count_onward(pos, visited | used))
                x, y = neighbors[0]
                path.append((x, y))
                visited.add((x, y))

            if len(path) == length:
                return path
            attempts += 1

        raise RuntimeError("Failed to generate non-overlapping Knight path after many attempts")

    def _count_onward(self, pos, visited):
        x, y = pos
        cnt = 0
        for dx, dy in self.moves:
            nx, ny = x+dx, y+dy
            if self._valid(nx, ny) and (nx, ny) not in visited:
                cnt += 1
        return cnt
