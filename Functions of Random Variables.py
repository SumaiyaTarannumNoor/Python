import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

np.random.seed(42)

# Define parameter sets for each distribution
params = {
    "Gaussian": [(0, 1), (2, 1), (0, 2)],  # (mu, sigma)
    "Poisson": [2, 5, 10],                # lambda
    "Exponential": [0.5, 1, 2],           # lambda
    "Binomial": [(10, 0.3), (10, 0.5), (20, 0.7)]  # (n, p)
}

def print_stats(dist_name, distribution, *params):
    mean, var = distribution.stats(*params, moments="mv")
    print(f"{dist_name} params={params} => Mean={mean:.3f}, Var={var:.3f}")

fig, axes = plt.subplots(4, 1, figsize=(4, 8))

# Gaussian
x = np.linspace(-10, 10, 500)
for mu, sigma in params["Gaussian"]:
    pdf = stats.norm.pdf(x, mu, sigma)
    axes[0].plot(x, pdf, label=f"μ={mu}, σ={sigma}")
    print_stats("Gaussian", stats.norm, mu, sigma)
axes[0].set_title("Gaussian Distribution")
axes[0].legend()
axes[0].grid()

# Poisson
x = np.arange(0, 25)
for lam in params["Poisson"]:
    pmf = stats.poisson.pmf(x, lam)
    axes[1].stem(x, pmf, basefmt=" ", label=f"λ={lam}")
    print_stats("Poisson", stats.poisson, lam)
axes[1].set_title("Poisson Distribution")
axes[1].legend()
axes[1].grid()

# Exponential
x = np.linspace(0, 10, 500)
for lam in params["Exponential"]:
    pdf = stats.expon.pdf(x, scale=1/lam)
    axes[2].plot(x, pdf, label=f"λ={lam}")
    print_stats("Exponential", stats.expon, 0, 1/lam)  # loc=0, scale=1/λ
axes[2].set_title("Exponential Distribution")
axes[2].legend()
axes[2].grid()

# Binomial
x = np.arange(0, 21)
for n, p in params["Binomial"]:
    pmf = stats.binom.pmf(x, n, p)
    axes[3].stem(x, pmf, basefmt=" ", label=f"n={n}, p={p}")
    print_stats("Binomial", stats.binom, n, p)
axes[3].set_title("Binomial Distribution")
axes[3].legend()
axes[3].grid()

plt.tight_layout()
plt.show()
