# Safer Evaluation

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

def evaluate_random_policy(seed=123):
    # Load data
    X_context = np.load("processed_top3/context_reduced.npy")
    actions = np.load("processed_top3/actions.npy")
    rewards = np.load("processed_top3/rewards.npy")
    pscores = np.load("processed_top3/pscores.npy")
    n_arms = len(np.unique(actions))
    
    # Shuffle data
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X_context))
    X_context = X_context[idx]
    actions = actions[idx]
    rewards = rewards[idx]
    pscores = pscores[idx]

    # One-hot encode
    onehot = OneHotEncoder(sparse_output=False)
    a_logged_1hot = onehot.fit_transform(actions.reshape(-1, 1))
    X_train = np.hstack([X_context, a_logged_1hot])

    # Train reward model
    reward_model = RandomForestRegressor(n_estimators=100, random_state=seed)
    reward_model.fit(X_train, rewards)

    # Simulated random actions
    a_sim = rng.integers(0, n_arms, size=len(X_context))
    a_sim_1hot = onehot.transform(a_sim.reshape(-1, 1))
    X_sim = np.hstack([X_context, a_sim_1hot])
    r_hat_sim = reward_model.predict(X_sim)

    # DR correction
    matches = a_sim == actions
    correction = np.zeros_like(rewards)
    correction[matches] = (rewards[matches] - r_hat_sim[matches]) / pscores[matches]
    dr_sim = r_hat_sim + correction

    return dr_sim


# to run on multiple seeds:
if __name__ == "__main__":
    X_context = np.load("processed_top3/context_reduced.npy")
    avg_curve = np.zeros(len(X_context))

    for seed in range(30):
        dr = evaluate_random_policy(seed)
        avg_curve += np.cumsum(dr)

    avg_curve /= 30
    np.save("results/dr_random_avg.npy", avg_curve)