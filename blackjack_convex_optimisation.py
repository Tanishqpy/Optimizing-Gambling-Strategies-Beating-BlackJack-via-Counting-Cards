import cvxpy as cp
import numpy as np

# Suppose we discretize the card count into N states
N = 1000  # number of count states

# Expected value per hand for each count state (for illustration)
expected_ev = np.zeros(N)
# Assign some positive EVs for high counts (e.g., last 10 states)
expected_ev[-10:] = np.linspace(0.01, 0.025, 10)
# Assign some slightly negative EVs for low counts (e.g., first 10 states)
expected_ev[:10] = np.linspace(-0.01, -0.005, 10)

# Probability of each count state (uniform for illustration)
prob_state = np.ones(N) / N

# Decision variables: bet size for each count state
x = cp.Variable(N)

# Table limits
x_min = 1.0   # minimum bet
x_max = 100.0 # maximum bet

# Objective: maximize expected profit across all count states
objective = cp.Maximize(cp.sum(cp.multiply(prob_state, expected_ev * x)))

# Constraints
constraints = [
    x >= x_min,
    x <= x_max
    # Optionally: cp.sum(x) <= total_bankroll
]

# Problem definition
problem = cp.Problem(objective, constraints)

# Solve
problem.solve()

print("Optimal bet sizes for each count state:", x.value)
print("Maximum expected profit per hand:", problem.value)
