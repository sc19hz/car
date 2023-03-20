import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
class View():
    def view(matrix):
        # 创建一个空的无向图
        G = nx.Graph()

        # 添加结点
        for i, coord in enumerate(matrix):
            G.add_node(i, pos=(coord[0], coord[1]))

        # 添加边
        for i, coord1 in enumerate(matrix):
            for j, coord2 in enumerate(matrix):
                if i != j:
                    if abs(coord1[0] - coord2[0]) != 30 and abs(coord1[1] - coord2[1]) != 30:
                        G.add_edge(i, j)

        # 可视化图
        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, node_color='red', edge_color='blue', with_labels=False, node_size=20, width=0.01)
        plt.show()