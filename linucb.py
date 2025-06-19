from load_opb import load_obp_dataset, preview_dataset
import numpy as np

# Load just 2 samples to inspect
data = load_obp_dataset(n_rounds=2)
preview_dataset(data)

context = data["context"]
action = data["action"]
reward = data["reward"]
n_actions = data["n_actions"]


context_dim = context.shape[1]
alpha = 1.0

# A and b per action
A = [np.identity(context_dim) for _ in range(n_actions)]
b = [np.zeros(context_dim) for _ in range(n_actions)]

x = context[0]               # the context vector
true_action = action[0]      # what the behavior policy chose (not used in LinUCB decision)
true_reward = reward[0]      # the observed reward (used in update)

# Compute UCB scores for each arm
p = []
for a in range(n_actions):
        A_inv = np.linalg.inv(A[a])
        theta_hat = np.dot(A_inv, b[a]) #ridge regression estimate
        exploit = np.dot(x, theta_hat) #predicted reward
        explore = alpha * np.sqrt(np.dot(x, np.dot(A_inv, x))) #exploration term
        p.append(exploit + explore) #combine them

chosen_action = np.argmax(p)
print(f"Chosen action: {chosen_action}")
print(f"True action taken in log: {true_action}")
print(f"Observed reward: {true_reward}")

A[chosen_action] += np.outer(x, x)
b[chosen_action] += true_reward * x

print(f"Updated A[{chosen_action}]:\n", A[chosen_action])
print(f"Updated b[{chosen_action}]:", b[chosen_action])