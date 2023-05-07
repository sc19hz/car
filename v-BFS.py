import pygame
import math
import heapq

# 配置参数
WIDTH = 800
GRID_SIZE = 20
SQUARE_SIZE = WIDTH // GRID_SIZE
FPS = 60

# 颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Grid:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []

    def make_visited(self):
        self.color = YELLOW

    def get_pos(self):
        return self.row, self.col

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.row * SQUARE_SIZE, self.col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # 上
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_barrier():  # 下
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # 左
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_barrier():  # 右
            self.neighbors.append(grid[self.row][self.col + 1])

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def best_first_search(draw, grid, start, end):
    open_set = [(0, 0, start)]  # 添加顺序值作为第二个元素
    visited = set()
    path = {}
    count = 0  # 添加一个计数器

    while open_set:
        current = heapq.heappop(open_set)[2]  # 获取第三个元素，即当前的Grid实例
        visited.add(current)

        if current == end:
            path_length = reconstruct_path(path, end, draw)  # 将结果赋值给 path_length 变量
            start.make_start()
            end.make_end()
            return True, len(visited), path_length  # 返回结果

        for neighbor in current.neighbors:
            if neighbor not in visited:  # 只有邻居节点不在访问集合中时才添加
                path[neighbor] = current
                count += 1  # 每次遍历时递增计数器
                heapq.heappush(open_set, (h(neighbor.get_pos(), end.get_pos()), count, neighbor))  # 使用计数器作为第二个元素
                visited.add(neighbor)
                draw()

    return False, len(visited), 0  # 如果未找到路径，返回路径长度为0



def reconstruct_path(path, end, draw):
    current = end
    length = 0
    while current in path:
        current = path[current]
        length += 1
        current.make_path()
        draw()
    return length






def create_grid():
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            grid[i].append(Grid(i, j))
    return grid

def draw_grid(win):
    for i in range(GRID_SIZE):
        pygame.draw.line(win, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
        for j in range(GRID_SIZE):
            pygame.draw.line(win, BLACK, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, WIDTH))

def draw_window(win, grid):
    win.fill(WHITE)
    for row in grid:
        for grid_item in row:
            grid_item.draw(win)
    draw_grid(win)
    pygame.display.update()

def get_clicked_position(position):
    row, col = position
    return row // SQUARE_SIZE, col // SQUARE_SIZE

def main(win):
    grid = create_grid()
    start = None
    end = None
    run = True

    while run:
        draw_window(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # 左键
                position = pygame.mouse.get_pos()
                row, col = get_clicked_position(position)
                grid_item = grid[row][col]
                if not start and grid_item != end:
                    start = grid_item
                    start.make_start()
                elif not end and grid_item != start:
                    end = grid_item
                    end.make_end()
                elif grid_item != start and grid_item != end:
                    grid_item.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for grid_item in row:
                            grid_item.update_neighbors(grid)
                    found, visited_nodes, path_length = best_first_search(lambda: draw_window(win, grid), grid, start,
                                                                          end)  # 更新为三个变量
                    print("路径是否找到：", found)
                    print("访问的节点数：", visited_nodes)
                    print("路径长度：", path_length)

                if event.key == pygame.K_r:  # 重置
                    start = None
                    end = None
                    grid = create_grid()

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Best First Search Visualization")
    main(WIN)
