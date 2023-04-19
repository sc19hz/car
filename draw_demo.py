import pygame
import sys

# 初始化pygame
pygame.init()

# 设置窗口大小、格子大小和颜色
WINDOW_SIZE = (800, 800)
GRID_SIZE = 20
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
# 创建窗口和设置标题
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("20x20 Grid")

# 生成初始网格
grid = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# 渲染网格
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[row][col], pygame.Rect(col * (WINDOW_SIZE[0] // GRID_SIZE), row * (WINDOW_SIZE[1] // GRID_SIZE), (WINDOW_SIZE[0] // GRID_SIZE), (WINDOW_SIZE[1] // GRID_SIZE)), 0)
    for x in range(0, WINDOW_SIZE[0], WINDOW_SIZE[0] // GRID_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, WINDOW_SIZE[1]), 1)
    for y in range(0, WINDOW_SIZE[1], WINDOW_SIZE[1] // GRID_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (WINDOW_SIZE[0], y), 1)

# 主循环
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            col = mouse_x // (WINDOW_SIZE[0] // GRID_SIZE)
            row = mouse_y // (WINDOW_SIZE[1] // GRID_SIZE)

            # 左键点击变为青色
            if event.button == 1:
                grid[row][col] = CYAN
            # 右键点击变为淡绿色
            elif event.button == 3:
                grid[row][col] = LIGHT_GREEN
            elif event.button == 2:
                grid[row][col] = RED
pygame.quit()
