from dubins_py import Waypoint, calcDubinsPath, dubins_traj
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing
import matplotlib.pyplot as plt
import numpy as np
import math

def dubins_length(param):
    length = (param.seg_final[0]+param.seg_final[1]+param.seg_final[2])*param.turn_radius
    return length

# Rezolvă problema TSP pentru a minimiza lungimea traseului Dubins
def solveTSP(Wptz, r):
    # Calculează matricea distanțelor
    distance_matrix = []
    for i in range(len(Wptz)):
        row = []
        for j in range(len(Wptz)):
            if i == j:
                row.append(0)
            else:
                param = calcDubinsPath(Wptz[i], Wptz[j], r, 20)
                row.append(dubins_length(param))
        distance_matrix.append(row)
    
    distance_matrix = np.array(distance_matrix)
    # NU vrem sa ne intoarcem la punctul de start
    distance_matrix[:, 0] = 0

    # Solve the TSP problem
    if len(Wptz) < 10:
        permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    else:
        permutation, distance = solve_tsp_simulated_annealing(distance_matrix)

    Wptz = [Wptz[i] for i in permutation]
    return Wptz, distance

# Rezolvă problema TSP, si ploteaza in ax traseul Dubins
def TSP_Dubins(Wptz, r, ax):
    Wptz, total_length = solveTSP(Wptz, r)

    # Calculează traseul Dubins
    for i in range(len(Wptz)-1):
        param = calcDubinsPath(Wptz[i], Wptz[i+1], r, 20)
        path = dubins_traj(param,1)

        # Plot the results
        ax.plot(Wptz[i].x,Wptz[i].y,'kx')
        ax.plot(Wptz[i+1].x,Wptz[i+1].y,'kx')
        ax.plot(path[:,0],path[:,1],'b-')

    ax.grid(True)
    ax.axis("equal")
    ax.set_title('Best trajectory, length: ' + str(round(total_length)) + 'm' + ', radius: ' + str(r) + 'm')
    ax.set_xlabel(' ')
    ax.set_ylabel('Y')

def main():
    # User's waypoints: [x, y, heading (degrees)] - heading is the angle of the vehicle's orientation where 0 is North, and 180 is South
    # Wptz = [Waypoint(0,0,0), 
    #         Waypoint(6000,7000,260), 
    #         Waypoint(1000,15000,180), 
    #         Waypoint(-5000,5000,270), 
    #         Waypoint(-5000,-5000,0),
    #         Waypoint(0,10000,0)]

    nr_points = 7

    # fill wptz with 20 points
    Wptz = []
    for i in range(nr_points):
        Wptz.append(Waypoint(np.random.randint(-10000, 10000), 
                             np.random.randint(-10000, 10000), 
                             np.random.randint(0, 360)))

    # Define the turning radius, try for different values
    radius = np.linspace(10, 150, num=6)

    # Calculăm numărul de rânduri necesar pentru 2 coloane
    nr_randuri = math.ceil(len(radius) / 2)

    fig, axs = plt.subplots(nr_randuri, 2, figsize=(10, 12))
    plt.tight_layout()

    # Pentru fiecare rază de virare, rezolvă problema TSP și generează traseul Dubins
    for t in range(len(radius)):
        TSP_Dubins(Wptz, radius[t], axs[t//2, t%2])

    plt.tight_layout()    
    plt.show()


if __name__ == '__main__':
    main()