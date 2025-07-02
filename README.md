# Contextual Bandits from Real and Synthetic Data: Online Learning and Offline Policy Evaluation

**Final Project – Reinforcement Learning**  
**Authors:** Marvin Ernst, Oliver Tausendschön, Timothy Cassel  
**Institution:** Barcelona School of Economics  
**Year:** 2025

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue?logo=python">
</p>

---

## Project Overview

This project investigates the performance of **contextual bandit algorithms** using both **real-world data** (from the Open Bandit Pipeline) and a **synthetic benchmark environment**. We focus on understanding algorithm behavior in realistic offline settings and explore the challenges of **off-policy evaluation (OPE)** using logged data.

### Main Objectives
- Compare the performance of **LinUCB**, **Thompson Sampling**, and **$\epsilon$-Greedy** strategies under various hyperparameter settings.
- Evaluate policies both in **online simulation** and **true offline policy evaluation** settings.
- Analyze the impact of reward sparsity, action space size, and estimator variance.
- Use robust OPE estimators: **Inverse Propensity Weighting (IPW)**, **Direct Method (DM)**, and **Doubly Robust (DR)**.

---

## Algorithms and Policies

Implemented bandit policies:
- `RandomPolicy` - Uniformly random baseline.
- `LinUCB` - Linear UCB with varying exploration levels ($\alpha$ = 0.0, 0.1, 0.5, 1.0).
- `LinTS` - Linear Thompson Sampling with varying exploration scales and priors.
- `LinEpsilonGreedy` - Linear $\epsilon$-Greedy with $\epsilon$ = 0.1.

---

## Experiments

We perform three main types of evaluations:

### 1. **Logged Bandit Replay** (selective update)
- Simulates online learning by only updating when the logged action matches the selected action.
- Reveals biases and pitfalls of naive online replay in offline settings.

### 2. **Synthetic Benchmarking**
- Ground-truth environment with known reward function.
- Evaluates regret and reward across multiple runs to validate algorithm performance.

### 3. **True Offline Policy Evaluation**
- Evaluates fixed policies using OPE estimators (IPW, DM, DR).
- Applied to both:
  - Reduced dataset (Top-3 Arms)
  - Full dataset (80 Arms)

---

## Dependencies

All experiments were run in **Python 3.12**, with the following main packages:

- `numpy`, `pandas`, `scikit-learn`
- `matplotlib`, `seaborn`
- `obp` (Open Bandit Pipeline)

We recommend managing the environment with `poetry` or `uv` for reproducibility.

---

## References

- **Open Bandit Pipeline (OBP)**  
  *Saito et al., NeurIPS 2020*  
  [GitHub](https://github.com/st-tech/zr-obp) | [Paper](https://arxiv.org/abs/2008.07146)

- **Bandit Algorithms for Website Optimization** - Scott, 2010  
- **A Survey on Contextual Bandits** - Zhou, 2015

---

## Notes

This project was an educational effort as part of the Reinforcement Learning course at BSE. We acknowledge that not all of the strategies explored represent best practices, but they helped us deepen our understanding of contextual bandits and the challenges of offline evaluation in real-world data environments.

---

## Contact

For questions or collaboration ideas, feel free to reach out to:

- Marvin Ernst – [marvin.ernst@bse.eu](mailto:marvin.ernst@bse.eu)  
- Oliver Tausendschön – [oliver.tausendschoen@bse.eu](mailto:oliver.tausendschoen@bse.eu)  
- Timothy Cassel – [timothy.cassel@bse.eu](mailto:timothy.cassel@bse.eu)

---
