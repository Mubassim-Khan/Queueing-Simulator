import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to generate times based on the chosen distribution
def generate_times(distribution, size, low, high, input_handler=None):
    try:
        if distribution == "poisson":
            lam = float(input_handler.get("poisson_lambda") if input_handler else input("Enter the lambda parameter for Poisson distribution: "))
            times = np.random.poisson(lam, size)
        elif distribution == "exponential":
            scale = float(input_handler.get("exponential_scale") if input_handler else input("Enter the mean (1/lambda) for Exponential distribution: "))
            times = np.random.exponential(scale, size)
        elif distribution == "uniform":
            low = float(input_handler.get("uniform_low") if input_handler else input("Enter the minimum value for Uniform distribution: "))
            high = float(input_handler.get("uniform_high") if input_handler else input("Enter the maximum value for Uniform distribution: "))
            times = np.random.uniform(low, high, size)
        elif distribution == "normal":
            mean = float(input_handler.get("normal_mean") if input_handler else input("Enter the mean for Normal distribution: "))
            std_dev = float(input_handler.get("normal_std_dev") if input_handler else input("Enter the standard deviation for Normal distribution: "))
            times = np.random.normal(mean, std_dev, size)
    except ValueError as e:
        raise "Invalid distribution selected: {}".format(e)

    return np.clip(times, low, high).astype(int)

# Function to create Gantt chart
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
    return fig

# Main function
def simulator(input_handler = None):
    num_simulations = int(input_handler.get("num_simulations") if input_handler else input("Enter the number of simulations: "))
    num_servers = int(input_handler.get("num_servers") if input_handler else input("Enter the number of servers: "))

    # Generate interarrival time
    arrival_dist = input_handler.get("arrival_dist") if input_handler else input("Select distribution for inter-arrival times (Poisson, Exponential, Uniform, Normal): ").lower()
    interarrival_times = generate_times(arrival_dist, num_simulations, 0, 9, input_handler)

    # Generate service time
    service_dist = input_handler.get("service_dist") if input_handler else input("Select distribution for service times (Poisson, Exponential, Uniform, Normal): ").lower()
    service_times = generate_times(service_dist, num_simulations, 1, 10, input_handler)

    priority_inclusion = input_handler.get("priority", None) if input_handler else input("Do you want to include priority? (yes/no): ").lower()
    priorities = None
    if priority_inclusion == "yes":
        priorities = np.random.randint(1, 4, num_simulations)
    else:
        priorities = ["N/A"] * num_simulations
        
    # Calculate cumulative arrival times
    arrival_times = np.cumsum(interarrival_times)

    # Initialize simulation tables
    # table1 = pd.DataFrame({
    #     "Simulation No": np.arange(1, num_simulations + 1),
    #     "Interarrival Time": interarrival_times,
    #     "Arrival Time": arrival_times,
    #     "Service Time": service_times
    # })

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
        "Priority": priorities,
        "Start Time": start_times,
        "End Time": end_times,
        "Turnaround Time": turnaround_times,
        "Wait Time": wait_times,
        "Response Time": response_times,
        "Server": server_allocations
    })

    # Metrics calculations
    # avg_interarrival_time = np.mean(interarrival_times)
    # avg_service_time = np.mean(service_times)
    # avg_turnaround_time = np.mean(turnaround_times)
    # avg_wait_time = np.mean(wait_times)
    # avg_response_time = np.mean(response_times)
    server_utilization = [float(round(servers[i] / arrival_times[-1], 2)) for i in range(num_servers)]
    # queue_length = np.sum(wait_times > 0)
    # prob_waiting = queue_length / num_simulations

    # print("\nTable 1:")
    # print(table1)
    # print("\nTable 2:")
    # print(table2)
    # print("\nMetrics:")
    # print(f"Average Interarrival Time: {round(avg_interarrival_time, 3)}")
    # print(f"Average Service Time: {round(avg_service_time, 3)}")
    # print(f"Average Turnaround Time: {round(avg_turnaround_time,3)}")
    # print(f"Average Wait Time: {round(avg_wait_time, 3)}")
    # print(f"Average Response Time: {round(avg_response_time, 3)}")
    # print(f"Server Utilization: {server_utilization}")
    # print(f"Queue Length: {round(queue_length, 3)}")
    # print(f"Probability of Waiting Customers: {round(prob_waiting, 3)}")

    # Gantt Chart
    gantt_chart = create_gantt_chart(num_servers, start_times, end_times, server_allocations)
    return table2, server_utilization, gantt_chart
# Run the simulator
# simulator()
