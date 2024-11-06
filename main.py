import os
import csv
import time
import numpy as np

# Function to parse the instance file
def parse_instance_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()[5:]
    lines = [line.strip() for line in lines if line.strip()]

    instance_name = lines[0].split('=')[1].strip().replace('"', '').replace(';', '')
    d = int(lines[1].split('=')[1].strip().replace(';', ''))
    r = int(lines[2].split('=')[1].strip().replace(';', ''))
    SCj = list(map(int, lines[3].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    Dk = list(map(int, lines[4].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    cjk_lines = lines[5].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '')
    for additional_line in lines[6:]:  # Add all subsequent lines to Cjk if they exist
        cjk_lines += " " + additional_line.strip().replace(';', '').replace('[', '').replace(']', '')

    # Convert the combined Cjk string into a numpy array
    Cjk = np.fromstring(cjk_lines, sep=' ').reshape(d, r)
    # print(instance_name+" "+str(d)+" "+str(r)+" "+str(SCj)+" "+str(Dk))
    print(Dk)
    print("\n")
    print(Cjk)
    
    return instance_name, d, r, SCj, Dk, Cjk

# North-West Corner Method implementation
def north_west_corner_method(d, r, SCj, Dk, Cjk):
    supply = SCj.copy()
    demand = Dk.copy()
    solution = np.zeros((d, r), dtype=int)
    cost = 0
    i, j = 0, 0
    iterations = 0

    start_time = time.time()

    while i < d and j < r:
        iterations += 1
        allocation = min(supply[i], demand[j])
        solution[i][j] = allocation
        cost += allocation * Cjk[i][j]
        supply[i] -= allocation
        demand[j] -= allocation

        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    end_time = time.time()
    running_time = end_time - start_time
    solved = sum(supply) >= 0 and sum(demand) == 0

    return cost, iterations, running_time, solved

# Main function to process files and write results
def process_files(input_directory, output_file):
    results = []
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".dat"):  # Assuming the files are text files
            file_path = os.path.join(input_directory, file_name)
            instance_name, d, r, SCj, Dk, Cjk = parse_instance_file(file_path)
            cost, iterations, running_time, solved = north_west_corner_method(d, r, SCj, Dk, Cjk)
            results.append([instance_name, cost, iterations, running_time, solved])

    # Write results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Instance Name", "Cost", "Iterations", "Running Time", "Solved"])
        writer.writerows(results)

# Example usage
input_directory = "./Lab_simple_instances"
output_file = "results.csv"
process_files(input_directory, output_file)
