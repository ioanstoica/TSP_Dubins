from dubins_py import Waypoint, calcDubinsPath, dubins_traj
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing
import matplotlib.pyplot as plt
import numpy as np
import pygad

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

    # Start point
    ax.plot(Wptz[0].x,Wptz[0].y, "ro")

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
    ax.set_title('TSP, length: ' + str(round(total_length)) + 'm' + ', radius: ' + str(r) + 'm')
    ax.set_xlabel(' ')
    ax.set_ylabel('Y')    

def genetic_solve(Wptz, r):
    # Parametrii algoritmului genetic
    num_generations = 100
    num_parents_mating = 4
    sol_per_pop = 50
    num_genes = len(Wptz)
    init_range_low = 0
    init_range_high = 360
    parent_selection_type = "sss"
    keep_parents = 1
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_percent_genes = 10

    if len(Wptz) > 10:
        num_generations = 10
        sol_per_pop = 20


    # Functia de fitness
    def fitness_func(ga_instance, solution, solution_idx):
        # Add the var from solution to Wptz, as the third element in the tuple
        Wptz_temp = [Waypoint(Wptz[i].x, Wptz[i].y, solution[i]) for i in range(len(Wptz))]
        Wptz_temp, total_length = solveTSP(Wptz_temp, r)
        fitness = 1.0 / total_length
        return fitness

    # Creaza instanta algoritmului genetic
    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_func,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes)

    # Ruleaza algoritmul genetic
    ga_instance.run()

    # Returneaza solutia
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    Wptz = [Waypoint(Wptz[i].x, Wptz[i].y, solution[i]) for i in range(len(Wptz))]
    return solveTSP(Wptz, r)

# Rezolvă problema TSP, si ploteaza in ax traseul Dubins
def TSP_Dubins_genetics(Wptz, r, ax):
    Wptz, total_length = genetic_solve(Wptz, r)

    # Start point
    ax.plot(Wptz[0].x,Wptz[0].y, "ro")

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
    ax.set_title('TSP with genetics, length: ' + str(round(total_length)) + 'm' + ', radius: ' + str(r) + 'm')
    ax.set_xlabel(' ')
    ax.set_ylabel('Y')

def main():
    # User's waypoints: [x, y, heading (degrees)] - heading is the angle of the vehicle's orientation where 0 is North, and 180 is South
    nr_points = 10
    Wptz = []
    # fill wptz with points
    for i in range(nr_points):
        Wptz.append(Waypoint(np.random.randint(-10000, 10000), 
                             np.random.randint(-10000, 10000), 
                             np.random.randint(0, 360)))

    # Define the turning radius, try for different values
    radius = np.linspace(50, 100, num=2)

    fig, axs = plt.subplots(len(radius), 2, figsize=(10, 12))
    plt.tight_layout()

    # Pentru fiecare rază de virare, rezolvă problema TSP și generează traseul Dubins
    for t in range(len(radius)):
        TSP_Dubins(Wptz, radius[t], axs[t, 0])
        TSP_Dubins_genetics(Wptz, radius[t], axs[t, 1])
        print("Done for radius: ", radius[t])

    plt.tight_layout()    
    plt.show()


if __name__ == '__main__':
    main()