import random
import copy
from collections import defaultdict

#  Fitness Function
def calculate_cost(solution, shop):
    distance = 0
    for route in solution.values():
        if not route:
            continue
        prev = shop
        for p in route:
            distance += ((prev.x - p.x)**2 + (prev.y - p.y)**2) ** 0.5
            prev = p
        distance += ((prev.x - shop.x)**2 + (prev.y - shop.y)**2) ** 0.5
    return round(distance, 2)

#  Generate Random Individual 
def generate_random_solution(packages, vehicles):
    solution = defaultdict(list)
    remaining_cap = {v.id: v.capacity for v in vehicles}

    for p in packages:
        random.shuffle(vehicles)
        for v in vehicles:
            if remaining_cap[v.id] >= p.weight:
                solution[v.id].append(p)
                remaining_cap[v.id] -= p.weight
                break
    return solution

#  Crossover Operation
def crossover(parent1, parent2, vehicles):
    child = defaultdict(list)
    assigned = set()

    for v in vehicles:
        p1_route = parent1.get(v.id, [])
        p2_route = parent2.get(v.id, [])

        combined = p1_route[:len(p1_route)//2] + p2_route[len(p2_route)//2:]
        capacity = v.capacity

        for p in combined:
            if p.id not in assigned:
                current_weight = sum(pkg.weight for pkg in child[v.id])
                if current_weight + p.weight <= capacity:
                    child[v.id].append(p)
                    assigned.add(p.id)

    return child

#  Mutation Operation 
def mutate(solution, vehicles, mutation_rate=0.1):
    if random.random() > mutation_rate:
        return solution

    sol = copy.deepcopy(solution)
    v_ids = [v.id for v in vehicles]
    v1, v2 = random.sample(v_ids, 2)
    if not sol[v1]:
        return sol

    pkg = random.choice(sol[v1])
    v2_cap = sum(p.weight for p in sol[v2])
    v2_total = next(v.capacity for v in vehicles if v.id == v2)

    if v2_total - v2_cap >= pkg.weight:
        sol[v1].remove(pkg)
        sol[v2].append(pkg)
    return sol

# ------------------ Main Genetic Algorithm Function ------------------
def run_genetic_algorithm(vehicle_objs, packages, shop, population_size=10, generations=30, mutation_rate=0.1):
    # Step 1: Initial population
    population = [generate_random_solution(packages, vehicle_objs) for _ in range(population_size)]

    # Step 2: Evolution loop
    for _ in range(generations):
        # Sort by fitness (lower distance = better)
        population.sort(key=lambda sol: calculate_cost(sol, shop))
        new_population = population[:2]  # Elitism

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:5], 2)  # Top 5 selection
            child = crossover(parent1, parent2, vehicle_objs)
            child = mutate(child, vehicle_objs, mutation_rate)
            new_population.append(child)

        population = new_population

    # Return best solution
    best = population[0]
    return best
