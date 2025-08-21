A Flask-based web application that optimizes local package delivery routes using Genetic Algorithms (GA) and Simulated Annealing (SA). This project solves the Vehicle Routing Problem (VRP) by assigning packages to a fleet of vehicles to minimize total travel distance while respecting vehicle capacity constraints and package priorities.

Key Features:

🤖 Dual-Algorithm Optimization: Implements both a Genetic Algorithm and Simulated Annealing to find efficient delivery routes, allowing for performance comparison.

📦 Constraint Handling: Efficiently manages real-world constraints:

Vehicle Capacity: No vehicle is overloaded.

Package Priority: Higher-priority packages (1-5) are prioritized for delivery.

Euclidean Distance: Minimizes the total straight-line distance traveled from the depot (0,0).

🌐 Interactive Web Interface: User-friendly Flask app for inputting vehicles, packages, and algorithm selection. Displays results with clear assignments, remaining capacity, and undelivered packages.

📊 Visual Route Plotting: Automatically generates and displays matplotlib plots of the optimized routes for each vehicle, providing intuitive visual feedback.

🧪 Comprehensive Testing: Includes detailed test cases for priority handling, feasibility, distance optimization, and edge cases (like over-capacity packages).

Tech Stack: Python, Flask, Matplotlib, NumPy (for distance calculation).
Algorithms: Genetic Algorithm (with Selection, Crossover, Mutation), Simulated Annealing.

