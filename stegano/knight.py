import random

class KnightTour:
    """
    使用 Warnsdorff 規則的騎士巡遊演算法
    用於在圖像內選取不重複的像素座標
    """
    moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

    def __init__(self, width: int, height: int, seed: int = None):
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)

    def _valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def generate_path(self, start_x: int, start_y: int, length: int) -> list:
        path = [(start_x, start_y)]
        for _ in range(length - 1):
            x, y = path[-1]
            # 找所有合法且未走過的移動
            neighbors = [(x+dx, y+dy) for dx, dy in self.moves if self._valid(x+dx,y+dy) and (x+dx,y+dy) not in path]
            if not neighbors:
                break
            # Warnsdorff: 選擇後續可走動數最少的
            neighbors.sort(key=lambda pos: self._count_onward(pos, path))
            path.append(neighbors[0])
        return path

    def _count_onward(self, pos, path):
        x,y = pos
        cnt = 0
        for dx,dy in self.moves:
            nx,ny = x+dx, y+dy
            if self._valid(nx, ny) and (nx,ny) not in path:
                cnt += 1
        return cnt