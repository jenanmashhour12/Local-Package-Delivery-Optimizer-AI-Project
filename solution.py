from MathCalc import euclidean_distance

class Solution:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def total_distance(self):
        total = 0
        for vehicle in self.vehicles:
            if not vehicle.route:
                continue  # Skip empty vehicle routes

            x, y = 0, 0  # Start from shop
            for pkg in vehicle.route:
                total += euclidean_distance(x, y, pkg.x, pkg.y)
                x, y = pkg.x, pkg.y

            total += euclidean_distance(x, y, 0, 0)  # Return to shop
        return round(total, 2)

    def print_routes(self):
        for v in self.vehicles:
            route_str = " --> ".join([p.id for p in v.route])
            print(f"\n Vehicle {v.id} [{v.capacity}kg]: {route_str} (Remaining: {v.remaining_capacity}kg)")
