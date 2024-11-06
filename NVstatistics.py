import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file containing the results
results_file = "results.csv"
data = pd.read_csv(results_file)

# Classify instance sizes based on the number of deposits and retailers
def classify_instance_size(row):
    if row["Instance Name"].startswith("small"):
        return "Small (2x3)"
    elif row["Instance Name"].startswith("medium"):
        return "Medium (5x15)"
    elif row["Instance Name"].startswith("large"):
        return "Large (10x50)"
    else:
        return "Unknown"

# Add a new column for instance size
data["Instance Size"] = data.apply(classify_instance_size, axis=1)

# Visualize the number of iterations based on instance size
plt.figure(figsize=(10, 6))
sns.boxplot(x="Instance Size", y="Iterations", data=data)
plt.title("Number of Iterations by Instance Size")
plt.xlabel("Instance Size")
plt.ylabel("Number of Iterations")
plt.show()

# Visualize the running time based on instance size
plt.figure(figsize=(10, 6))
sns.boxplot(x="Instance Size", y="Running Time", data=data)
plt.title("Running Time by Instance Size")
plt.xlabel("Instance Size")
plt.ylabel("Running Time (seconds)")
plt.show()
