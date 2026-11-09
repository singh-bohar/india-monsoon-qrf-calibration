# Coin Test (Binomial Test) for Ranked Probability Scores (RPS)

This markdown file provides an overview of the **coin test (binomial test)** for evaluating the significance of differences in Ranked Probability Scores (RPS). This statistical method is commonly used to determine whether the observed difference between two forecasting methods is statistically significant.

---

## **Background**

The **Ranked Probability Score (RPS)** is a commonly used metric to evaluate probabilistic forecasts, measuring how well the predicted probability distribution matches the observed outcomes. When comparing two forecasting methods (e.g., Model A and Model B), we aim to assess whether one model significantly outperforms the other in terms of RPS.

The **coin test** (or binomial test) evaluates whether the observed differences in RPS between two models are likely to have occurred by chance, assuming no inherent superiority of one model over the other.

---

## **Methodology**

### **1. Pairwise Comparison of RPS**
- For each forecast instance (e.g., each grid point or observation), compute the RPS for both models:
  - $` RPS_A `$ for Model A
  - $` RPS_B `$ for Model B
- Calculate the difference in RPS:
```math
  \Delta RPS = RPS_B - RPS_A
```

### **2. Determine Win/Loss/Tie**
- Assign outcomes based on $` \Delta RPS `$:
  - **Win for Model A:** $` \Delta RPS > 0 `$
  - **Win for Model B:** $` \Delta RPS < 0 `$
  - **Tie:** $` \Delta RPS = 0 `$

### **3. Perform Binomial Test**
- Let \( n \) represent the number of non-tie observations.
- Let \( k \) represent the number of instances where Model A wins $` \Delta RPS > 0 `$.
- The null hypothesis assumes that each model has a 50% chance of winning, i.e., the outcomes are equally likely:
```math
  H_0: p = 0.5
```
- The binomial test evaluates the probability of observing at least $` k `$ wins for Model A (or Model B, depending on the test direction) under $` H_0 `$.

The p-value is computed as:
```math
P(X \geq k) = \sum_{i=k}^{n} \binom{n}{i} p^i (1-p)^{n-i}
```
where p = 0.5.

---

## **Interpretation**

- If the p-value is **less than the significance level** (e.g., $` \alpha = 0.05 `$), we reject the null hypothesis and conclude that one model significantly outperforms the other.
- A high p-value indicates no significant difference between the models.

---

## **Practical Example**

### **Input Data**
| Instance | \( RPS_A \) | \( RPS_B \) | \( \Delta RPS \) | Outcome         |
|----------|-------------|-------------|------------------|-----------------|
| 1        | 0.20        | 0.25        | -0.05            | Win for B       |
| 2        | 0.15        | 0.18        | -0.03            | Win for B       |
| 3        | 0.12        | 0.11        | 0.01             | Win for A       |
| 4        | 0.10        | 0.10        | 0.00             | Tie             |

### **Step-by-Step Calculation**
1. Total non-tie instances: $` n = 3 `$
2. Wins for Model A: $` k = 1 `$
3. Perform binomial test:
```math
   P(X \geq 1) = \binom{3}{1} (0.5)^1 (0.5)^2 + \binom{3}{2} (0.5)^2 (0.5)^1 + \binom{3}{3} (0.5)^3
```
   
   Simplifying:
   ```math
   P(X \geq 1) = 0.375 + 0.375 + 0.125 = 0.875
   ```

5. p-value = 0.875.

### **Conclusion**
- With a p-value of 0.875 (greater than $`\alpha = 0.05 `$), we fail to reject the null hypothesis, indicating no significant difference in RPS performance.

---

## **Key Assumptions**
- The outcomes are independent.
- Each forecast instance is equally likely to favor either model under the null hypothesis.

---

## **Implementation**

This test can be implemented using Python's `scipy.stats.binom_test` function. Below is a sample code snippet:

```python
from scipy.stats import binom_test

# Example data
n = 3  # Number of non-tie observations
k = 1  # Wins for Model A

# Perform binomial test
p_value = binom_test(k, n, p=0.5, alternative='greater')
print(f"P-value: {p_value}")
```
