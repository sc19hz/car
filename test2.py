# 创建一个简化的地图，您可以根据需要创建一个350x350的地图
matrix = [
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0]
]

# 定义起点和终点坐标
start = (1, 1)
end = (4, 3)

# 调用getPath函数
path = getPath(matrix, start, end)

# 输出结果
if path:
    print("找到路径:", path)
else:
    print("没有找到路径")
