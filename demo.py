import numpy as np
from mayavi import mlab

# 定义引力常数
G = 6.67430e-11

# 定义两个质点的位置和质量
mass1 = 1.0e5
pos1 = np.array([0, 0, 0])
mass2 = 2.0e5
pos2 = np.array([1, 1, 1])

# 定义计算势能的函数
def gravitational_potential(mass, position, x, y, z):
    r = np.sqrt((x - position[0])**2 + (y - position[1])**2 + (z - position[2])**2)
    return -G * mass / r

# 定义计算空间网格点的势能函数
def total_potential(x, y, z):
    potential1 = gravitational_potential(mass1, pos1, x, y, z)
    potential2 = gravitational_potential(mass2, pos2, x, y, z)
    return potential1 + potential2

# 设置三维空间的范围和步长
x_range = np.linspace(-2, 2, 100)
y_range = np.linspace(-2, 2, 100)
z_range = np.linspace(-2, 2, 100)

# 创建空间网格点
x, y, z = np.meshgrid(x_range, y_range, z_range)

# 计算每个网格点上的引力势能
potential = total_potential(x, y, z)

# 绘制三维引力势场图
mlab.figure(bgcolor=(1, 1, 1), size=(800, 800))
mlab.contour3d(x, y, z, potential, contours=30, colormap='coolwarm', opacity=0.5)
mlab.points3d(pos1[0], pos1[1], pos1[2], color=(1, 0, 0), scale_factor=0.1, resolution=20)
mlab.points3d(pos2[0], pos2[1], pos2[2], color=(0, 0, 1), scale_factor=0.1, resolution=20)
mlab.axes()
mlab.show()
