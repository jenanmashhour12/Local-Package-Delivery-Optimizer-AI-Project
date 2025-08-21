import copy
import random
import math
from solution import Solution  

# calculates the total travel distance for a solution
def calculate_cost(solution):
    return solution.total_distance()

# assigning packages randomly to vehicles
def generate_initial_solution(packages, vehicles_template):
    vehicles = copy.deepcopy(vehicles_template)  # to avoid modifying the original ones

    #initializing each vehicle's route and capacity
    for v in vehicles:
        v.route = []
        v.remaining_capacity = v.capacity

    #try assigning each package to a random vehicle that has enough capacity
    for pkg in packages:
        print(f" Trying to assign {pkg.id} (weight: {pkg.weight})")
        random.shuffle(vehicles)  # Randomize order to increase diversity in assignment

        assigned = False
        for v in vehicles:
            if v.remaining_capacity >= pkg.weight:
                v.route.append(pkg)
                v.remaining_capacity -= pkg.weight
                print(f"Assigned to Vehicle {v.id} (Remaining: {v.remaining_capacity}kg)")
                assigned = True
                break

        if not assigned:
            # If no vehicle has enough space, the package remains unassigned
            print(f"Could NOT assign {pkg.id} to any vehicle!")

    return Solution(vehicles)

# recalculates the remaining capacity for each vehicle based on current route
def recompute_remaining_capacity(vehicles):
    for v in vehicles:
        v.remaining_capacity = v.capacity - sum(pkg.weight for pkg in v.route)

# generating neighboring solution by attempting to move one package between two vehicles
def generate_neighbor(current_solution):
    new_solution = copy.deepcopy(current_solution) 

    # choose different vehicles randomly
    v1, v2 = random.sample(new_solution.vehicles, 2)

    #proceed if the first vehicle has packages to move
    if not v1.route:
        return new_solution  # no neighbor will be generated if v1 is empty

    pkg = random.choice(v1.route)  # choose a random package from v1

    # check if v2 has enough space to accept the package
    if sum(p.weight for p in v2.route) + pkg.weight <= v2.capacity:
        v1.route.remove(pkg)
        v2.route.append(pkg)

        # recalculate capacities after the moving
        recompute_remaining_capacity(new_solution.vehicles)

    return new_solution

# show any packages that were not assigned to any vehicle
def find_unassigned_packages(vehicles, all_packages):
    assigned_ids = {p.id for v in vehicles for p in v.route}
    unassigned = [p for p in all_packages if p.id not in assigned_ids]
    return unassigned

# simulated annealing SA function for route optimization
def simulated_annealing(packages, vehicles, initial_temp=1000, cooling_rate=0.95, stopping_temp=1):
    current = generate_initial_solution(packages, vehicles)  
    best = copy.deepcopy(current)  #track the best solution found
    T = initial_temp  #temperature parameter

    while T > stopping_temp:
        neighbor = generate_neighbor(current) 
        cost_curr = calculate_cost(current)
        cost_neigh = calculate_cost(neighbor)
        delta = cost_neigh - cost_curr  

        #accepting the neighbor if it's better or exploration
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            if calculate_cost(current) < calculate_cost(best):
                best = copy.deepcopy(current)  # updating best if improvement found

        T *= cooling_rate  

    return best  # return the best solution found
