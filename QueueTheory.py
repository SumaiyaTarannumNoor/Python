import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

def exponential_rv(lam, size=10000):
    U = np.random.rand(size)
    return -np.log(U) / lam

def simulate_mm1(lambda_arrival, mu_service, N=100000, max_customers=20):
    # Generate interarrival and service times
    inter_arrival_times = exponential_rv(lambda_arrival, N)
    service_times = exponential_rv(mu_service, N)

    arrival_times = np.cumsum(inter_arrival_times)
    start_service_times = np.zeros(N)
    departure_times = np.zeros(N)

    for i in range(N):
        if i == 0:
            start_service_times[i] = arrival_times[i]
        else:
            start_service_times[i] = max(arrival_times[i], departure_times[i-1])
        departure_times[i] = start_service_times[i] + service_times[i]

    # ---- Event-driven state tracking ----
    events = np.sort(np.concatenate([arrival_times, departure_times]))
    customers = 0
    last_t = 0
    time_in_state = np.zeros(max_customers+1)

    for t in events:
        # accumulate time spent in current state
        dt = t - last_t
        if customers <= max_customers:
            time_in_state[customers] += dt
        else:
            time_in_state[max_customers] += dt  # lump overflow into max_customers
        last_t = t

        # update state
        if t in arrival_times:
            customers += 1
        else:
            customers -= 1

    # normalize to get probabilities
    Pn_simulated = time_in_state / np.sum(time_in_state)
    return Pn_simulated

# Parameters
mu_service = 10
max_customers = 20
N = 50000   # reduce a bit for faster simulation

# ---- Simulation for rho = 0.9 ----
lambda_arrival = 9
Pn_simulated = simulate_mm1(lambda_arrival, mu_service, N, max_customers)
rho = lambda_arrival / mu_service
Pn_analytical = rho**np.arange(max_customers+1) * (1-rho)

plt.figure()
plt.bar(range(max_customers+1), Pn_simulated, alpha=0.6, label='Simulated Pn')
plt.plot(range(max_customers+1), Pn_analytical, 'r-o', lw=2, label='Analytical Pn')
plt.xlabel('Number of Customers n')
plt.ylabel('Pn')
plt.title('M/M/1 Queue Stationary Distribution (rho=0.9)')
plt.legend()
plt.show()

# ---- Compare for different rho ----
plt.figure()
for rho_val in [0.9, 0.5, 0.25]:
    lambda_val = rho_val * mu_service
    Pn_sim = simulate_mm1(lambda_val, mu_service, N, max_customers)
    Pn_theory = rho_val**np.arange(max_customers+1) * (1-rho_val)

    plt.plot(range(max_customers+1), Pn_sim, 'o', label=f'Sim rho={rho_val} (simulated)')
    plt.plot(range(max_customers+1), Pn_theory, '-', label=f'rho={rho_val} (analytical)')

plt.xlabel('Number of Customers n')
plt.ylabel('Pn')
plt.title('M/M/1 Queue: Simulated vs Analytical for Different Traffic Intensities')
plt.legend()
plt.grid(True)
plt.show()
