
from flask import Flask, render_template, request
from main import run_optimization  

app = Flask(__name__) 

@app.route('/')
def index():
    return render_template("index.html")  # show this page for user input

# a route to handle submission and runs the optimization
@app.route('/run', methods=['POST'])
def run():
    try:
        #reading the num of vehicles and packages
        num_vehicles = int(request.form['num_vehicles'])
        num_packages = int(request.form['num_packages'])

        #read which algorithm the user selected
        algorithm = request.form['algorithm']
        # a list to store each vehicle's capacity
        vehicle_caps = []  
        
        for i in range(num_vehicles):
            cap = request.form.get(f"vehicle_{i}", "")  
            if not cap.strip():  # to check if capacity is empty 
                raise ValueError(f"Missing capacity input for vehicle {i + 1}.")
            vehicle_caps.append(float(cap)) 

        packages = []  #to store package info(x, y, weight, priority)
        for i in range(num_packages):
            try:
                x = float(request.form[f"x_{i}"])  
                y = float(request.form[f"y_{i}"])  
                w = float(request.form[f"w_{i}"])  
                p = int(request.form[f"p_{i}"])
                packages.append((x, y, w, p))
            except ValueError:
                # In case of invalid input
                raise ValueError(f"Invalid package data at index {i + 1}.")

        # Run the optimization algorithm with user's input
        result = run_optimization(vehicle_caps, packages, algorithm)

        # display the result 
        return render_template("result.html", result=result)

    except Exception as e:
        # handling if any error occurs
        return render_template("error.html", error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
