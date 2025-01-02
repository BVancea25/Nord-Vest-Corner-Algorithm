import numpy as np
import os
import csv

def parse_instance_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()[5:]  # Skip header lines
    lines = [line.strip() for line in lines if line.strip()]

    # Parse basic info
    instance_name = lines[0].split('=')[1].strip().replace('"', '').replace(';', '')
    d = int(lines[1].split('=')[1].strip().replace(';', ''))
    r = int(lines[2].split('=')[1].strip().replace(';', ''))
    SCj = list(map(int, lines[3].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    Dk = list(map(int, lines[4].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))

    # Extract and reshape `Cjk`
    cjk_start = next(i for i, line in enumerate(lines) if line.startswith("Cjk"))
    cjk_values = []
    if "[" in lines[cjk_start]:  # Matrix starts on the same line
        cjk_values.extend(map(int, lines[cjk_start].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    for line in lines[cjk_start + 1:]:
        if line.startswith("Fjk"):
            break
        cjk_values.extend(map(int, line.replace(';', '').replace('[', '').replace(']', '').split()))
    if len(cjk_values) != d * r:
        raise ValueError(f"Size mismatch in Cjk matrix for {instance_name}. Expected {d * r}, got {len(cjk_values)}.")
    Cjk = np.array(cjk_values).reshape(d, r)

    # Extract and reshape `Fjk`
    fjk_start = next(i for i, line in enumerate(lines) if line.startswith("Fjk"))
    fjk_values = []
    if "[" in lines[fjk_start]:  # Matrix starts on the same line
        fjk_values.extend(map(int, lines[fjk_start].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    for line in lines[fjk_start + 1:]:
        if not line:
            break
        fjk_values.extend(map(int, line.replace(';', '').replace('[', '').replace(']', '').split()))
    if len(fjk_values) != d * r:
        raise ValueError(f"Size mismatch in Fjk matrix for {instance_name}. Expected {d * r}, got {len(fjk_values)}.")
    Fjk = np.array(fjk_values).reshape(d, r)

    return instance_name, d, r, SCj, Dk, Cjk, Fjk


def solve_minimum_matrix_method(d, r, SCj, Dk, Cjk, Fjk):
    allocation = np.zeros((d, r), dtype=int)
    total_cost = 0
    remaining_SCj = SCj[:]
    remaining_Dk = Dk[:]

    while np.sum(remaining_Dk) > 0:
        min_cost = float('inf')
        min_i, min_j = -1, -1
        for i in range(d):
            for j in range(r):
                if remaining_SCj[i] > 0 and remaining_Dk[j] > 0 and Cjk[i][j] < min_cost:
                    min_cost = Cjk[i][j]
                    min_i, min_j = i, j

        if min_i == -1 or min_j == -1:
            raise ValueError("Allocation not possible with current data.")

        allocation_amount = min(remaining_SCj[min_i], remaining_Dk[min_j])
        allocation[min_i][min_j] = allocation_amount
        total_cost += allocation_amount * Cjk[min_i][min_j] + Fjk[min_i][min_j]
        remaining_SCj[min_i] -= allocation_amount
        remaining_Dk[min_j] -= allocation_amount

    return total_cost, allocation

def process_files(input_directory, output_file):
    results = []
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".dat"):
            file_path = os.path.join(input_directory, file_name)
            try:
                instance_name, d, r, SCj, Dk, Cjk, Fjk = parse_instance_file(file_path)
                cost, allocation = solve_minimum_matrix_method(d, r, SCj, Dk, Cjk, Fjk)
                results.append([instance_name, cost])
                print(f"Processed {instance_name}: Cost = {cost}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Write results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Instance Name", "Cost"])
        writer.writerows(results)

# Example usage
process_files('./Lab_FCR_instances', 'results.csv')
