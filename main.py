from dubins_py import Waypoint, calcDubinsPath, dubins_traj
from python_tsp.exact import solve_tsp_dynamic_programming
import matplotlib.pyplot as plt
import numpy as np

def dubins_length(param):
    length = (param.seg_final[0]+param.seg_final[1]+param.seg_final[2])*param.turn_radius
    return length

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
    
    print(distance_matrix)
    distance_matrix = np.array(distance_matrix)
    # NU vrem sa ne intoarcem la punctul de start
    distance_matrix[:, 0] = 0

    # Solve the TSP problem
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    print(permutation, distance)


    Wptz = [Wptz[i] for i in permutation]
    return Wptz

def main():
    # User's waypoints: [x, y, heading (degrees)] - heading is the angle of the vehicle's orientation where 0 is North
    Wptz = [Waypoint(0,0,0), 
            Waypoint(6000,7000,260), 
            Waypoint(1000,15000,180), 
            Waypoint(-5000,5000,270), 
            Waypoint(0,10000,0)]

    radius = [50, 100, 150, 200]


    fig, axs = plt.subplots(len(radius), 1, figsize=(10, 12))

    for t in range(len(radius)):
        # Rezolvă problema TSP, reordonând punctele pentru a minimiza lungimea traseului
        r = radius[t]
        Wptz = solveTSP(Wptz, r)

        # Calculează traseul Dubins
        i = 0
        total_length = 0  # Inițializează o variabilă pentru a stoca lungimea totală a traseului
        while i<len(Wptz)-1:
            param = calcDubinsPath(Wptz[i], Wptz[i+1], r, 20)
            path = dubins_traj(param,1)

            # Calculează lungimea totală a traseului
            length = dubins_length(param)
            total_length += length  # Adaugă lungimea segmentului curent la lungimea totală
            print('Segment Length: ',length)
    

            # Plot the results
            axs[t].plot(Wptz[i].x,Wptz[i].y,'kx')
            axs[t].plot(Wptz[i+1].x,Wptz[i+1].y,'kx')
            axs[t].plot(path[:,0],path[:,1],'b-')
            i+=1

        # Afișează lungimea totală a traseului
        print("Lungimea totală a drumului Dubins este:", total_length, "metri")

        axs[t].grid(True)
        axs[t].axis("equal")
        axs[t].set_title('Best trajectory, length: ' + str(round(total_length)) + 'm' + ', radius: ' + str(r) + 'm')
        axs[t].set_xlabel('X')
        axs[t].set_ylabel('Y')
        axs[t].legend()

    plt.tight_layout()    
    plt.show()


if __name__ == '__main__':
    main()