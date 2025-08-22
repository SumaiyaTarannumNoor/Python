import numpy as np
import matplotlib.pyplot as plt

N = 1000000
rng = np.random.default_rng(42)
U = rng.random(N)

x_vals = np.linspace(0.75, 0.999, 200)

empirical_tail = np.array([(U > x).mean() for x in x_vals])

theoretical_tail = 1 - x_vals

plt.figure(figsize=(8,6))
plt.plot(x_vals, empirical_tail, label="Empirical P(U>x)", color="green")
plt.plot(x_vals, theoretical_tail, "--", label="Theoretical 1-x", color="red")
plt.xlabel("x")
plt.ylabel("Tail Probability")
plt.title("Tail Distribution of U(0,1): P(U>x) for x in (0.75, 1)")
plt.legend()
plt.grid(True)
plt.show()