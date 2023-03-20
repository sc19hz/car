# 定义节点类，包含坐标、g值、h值、父节点和f值
class Node:
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = parent
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f