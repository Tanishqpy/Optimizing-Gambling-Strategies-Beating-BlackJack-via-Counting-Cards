# Blackjack Betting Optimization Report

## 1. Introduction

This report details the optimization problem aimed at determining the optimal betting strategy for the card game Blackjack, based on the current card count state. The goal is to maximize the expected profit per hand by adjusting the bet size according to the perceived advantage (or disadvantage) indicated by the count state. The provided Python GUI tool implements and solves this optimization problem.

## 2. Problem Formulation

The core problem is to decide how much to bet for each possible count state encountered during a Blackjack game to maximize long-term expected winnings, subject to betting limits.

### 2.1. Objective Function

The primary objective is to **maximize the total expected profit per hand** across all possible count states. The expected profit for a single state is the product of the probability of being in that state, the expected value (EV) of a hand played in that state, and the bet size chosen for that state.

*   **Maximize:** Σ (Probability of State *i* × Expected Value of State *i* × Bet Size for State *i*) for all states *i*.

### 2.2. Decision Variables

*   **`x_i`**: The bet size for each count state *i*, where *i* ranges from 0 to N-1 (N being the total number of discrete count states considered).

### 2.3. Parameters

*   **`N`**: Total number of discrete count states.
*   **`x_min`**: The minimum allowed bet size.
*   **`x_max`**: The maximum allowed bet size.
*   **`ev_i`**: The expected value (average win/loss per unit bet) for playing a hand when the count is in state *i*. This is typically positive for high counts (player advantage) and negative for low counts (dealer advantage).
*   **`p_i`**: The probability of the game being in count state *i*. In the current implementation, this is assumed to be uniform (1/N) for simplicity, but could be based on simulation data in a more advanced model.

### 2.4. Constraints

The bet size for each state must adhere to the table limits:

1.  **Minimum Bet Constraint:** `x_i ≥ x_min` for all states *i*.
2.  **Maximum Bet Constraint:** `x_i ≤ x_max` for all states *i*.

*(Optional: A bankroll constraint could be added, such as Σ (p_i * x_i) ≤ Average Available Bankroll, but is not included in the current basic model).*

## 3. Mathematical Model

Let:
*   `N` be the number of count states.
*   `x = [x_0, x_1, ..., x_{N-1}]` be the vector of bet sizes (decision variables).
*   `ev = [ev_0, ev_1, ..., ev_{N-1}]` be the vector of expected values for each state.
*   `p = [p_0, p_1, ..., p_{N-1}]` be the vector of probabilities for each state.

The optimization problem is formulated as:

**Maximize:** `p^T * (ev .* x)`  (where `.*` denotes element-wise multiplication)

**Subject to:**
1.  `x_i ≥ x_min` for *i* = 0, ..., N-1
2.  `x_i ≤ x_max` for *i* = 0, ..., N-1

This is a Linear Programming (LP) problem, as the objective function and constraints are linear with respect to the decision variables `x`.

## 4. Implementation

The problem is implemented in Python using:
*   **`cvxpy`**: A library for convex optimization, used here to define and solve the LP problem.
*   **`numpy`**: For numerical operations, particularly vector calculations.
*   **`tkinter`**: For creating the graphical user interface (GUI).
*   **`matplotlib`**: For plotting the results (optimal bet size vs. count state).

The GUI allows users to easily modify parameters and visualize the resulting optimal betting strategy.

## 5. Input Parameters (GUI)

The user can configure the following parameters through the GUI:

*   **Number of count states (N):** Defines the granularity of the count states.
*   **Minimum bet (x_min):** The smallest allowed wager.
*   **Maximum bet (x_max):** The largest allowed wager.
*   **High/Low count EV ranges:** Defines the expected values for the highest and lowest count states. The EV for intermediate states is interpolated (currently linearly, with neutral states having EV=0).
*   **High/Low count states:** The number of states at the extremes considered to have non-zero EV.

## 6. Output

The tool provides the following outputs:

1.  **Maximum Expected Profit:** The optimal value of the objective function, representing the highest achievable average profit per hand given the constraints and parameters.
2.  **Optimal Bet Sizes:** A list or array containing the calculated optimal bet `x_i` for each count state *i*. Samples are displayed in the text area.
3.  **Plot:** A graph visualizing the optimal bet size (`x_i`) against the count state (*i*), clearly showing how the bet should vary with the count.

## 7. Assumptions and Limitations

*   **Uniform State Probability:** Assumes each count state is equally likely (`p_i = 1/N`). Real-world state probabilities are non-uniform.
*   **Linear EV Model:** The current model uses a simplified linear distribution of EVs for high and low counts, with neutral counts having zero EV. Actual EV-count relationships can be more complex.
*   **Static EV:** Assumes the EV for a given count state is fixed. In reality, EV can depend on specific rules variations and remaining deck composition.
*   **Risk Neutrality:** The objective maximizes expected value without considering risk (e.g., variance or probability of ruin). Kelly Criterion or other risk-adjusted models could be used for a different perspective.
*   **No Bankroll Constraint:** The basic model doesn't explicitly limit bets based on a total bankroll size.

## 8. Conclusion

The Blackjack Betting Optimization tool provides a practical application of linear programming to determine an optimal betting strategy based on card counting. By inputting relevant parameters like betting limits and expected values associated with count states, users can derive a strategy that maximizes their expected profit per hand under the given assumptions. The visualization helps in understanding the relationship between the count state and the recommended bet size. While based on simplifying assumptions, it serves as a valuable tool for understanding basic optimal betting principles in Blackjack.
