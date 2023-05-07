import numpy as np
import matplotlib.pyplot as plt
import time

def attractive_potential(x, y, goal):
    k_att = 1.0
    return 0.5 * k_att * np.hypot(goal[0] - x, goal[1] - y)

def repulsive_potential(x, y, obstacle, q_star):
    k_rep = 100.0
    dist = np.hypot(obstacle[0] - x, obstacle[1] - y)
    rep_force = np.where(dist <= q_star, 0.5 * k_rep * (1/dist - 1/q_star)**2, 0)
    return rep_force

def calc_potential_field(grid_size, goal, obstacles, q_star):
    x, y = np.meshgrid(range(grid_size[0]), range(grid_size[1]))
    u_att = attractive_potential(x, y, goal)
    u_rep = np.zeros_like(u_att)

    for obstacle in obstacles:
        u_rep += repulsive_potential(x, y, obstacle, q_star)

    u = u_att + u_rep
    return u

def gradient_descent(start, goal, potential_field, max_iter=10000, alpha=0.1):
    current_position = np.array(start, dtype=np.float64)
    path = [start]

    for _ in range(max_iter):
        gradient_x = potential_field[int(current_position[0]) + 1, int(current_position[1])] - \
                     potential_field[int(current_position[0]) - 1, int(current_position[1])]
        gradient_y = potential_field[int(current_position[0]), int(current_position[1]) + 1] - \
                     potential_field[int(current_position[0]), int(current_position[1]) - 1]
        gradient = np.array([gradient_x, gradient_y])
        current_position -= alpha * gradient
        path.append(current_position.copy())

        if np.linalg.norm(current_position - goal) < 1.0:
            break

    return path

def plot_potential_field(u, grid_size, goal, obstacles, path):
    plt.figure()
    plt.imshow(u.T, origin='lower', cmap='jet', extent=[0, grid_size[0], 0, grid_size[1]])
    plt.colorbar()
    plt.plot(goal[0], goal[1], 'r*', markersize=12)
    for obstacle in obstacles:
        plt.plot(obstacle[0], obstacle[1], 'mo', markersize=8)

    if path is not None:
        path = np.array(path)
        plt.plot(path[:, 0], path[:, 1], 'w--', linewidth=2)

    plt.title('Potential Field')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show(block=False)

grid_size = (30, 30)
goal = (25, 25)
start = (5, 0)
obstacles = [(10, 10), (15, 15), (20, 5)]
q_star = 5

u = calc_potential_field(grid_size, goal, obstacles, q_star)

path = gradient_descent(start, goal, u)

for i in range(len(path)):
    plot_potential_field(u, grid_size, goal, obstacles, path[:i+1])
    plt.pause(0.1)
    if i != len(path) - 1:
        plt.clf()

plt.show()
