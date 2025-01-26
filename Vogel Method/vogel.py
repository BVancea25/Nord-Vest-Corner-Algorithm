import time
import numpy as np
import os
import csv
import matplotlib.pyplot as plt

def parse_instance_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()[5:]  # Skip header lines
    lines = [line.strip() for line in lines if line.strip()]

    # Parse basic info
    instance_name = lines[0].split('=')[1].strip().replace('"', '').replace(';', '')
    d = int(lines[1].split('=')[1].strip().replace(';', ''))
    r = int(lines[2].split('=')[1].strip().replace(';', ''))
    SCj = list(map(int, lines[3].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    Fj = list(map(int, lines[4].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))
    Dk = list(map(int, lines[5].split('=')[1].strip().replace(';', '').replace('[', '').replace(']', '').split()))

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

    return instance_name, d, r, SCj, Dk, Cjk, Fj


def process_files(input_directory, output_file):
    results = []
    iteration_data = []
    execution_times = []

    for file_name in os.listdir(input_directory):
        if file_name.endswith(".dat"):
            file_path = os.path.join(input_directory, file_name)
            try:
                instance_name, d, r, SCj, Dk, Cjk, Fj = parse_instance_file(file_path)
                print(instance_name)
                start_time = time.time()
                cost, allocation, iteration_count = vogel_method(d, r, SCj, Dk, Cjk, Fj)
                end_time = time.time()

                exec_time = end_time - start_time

                results.append([instance_name, cost])
                iteration_data.append([instance_name, iteration_count])
                execution_times.append([instance_name, exec_time])

                print(f"Processed {instance_name}: Cost = {cost}, Iterations = {iteration_count}, Time = {exec_time:.4f}s")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Write results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Instance Name", "Cost"])
        writer.writerows(results)

    return iteration_data, execution_times


def vogel_method(d, r, SCj, Dk, Cjk, Fj):
    # Initialize the allocation matrix
    allocation = np.zeros((d, r), dtype=int)
    total_cost = 0
    iteration_count = 0

    # Convert SCj and Dk to numpy arrays for easier manipulation
    supply = np.array(SCj)
    demand = np.array(Dk)

    # Add fixed costs to the cost matrix if a deposit is used
    for j in range(d):
        if np.any(allocation[j, :] > 0):
            total_cost += Fj[j]

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        iteration_count += 1

        # Calculate penalties for rows and columns
        row_penalties = []
        for i in range(d):
            if supply[i] > 0:
                row = Cjk[i, :]
                row = row[demand > 0]
                if len(row) > 1:
                    sorted_row = np.sort(row)
                    penalty = sorted_row[1] - sorted_row[0]
                else:
                    penalty = 0
                row_penalties.append(penalty)
            else:
                row_penalties.append(-1)

        col_penalties = []
        for j in range(r):
            if demand[j] > 0:
                col = Cjk[:, j]
                col = col[supply > 0]
                if len(col) > 1:
                    sorted_col = np.sort(col)
                    penalty = sorted_col[1] - sorted_col[0]
                else:
                    penalty = 0
                col_penalties.append(penalty)
            else:
                col_penalties.append(-1)

        # Find the maximum penalty
        max_row_penalty = max(row_penalties)
        max_col_penalty = max(col_penalties)

        if max_row_penalty >= max_col_penalty:
            # Allocate in the row with the maximum penalty
            row_index = row_penalties.index(max_row_penalty)
            row = Cjk[row_index, :]
            row = row[demand > 0]
            min_col_index = np.argmin(row)
            col_index = np.where(demand > 0)[0][min_col_index]
        else:
            # Allocate in the column with the maximum penalty
            col_index = col_penalties.index(max_col_penalty)
            col = Cjk[:, col_index]
            col = col[supply > 0]
            min_row_index = np.argmin(col)
            row_index = np.where(supply > 0)[0][min_row_index]

        # Allocate as much as possible
        amount = min(supply[row_index], demand[col_index])
        allocation[row_index, col_index] += amount
        total_cost += amount * Cjk[row_index, col_index]
        supply[row_index] -= amount
        demand[col_index] -= amount

    return total_cost, allocation, iteration_count

iteration_data, execution_times = process_files('./Lab_FCD_instances', 'results.csv')