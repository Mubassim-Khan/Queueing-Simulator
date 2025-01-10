import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to generate times based on the chosen distribution
def generate_times(distribution, size, low, high):
    if distribution == "Poisson":
        lam = float(input("Enter the lambda parameter for Poisson distribution: "))
        times = np.random.poisson(lam, size)
    elif distribution == "Exponential":
        scale = float(input("Enter the mean (1/lambda) for Exponential distribution: "))
        times = np.random.exponential(scale, size)
    elif distribution == "Uniform":
        low = float(input("Enter the minimum value for Uniform distribution: "))
        high = float(input("Enter the maximum value for Uniform distribution: "))
        times = np.random.uniform(low, high, size)
    elif distribution == "Normal":
        mean = float(input("Enter the mean for Normal distribution: "))
        std_dev = float(input("Enter the standard deviation for Normal distribution: "))
        times = np.random.normal(mean, std_dev, size)
    else:
        raise ValueError("Invalid distribution selected.")

    return np.clip(times, low, high).astype(int)

# Function to create a professional Gantt chart
def create_gantt_chart(num_servers, start_times, end_times, server_allocations):
    fig, axes = plt.subplots(num_servers, 1, figsize=(8, 3 * num_servers), sharex=True)
    if num_servers == 1:
        axes = [axes]

    for server_idx in range(num_servers):
        server_times = [(start_times[i], end_times[i]) for i in range(len(start_times)) if server_allocations[i] == server_idx + 1]
        for start, end in server_times:
            axes[server_idx].barh(0, end - start, left=start, color='skyblue', edgecolor='black', height=0.4)
        
        # Customize each subplot
        axes[server_idx].set_title(f"Server {server_idx + 1}", fontsize=12, fontweight='bold')
        axes[server_idx].set_yticks([])  # Remove y-axis ticks
        axes[server_idx].set_xlabel("Time", fontsize=10)
        axes[server_idx].grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# Main function
def simulator():
    num_simulations = int(input("Enter the number of simulations: "))
    num_servers = int(input("Enter the number of servers: "))

    # Generate interarrival times
    arrival_dist = input("Select distribution for inter-arrival times (Poisson, Exponential, Uniform, Normal): ")
    interarrival_times = generate_times(arrival_dist, num_simulations, 0, 9)

    # Generate service times
    service_dist = input("Select distribution for service times (Poisson, Exponential, Uniform, Normal): ")
    service_times = generate_times(service_dist, num_simulations, 1, 10)

    # Generate priority column if required
    priority = input("Do you want to include priority? (yes/no): ").lower()
    priorities = None
    if priority == "yes":
        priorities = np.random.randint(1, 4, num_simulations)

    # Calculate cumulative arrival times
    arrival_times = np.cumsum(interarrival_times)

    # Initialize simulation tables
    table1 = pd.DataFrame({
        "Simulation No": np.arange(1, num_simulations + 1),
        "Interarrival Time": interarrival_times,
        "Arrival Time": arrival_times,
        "Service Time": service_times
    })

    start_times = np.zeros(num_simulations)
    end_times = np.zeros(num_simulations)
    turnaround_times = np.zeros(num_simulations)
    wait_times = np.zeros(num_simulations)
    response_times = np.zeros(num_simulations)
    server_allocations = np.zeros(num_simulations, dtype=int)

    # Assign servers and calculate times
    servers = [0] * num_servers  # Keeps track of when each server is free
    for i in range(num_simulations):
        # Assign server based on availability
        server_idx = np.argmin(servers)
        server_allocations[i] = server_idx + 1
        start_times[i] = max(servers[server_idx], arrival_times[i])
        end_times[i] = start_times[i] + service_times[i]
        servers[server_idx] = end_times[i]

        # Calculate other metrics
        turnaround_times[i] = end_times[i] - arrival_times[i]
        wait_times[i] = start_times[i] - arrival_times[i]
        response_times[i] = start_times[i] - arrival_times[i]

    table2 = pd.DataFrame({
        "Simulation No": np.arange(1, num_simulations + 1),
        "Arrival Time": arrival_times,
        "Service Time": service_times,
        "Priority": priorities if priorities is not None else "N/A",
        "Start Time": start_times,
        "End Time": end_times,
        "Turnaround Time": turnaround_times,
        "Wait Time": wait_times,
        "Response Time": response_times,
        "Server": server_allocations
    })

    # Metrics calculations
    avg_interarrival_time = np.mean(interarrival_times)
    avg_service_time = np.mean(service_times)
    avg_turnaround_time = np.mean(turnaround_times)
    avg_wait_time = np.mean(wait_times)
    avg_response_time = np.mean(response_times)
    server_utilization = [round(servers[i] / arrival_times[-1], 2) for i in range(num_servers)]
    queue_length = np.sum(wait_times > 0)
    prob_waiting = queue_length / num_simulations

    print("\nTable 1:")
    print(table1)
    print("\nTable 2:")
    print(table2)
    print("\nMetrics:")
    print(f"Average Interarrival Time: {avg_interarrival_time}")
    print(f"Average Service Time: {avg_service_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print(f"Average Wait Time: {avg_wait_time}")
    print(f"Average Response Time: {avg_response_time}")
    print(f"Server Utilization: {server_utilization}")
    print(f"Queue Length: {queue_length}")
    print(f"Probability of Waiting Customers: {prob_waiting}")

    # Gantt Chart
    create_gantt_chart(num_servers, start_times, end_times, server_allocations)

# Run the simulator
simulator()
