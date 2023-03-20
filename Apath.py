import heapq
import numpy as np
import math


def getsin(a1, a2, b1, b2, c1, c2):
    # 计算向量CA和向量CB
    vector_CA = (c1 - a1, c2 - a2)
    vector_CB = (c1 - b1, c2 - b2)

    # 计算向量CA和向量CB的点积
    dot_product = vector_CA[0] * vector_CB[0] + vector_CA[1] * vector_CB[1]

    # 计算向量CA和向量CB的模长
    length_CA = math.sqrt(vector_CA[0] ** 2 + vector_CA[1] ** 2)
    length_CB = math.sqrt(vector_CB[0] ** 2 + vector_CB[1] ** 2)

    # 计算夹角正弦值
    if(length_CA * length_CB==0):
        return 0
    sin_value = dot_product / (length_CA * length_CB)

    return sin_value
# 计算对角线距离的启发式函数
def diagonal_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy)+math.sqrt(2)*min(dx,dy)

def new(a,b,start):

    dig=diagonal_distance(a,b)
    sin=getsin(a[0],a[1],b[0],b[1],start[0],start[1])
    return dig+sin
# 构建无向图的函数，将符合条件的邻近节点连接起来
def build_graph(matrix):
    graph = {}
    for i, node in enumerate(matrix):
        graph[tuple(node)] = []
        for j, neighbor in enumerate(matrix):
            dx = abs(node[0] - neighbor[0])
            dy = abs(node[1] - neighbor[1])
            if i != j and (dx < 30 or dy < 30):
                graph[tuple(node)].append(tuple(neighbor))
    return graph

# A*算法实现
def a_star(graph, start, goal):
    # 初始化open_set，将起点的启发式函数值、已经走过的距离、当前点和路径加入
    open_set = [(diagonal_distance(start, goal), 0, start, [])]
    closed_set = set()

    while open_set:
        _, cost_so_far, current, path = heapq.heappop(open_set)
        if current == goal:
            return path + [current]

        if current not in closed_set:
            closed_set.add(current)
            for neighbor in graph[current]:
                new_cost = cost_so_far + diagonal_distance(current, neighbor)
                heapq.heappush(open_set, (new_cost + new(neighbor, goal,start), new_cost, neighbor, path + [current]))

    return None

class GetPath():
    # getpath()函数，接收输入矩阵、起点和终点坐标，返回从起点到终点的路径
    def getPath(matrix, start, goal):
        graph = build_graph(matrix)
        start = tuple(start)
        goal = tuple(goal)
        path = a_star(graph, start, goal)
        return path

# 示例
# matrix = np.array([[0, 0], [40, 0], [40, 30], [80, 30], [80, 60],[80,240],[200,240]])
# start = np.array([0, 0])
# goal = np.array([80, 60])
#
# path = GetPath.getPath(matrix, start, goal)
# print(path)
