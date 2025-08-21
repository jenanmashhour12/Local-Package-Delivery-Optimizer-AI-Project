import math
from collections import defaultdict
from vehicle import Vehicle
from package import Package
from GA_algo import run_genetic_algorithm  # UPDATED import
from SA_algo import simulated_annealing
from plot import plot_routes_sa, plot_routes_ga

def calculate_cost(solution, shop):
    distance = 0
    for route in solution.values():
        if not route:
            continue
        prev = shop
        for p in route:
            distance += math.dist((prev.x, prev.y), (p.x, p.y))
            prev = p
        distance += math.dist((prev.x, prev.y), (shop.x, shop.y))
    return round(distance, 2)

# Main optimization interface
def run_optimization(vehicle_caps, packages, algorithm):
    vehicles = [Vehicle(i + 1, cap) for i, cap in enumerate(vehicle_caps)]
    package_objs = [Package(f"Package {i+1}", x, y, w, p) for i, (x, y, w, p) in enumerate(packages)]
    shop = Package("Shop", 0, 0, 0, 0)

    if algorithm == "ga":
        # Call GA function (with crossover + mutation)
        best_solution = run_genetic_algorithm(
            vehicle_objs=vehicles,
            packages=package_objs,
            shop=shop,
            population_size=10,
            generations=30,
            mutation_rate=0.1
        )

        # Prepare output
        total_distance = calculate_cost(best_solution, shop)

        assignments = {}
        remaining = {}
        for v in vehicles:
            assigned = [p.id for p in best_solution[v.id]]
            assignments[f"Vehicle {v.id}"] = assigned
            used = sum(p.weight for p in best_solution[v.id])
            remaining[f"Vehicle {v.id}"] = round(v.capacity - used, 2)

        all_ids = {p.id for p in package_objs}
        assigned_ids = {p.id for plist in best_solution.values() for p in plist}
        undelivered = list(all_ids - assigned_ids)

        image_path = plot_routes_ga(best_solution, save_path="static/ga_plot.png")

        return {
            "algorithm": "GA",
            "distance": total_distance,
            "routes": assignments,
            "remaining": remaining,
            "undelivered": undelivered,
            "plot_image": "ga_plot.png"
        }

    else:
        # Run Simulated Annealing
        solution = simulated_annealing(package_objs, vehicles)
        image_path = plot_routes_sa(solution, save_path="static/sa_plot.png")

        assignments = {}
        remaining = {}
        for v in solution.vehicles:
            assigned = [p.id for p in v.route]
            assignments[f"Vehicle {v.id}"] = assigned
            remaining[f"Vehicle {v.id}"] = round(v.remaining_capacity, 2)

        undelivered = [p.id for p in solution.unassigned_packages] if hasattr(solution, 'unassigned_packages') else []

        return {
            "algorithm": "SA",
            "distance": round(solution.total_distance(), 2),
            "routes": assignments,
            "remaining": remaining,
            "undelivered": undelivered,
            "plot_image": "sa_plot.png"
        }
