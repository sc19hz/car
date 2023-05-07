import numpy as np
import matplotlib.pyplot as plt
import copy
from celluloid import Camera  # Used for saving animations, install with pip install celluloid

## Initialize car parameters
d = 3.5  # Standard road width

W = 1.6  # Car width

L = 4.7  # Car length

P0 = np.array([0, -d / 2, 1, 1]) # Initial position of the car, representing x, y, vx, vy

Pg = np.array([99, d / 8, 0, 0]) # Target position

# Obstacle positions
Pobs = np.array([
    [15, 7 / 4, 0, 0],
    [30, - 3 / 2, 0, 0],
    [45, 3 / 2, 0, 0],
    [60, - 3 / 4, 0, 0],
    [80, 3/2, 0, 0]])

P = np.vstack((Pg, Pobs))  # Combine target position and obstacle positions

Eta_att = 5  # Attraction gain coefficient

Eta_rep_ob = 15  # Repulsion gain coefficient for obstacles

Eta_rep_edge = 50   # Repulsion gain coefficient for road edges

d0 = 20  # Maximum distance of obstacle influence

num = P.shape[0] # Total number of obstacles and target

len_step = 0.5 # Step length

n = 1

Num_iter = 300  # Maximum number of loop iterations
path = []  # Save the coordinates of each point the car passes through
delta = np.zeros((num, 2)) # Save the direction vector of the car's current position to the obstacle, pointing to the car; save the direction vector of the car's current position to the target point, pointing to the target point
dists = [] # Save the distance between the car's current position and the obstacles and the distance between the car's current position and the target point
unite_vec = np.zeros((num, 2)) # Save the unit direction vector of the car's current position to the obstacle, pointing to the car; save the unit direction vector of the car's current position to the target point, pointing to the target point

F_rep_ob = np.zeros((len(Pobs), 2))  # Store the repulsive force from each obstacle to the car, with direction
v = np.linalg.norm(P0[2:4]) # Set the car's speed to a constant value
## *************** Initialization finished, start main loop ******************
Pi = P0[0:2]  # Current car position
# count = 0
for i in range(Num_iter):
    if ((Pi[0] - Pg[0]) ** 2 + (Pi[1] - Pg[1]) ** 2) ** 0.5 < 1:
        break
    dists = []
    path.append(Pi)
    # Calculate the unit direction vector of the car's current position to the obstacle
    for j in range(len(Pobs)):
        delta[j] = Pi[0:2] - Pobs[j, 0:2]
        dists.append(np.linalg.norm(delta[j]))
        unite_vec[j] = delta[j] / dists[j]
    # Calculate the unit direction vector of the car's current position to the target
    delta[len(Pobs)] = Pg[0:2] - Pi[0:2]
    dists.append(np.linalg.norm(delta[len(Pobs)]))
    unite_vec[len(Pobs)] = delta[len(Pobs)] / dists[len(Pobs)]

    ## Calculate attraction
    F_att = Eta_att * dists[len(Pobs)] * unite_vec[len(Pobs)]

    ## Calculate repulsion
    # Add target adjustment factor (i.e., distance from car to target) to the original repulsive potential function so that the repulsive force also becomes 0 after the car reaches the target
    for j in range(len(Pobs)):
        if dists[j] >= d0:
            F_rep_ob[j] = np.array([0, 0])
        else:
            # Repulsive force 1 from obstacle, direction from obstacle to car
            F_rep_ob1_abs = Eta_rep_ob * (1 / dists[j] - 1 / d0) * (dists[len(Pobs)]) ** n / dists[j] ** 2  # Repulsive force magnitude
            F_rep_ob1 = F_rep_ob1_abs * unite_vec[j]  # Repulsive force vector
            # Repulsive force 2 from obstacle, direction from car to target
            F_rep_ob2_abs = n / 2 * Eta_rep_ob * (1 / dists[j] - 1 / d0) ** 2 * (dists[len(Pobs)]) ** (n - 1)  # Repulsive force magnitude
            F_rep_ob2 = F_rep_ob2_abs * unite_vec[len(Pobs)]  # Repulsive force vector
            # Improved obstacle repulsive force calculation
            F_rep_ob[j] = F_rep_ob1 + F_rep_ob2

    # Add road edge repulsive potential field, select corresponding repulsive function based on car's current position
    if Pi[1] > - d + W / 2 and Pi[1] <= - d / 2:
        F_rep_edge = [0, Eta_rep_edge * v * np.exp(-d / 2 - Pi[1])]  # Lower road edge repulsive potential field, direction pointing to positive y-axis
    elif Pi[1] > - d / 2 and Pi[1] <= - W / 2:
        F_rep_edge = np.array([0, 1 / 3 * Eta_rep_edge * Pi[1] ** 2])
    elif Pi[1] > W / 2 and Pi[1] <= d / 2:
        F_rep_edge = np.array([0, - 1 / 3 * Eta_rep_edge * Pi[1] ** 2])
    elif Pi[1] > d / 2 and Pi[1] <= d - W / 2:
        F_rep_edge = np.array([0, Eta_rep_edge * v * (np.exp(Pi[1] - d / 2))])

        ## Calculate total force and direction
    F_rep = np.sum(F_rep_ob, axis=0) + F_rep_edge

    F_sum = F_att + F_rep

    UnitVec_Fsum = 1 / np.linalg.norm(F_sum) * F_sum
    # Calculate the next position of the car
    Pi = copy.deepcopy(Pi + len_step * UnitVec_Fsum)

path.append(Pg[0:2])  # Finally, add the target point to the path
path = np.array(path)  # Convert to numpy

## Plot
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
    # Draw dividing lines
    plt.plot(np.array([- 5, len_line]), np.array([0, 0]), 'w--')

    plt.plot(np.array([- 5, len_line]), np.array([d, d]), 'w')

    plt.plot(np.array([- 5, len_line]), np.array([- d, - d]), 'w')

    # Set the coordinate axis display range
    plt.plot(Pobs[:, 0], Pobs[:, 1], 'ro')  # Obstacle positions

    plt.plot(Pg[0], Pg[1], 'gv')  # Target position

    plt.plot(P0[0], P0[1], 'bs')  # Starting position
    plt.plot(path[0:i, 0], path[0:i, 1], 'k')  # Path points
    plt.pause(0.001)
    camera.snap()
animation = camera.animate()
animation.save('imp_2.gif')
