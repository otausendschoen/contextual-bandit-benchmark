#### LinTS ####
import numpy as np

def ts_linear_all(contexts, actions, rewards, alpha=1.0, lambda_prior=1.0):
    n_rounds, context_dim = contexts.shape
    n_actions = len(np.unique(actions))

    A = [lambda_prior * np.identity(context_dim) for _ in range(n_actions)]
    b = [np.zeros(context_dim) for _ in range(n_actions)]

    chosen_actions = []
    theta_samples = []

    for t in range(n_rounds):
        x = contexts[t]
        sampled_thetas = []

        for a in range(n_actions):
            A_inv = np.linalg.inv(A[a])
            mu = A_inv @ b[a]
            cov = alpha**2 * A_inv  # scale variance by alpha
            theta_sample = np.random.multivariate_normal(mu, cov)
            sampled_thetas.append(theta_sample)

        rewards_hat = [x @ theta for theta in sampled_thetas]
        chosen_action = np.argmax(rewards_hat)

        # update only if action matches the logged one
        if chosen_action == actions[t]:
            A[chosen_action] += np.outer(x, x)
            b[chosen_action] += rewards[t] * x

        chosen_actions.append(chosen_action)
        theta_samples.append(sampled_thetas)

    return {
        "chosen_actions": chosen_actions,
        "theta_samples": theta_samples,
        "rewards": rewards,
        "true_actions": actions,
    }