import matplotlib.pyplot as plt
import os

def save_and_show(algorithm):
    # Get the absolute path to the static folder
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    filename = f'{algorithm}_plot.png'
    filepath = os.path.join(static_dir, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    return filename  # only return the filename for HTML

def plot_routes_sa(solution, save_path=None):
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    shop_x, shop_y = 0, 0

    plt.figure(figsize=(8, 6))
    plt.title("Vehicle Routes (SA)")
    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")

    plt.plot(shop_x, shop_y, 'ks', markersize=10, label="Shop")

    for idx, vehicle in enumerate(solution.vehicles):
        route = vehicle.route
        if not route:
            continue

        color = colors[idx % len(colors)]
        x_coords = [shop_x] + [pkg.x for pkg in route] + [shop_x]
        y_coords = [shop_y] + [pkg.y for pkg in route] + [shop_y]

        plt.plot(x_coords, y_coords, marker='o', color=color, label=f"Vehicle {vehicle.id}")

        for pkg in route:
            plt.annotate(pkg.id, (pkg.x, pkg.y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.legend()
    plt.grid(True)
    return save_and_show('sa')

def plot_routes_ga(solution, save_path=None):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    shop_x, shop_y = 0, 0

    plt.figure(figsize=(8, 6))
    plt.title("Vehicle Routes (GA)")
    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")

    plt.plot(shop_x, shop_y, 'ks', markersize=10, label="Shop")

    for idx, (vehicle_id, packages) in enumerate(solution.items()):
        if not packages:
            continue

        route_x = [shop_x] + [pkg.x for pkg in packages] + [shop_x]
        route_y = [shop_y] + [pkg.y for pkg in packages] + [shop_y]

        for pkg in packages:
            plt.annotate(pkg.id, (pkg.x, pkg.y), textcoords="offset points", xytext=(0, 10), ha='center')

        color = colors[idx % len(colors)]
        plt.plot(route_x, route_y, f'{color}-o', label=f'Vehicle {vehicle_id}')

    plt.legend()
    plt.grid(True)
    return save_and_show('ga')
