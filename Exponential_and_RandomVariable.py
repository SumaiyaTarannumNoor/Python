import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, poisson

np.random.seed(42)

def exponential_rv(lam, size=10000):
    U = np.random.rand(size)
    return -np.log(U) / lam

lam = 1 / 10  # E[X] = 10
X = exponential_rv(lam, size=100000)

def poisson_rv(mu, size=10000):
    samples = []
    for _ in range(size):
        L = np.exp(-mu)
        k = 0
        p = 1
        while p > L:
            k += 1
            p *= np.random.rand()
        samples.append(k-1)
    return np.array(samples)

mu = 10  # E[Z] = 10
Z = poisson_rv(mu, size=50000)

#Exponential histogram vs theoretical PDF
x_vals = np.linspace(0, 60, 200)
plt.figure()
plt.hist(X, bins=100, density=True, alpha=0.6, label="Simulated Exponential")
plt.plot(x_vals, expon.pdf(x_vals, scale=1/lam), 'r-', lw=2, label="Theoretical PDF")
plt.title("Exponential Distribution PDF")
plt.xlabel("x"); plt.ylabel("Density")
plt.legend()

# Poisson histogram vs theoretical PMF
z_vals = np.arange(0, 25)
counts, bins = np.histogram(Z, bins=np.arange(-0.5, 25.5, 1), density=True)

plt.figure()
plt.bar(z_vals, counts, alpha=0.6, label="Simulated Poisson")
plt.plot(z_vals, poisson.pmf(z_vals, mu), 'r-', lw=2, label="Theoretical PMF")
plt.title("Poisson Distribution PMF")
plt.xlabel("z"); plt.ylabel("Probability")
plt.legend()

# Exponential: P(X > x)
plt.figure()
plt.plot(x_vals, np.mean(X[:,None] > x_vals, axis=0), 'b.', label="Simulated P(X>x)")
plt.plot(x_vals, np.exp(-lam*x_vals), 'r-', lw=2, label="Theoretical P(X>x)")
plt.title("Exponential Survival Function")
plt.xlabel("x"); plt.ylabel("P(X>x)")
plt.legend()

# Poisson: P(Z > z)
plt.figure()
plt.plot(z_vals, [np.mean(Z > z) for z in z_vals], 'bo', label="Simulated P(Z>z)")
plt.plot(z_vals, 1-poisson.cdf(z_vals, mu), 'r-', lw=2, label="Theoretical P(Z>z)")
plt.title("Poisson Survival Function")
plt.xlabel("z"); plt.ylabel("P(Z>z)")
plt.legend()

plt.show()
