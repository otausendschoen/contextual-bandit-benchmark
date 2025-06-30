# Evaluating all policies

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from linucb import linucb_all
from ts_linear import ts_linear_all  # this should contain your Thompson Sampling implementation
import os


def evaluate_policy(policy_label, chosen_actions_fn, save_path, seed=123):
    # Load data
    X_context = np.load("processed_top3/context_reduced.npy")
    actions = np.load("processed_top3/actions.npy")
    rewards = np.load("processed_top3/rewards.npy")
    pscores = np.load("processed_top3/pscores.npy")
    n_rounds, context_dim = X_context.shape

    # Shuffle data
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n_rounds)
    X = X_context[idx]
    a_logged = actions[idx]
    r_logged = rewards[idx]
    p = pscores[idx]

    # Train reward model
    onehot = OneHotEncoder(sparse_output=False)
    a_1hot = onehot.fit_transform(a_logged.reshape(-1, 1))
    X_train = np.hstack([X, a_1hot])

    reward_model = RandomForestRegressor(n_estimators=100, random_state=seed)
    reward_model.fit(X_train, r_logged)

    # Generate chosen actions for policy
    a_chosen = chosen_actions_fn(X, a_logged, r_logged, seed)
    a_chosen_1hot = onehot.transform(a_chosen.reshape(-1, 1))
    X_eval = np.hstack([X, a_chosen_1hot])
    r_hat = reward_model.predict(X_eval)

    matches = a_chosen == a_logged
    correction = np.zeros_like(r_logged)
    correction[matches] = (r_logged[matches] - r_hat[matches]) / p[matches]
    dr = r_hat + correction

    return dr

def run_all_evaluations():
    X_context = np.load("processed_top3/context_reduced.npy")
    n_rounds = len(X_context)
    n_runs = 30
    os.makedirs("results", exist_ok=True)

    linucb_alphas = [0.0, 0.1, 0.25]
    ts_alphas = [0.25, 0.5, 1.0]

    def make_linucb(alpha):
        return lambda X, a, r, seed: linucb_all(
            X, a, r,
            A=[np.identity(X.shape[1]) for _ in range(len(np.unique(a)))],
            b=[np.zeros(X.shape[1]) for _ in range(len(np.unique(a)))],
            alpha=alpha
        )["chosen_actions"]

    def make_ts(alpha):
        return lambda X, a, r, seed: ts_linear_all(X, a, r, alpha=alpha)["chosen_actions"]

    policies = {
        f"LinUCB_alpha_{alpha}": make_linucb(alpha) for alpha in linucb_alphas
    }
    policies.update({
        f"TS_alpha_{alpha}": make_ts(alpha) for alpha in ts_alphas
    })

    for label, policy_fn in policies.items():
        avg_curve = np.zeros(n_rounds)
        for seed in range(n_runs):
            dr = evaluate_policy(label, policy_fn, save_path=None, seed=seed)
            avg_curve += np.cumsum(dr)
        avg_curve /= n_runs
        np.save(f"results/dr_{label}.npy", avg_curve)
        print(f"Saved: results/dr_{label}.npy")


if __name__ == "__main__":
    run_all_evaluations()


def evaluate_ts_lambda(alpha, lam, seed):
    from ts_linear import ts_linear_all

    # Load and shuffle
    X = np.load("processed_top3/context_reduced.npy")
    a_logged = np.load("processed_top3/actions.npy")
    r_logged = np.load("processed_top3/rewards.npy")
    p = np.load("processed_top3/pscores.npy")
    n_rounds = len(X)

    rng = np.random.default_rng(seed)
    idx = rng.permutation(n_rounds)
    X, a_logged, r_logged, p = X[idx], a_logged[idx], r_logged[idx], p[idx]

    # Reward model
    enc = OneHotEncoder(sparse_output=False)
    a_1hot = enc.fit_transform(a_logged.reshape(-1, 1))
    X_train = np.hstack([X, a_1hot])

    model = RandomForestRegressor(n_estimators=100, random_state=seed)
    model.fit(X_train, r_logged)

    # TS predictions
    ts_result = ts_linear_all(X, a_logged, r_logged, alpha=alpha, lambda_prior=lam)
    a_pred = np.array(ts_result["chosen_actions"])
    a_pred_1hot = enc.transform(a_pred.reshape(-1, 1))
    X_eval = np.hstack([X, a_pred_1hot])
    r_hat = model.predict(X_eval)

    match = a_pred == a_logged
    correction = np.zeros_like(r_logged)
    correction[match] = (r_logged[match] - r_hat[match]) / p[match]
    dr = r_hat + correction

    return dr
