
import numpy as np

def linucb_step(x, true_action, true_reward, A, b, alpha):
    n_actions = len(A)
    p = []
    for a in range(n_actions):
        A_inv = np.linalg.inv(A[a]) # Inverse of the design matrix for action a
        theta_hat = np.dot(A_inv, b[a]) # Ridge regression estimate
        exploit = np.dot(x, theta_hat)# Predicted reward
        explore = alpha * np.sqrt(np.dot(x, np.dot(A_inv, x)))# Exploration term, confidence bonus
        p.append(exploit + explore)

    chosen_action = np.argmax(p)

    # Update model for chosen action only if it matches logged action:
    if chosen_action == true_action:
        A[chosen_action] += np.outer(x, x) # Update design matrix for chosen action (XTX = sum x_i x_i^T for all i where action a was chosen)
        b[chosen_action] += true_reward * x # Update feature vector for chosen action (X^T*y in regression terms)

    return chosen_action, p[chosen_action]

def linucb_all(contexts, actions, rewards, A, b, alpha):
    chosen_actions = []
    ucb_scores = []

    for x, a_true, r in zip(contexts, actions, rewards):
        a_chosen, score = linucb_step(x, a_true, r, A, b, alpha)
        chosen_actions.append(a_chosen)
        ucb_scores.append(score)

    # Final theta estimates for each arm
    theta_list = [np.dot(np.linalg.inv(A[i]), b[i]) for i in range(len(A))]

    return {
        "theta": theta_list,
        "A": A,
        "b": b,
        "chosen_actions": chosen_actions,
        "true_actions": actions,
        "rewards": rewards,
        "ucb_scores": ucb_scores,   
    }
