import numpy as np
import matplotlib.pyplot as plt
import copy
from celluloid import Camera  # Used to save animated gifs, install with 'pip install celluloid'

## Initialize vehicle parameters
d = 3.5  # Standard road width

W = 1.6  # Vehicle width

L = 4.7  # Vehicle length

P0 = np.array([0, - d / 2, 1, 1]) # Vehicle starting position, representing x, y, vx, vy

Pg = np.array([99, d / 2, 0, 0]) # Goal position

# Obstacle positions
Pobs = np.array([
    [15, 7 / 4, 0, 0],
    [30, - 3 / 2, 0, 0],
    [45, 3 / 2, 0, 0],
    [60, - 3 / 4, 0, 0],
    [80, 3/2, 0, 0]])

P = np.vstack((Pg,Pobs))  # Combine goal and obstacle positions

Eta_att = 5  # Attraction gain coefficient

Eta_rep_ob = 15  # Repulsion gain coefficient for obstacles

Eta_rep_edge = 50   # Road edge repulsion gain coefficient

d0 = 20  # Maximum distance at which obstacles have an effect

num = P.shape[0] # Total number of obstacles and goal

len_step = 0.5 # Step size

n=1

Num_iter = 300  # Maximum number of iterations in the loop
path = []  # Save the coordinates of each point the vehicle passes through
delta = np.zeros((num,2)) # Save the direction vector from the vehicle to obstacles, and from the vehicle to the goal
dists = [] # Save the distance from the vehicle to obstacles and to the goal
unite_vec = np.zeros((num,2)) # Save the unit direction vector from the vehicle to obstacles, and from the vehicle to the goal

F_rep_ob = np.zeros((len(Pobs),2))  # Store the repulsive force from each obstacle to the vehicle, with direction
v=np.linalg.norm(P0[2:4]) # Set vehicle speed as a constant value
## ***************Initialization finished, start the main loop******************
Pi = P0[0:2]  # Current vehicle position
for i in range(Num_iter):
    if ((Pi[0] - Pg[0]) ** 2 + (Pi[1] - Pg[1]) ** 2) ** 0.5 < 1:
        break
    dists = []
    path.append(Pi)
    # Calculate the unit direction vector from the vehicle to obstacles
    for j in range(len(Pobs)):
        delta[j] = Pi[0:2] - Pobs[j, 0:2]
        dists.append(np.linalg.norm(delta[j]))
        unite_vec[j] = delta[j] / dists[j]
    # Calculate the unit direction vector from the vehicle to the goal
    delta[len(Pobs)] = Pg[0:2] - Pi[0:2]
    dists.append(np.linalg.norm(delta[len(Pobs)]))
    unite_vec[len(Pobs)] = delta[len(Pobs)] / dists[len(Pobs)]

    ## Calculate attraction force
    F_att = Eta_att * dists[len(Pobs)] * unite_vec[len(Pobs)]

    ## Calculate repulsion force
    # Add goal adjustment factor (i.e., distance from vehicle to goal) to the original repulsion potential function so that the repulsion force is also 0 when the vehicle reaches the goal
    for j in range(len(Pobs)):
        if dists[j] >= d0:
            F_rep_ob[j] = np.array([0, 0])
        else:
            # Obstacle repulsion force 1, direction from obstacle to vehicle
            F_rep_ob1_abs = Eta_rep_ob * (1 / dists[j] - 1 / d0) * (dists[len(Pobs)]) ** n / dists[j] ** 2  # Repulsion force magnitude
            F_rep_ob1 = F_rep_ob1_abs * unite_vec[j]  # Repulsion force vector
            # Obstacle repulsion force 2, direction from vehicle to goal
            F_rep_ob2_abs = n / 2 * Eta_rep_ob * (1 / dists[j] - 1 / d0) ** 2 * (dists[len(Pobs)]) ** (n - 1)  # Repulsion force magnitude
            F_rep_ob2 = F_rep_ob2_abs * unite_vec[len(Pobs)]  # Repulsion force vector
            # Improved obstacle repulsion force calculation
            # F_rep_ob[j] = F_rep_ob1 + F_rep_ob2
            F_rep_ob[j] = F_rep_ob1

    # Add road edge repulsion potential field, select the corresponding repulsion function based on the current vehicle position
    if Pi[1] > - d + W / 2 and Pi[1] <= - d / 2:
        F_rep_edge = [0, Eta_rep_edge * v * np.exp(-d / 2 - Pi[1])]  # Lower road edge repulsion field, direction pointing to positive y-axis
    elif Pi[1] > - d / 2 and Pi[1] <= - W / 2:
        F_rep_edge = np.array([0, 1 / 3 * Eta_rep_edge * Pi[1] ** 2])
    elif Pi[1] > W / 2 and Pi[1] <= d / 2:
        F_rep_edge = np.array([0, - 1 / 3 * Eta_rep_edge * Pi[1] ** 2])
    elif Pi[1] > d / 2 and Pi[1] <= d - W / 2:
        F_rep_edge = np.array([0, Eta_rep_edge * v * (np.exp(Pi[1] - d / 2))])

        ## Calculate total force and direction
        # F_rep = np.sum(F_rep_ob, axis=0) + F_rep_edge
    F_rep = np.sum(F_rep_ob, axis=0)
    F_sum = F_att + F_rep

    UnitVec_Fsum = 1 / np.linalg.norm(F_sum) * F_sum
    # Calculate the next position of the vehicle
    Pi = copy.deepcopy(Pi + len_step * UnitVec_Fsum)

path.append(Pg[0:2])  # Add the goal point to the path as well
path = np.array(path)  # Convert to numpy

## Plotting
fig = plt.figure(1)
plt.axis([-10, 100, -15, 15])
camera = Camera(fig)
len_line = 100
# Draw the gray road surface
GreyZone = np.array([[- 5, - d - 0.5], [- 5, d + 0.5],
                     [len_line, d + 0.5], [len_line, - d - 0.5]])
for i in range(len(path)):
    plt.fill(GreyZone[:, 0], GreyZone[:, 1], 'gray')
    plt.fill(np.array([P0[0], P0[0], P0[0] - L, P0[0] - L]), np.array([- d /
                                                                       2 - W / 2, - d / 2 + W / 2, - d / 2 + W / 2,
                                                                       - d / 2 - W / 2]), 'b')
    # Draw the dividing line
    plt.plot(np.array([- 5, len_line]), np.array([0, 0]), 'w--')

    plt.plot(np.array([- 5, len_line]), np.array([d, d]), 'w')

    plt.plot(np.array([- 5, len_line]), np.array([- d, - d]), 'w')

    # Set the coordinate axis display range
    # plt.axis('equal')
    # plt.gca().set_aspect('equal')
    # Draw the path
    plt.plot(Pobs[:, 0], Pobs[:, 1], 'ro')  # Obstacle positions

    plt.plot(Pg[0], Pg[1], 'gv')  # Goal position

    plt.plot(P0[0], P0[1], 'bs')  # Starting position
    plt.plot(path[0:i, 0], path[0:i, 1], 'k')  # Path points
    plt.pause(0.001)
    camera.snap()
animation = camera.animate()
animation.save('imp_1.gif')

