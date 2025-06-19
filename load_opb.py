# load_opb.py
# We will load the OBP dataset and do basic preprocessing if necessary.

#%%
from obp.dataset import OpenBanditDataset
import pandas as pd
import numpy as np

#%%

def load_obp_dataset(campaign="all", behavior_policy="random", n_rounds = None):
    """
    Loads Open Bandit Pipeline data.

    Args:
        campaign (str): "all", "men", or "women"
        behavior_policy (str): "random" or "bts"

    Returns:
        dict: Contains contexts, actions, rewards, propensities, and number of actions
    """
    dataset = OpenBanditDataset(
        behavior_policy=behavior_policy,
        campaign=campaign
    )

    # Simulate bandit feedback (offline log)
    bandit_feedback = dataset.obtain_batch_bandit_feedback()

    # Structure it into a simpler format
    data = {
        "context": bandit_feedback["context"],
        "action": bandit_feedback["action"],
        "reward": bandit_feedback["reward"],
        "pscore": bandit_feedback["pscore"],
        "n_actions": dataset.n_actions,
    }
    if n_rounds is not None:
        # Limit the dataset to the first n_rounds
        data["context"] = data["context"][:n_rounds]
        data["action"] = data["action"][:n_rounds]
        data["reward"] = data["reward"][:n_rounds]
        data["pscore"] = data["pscore"][:n_rounds]
    return data

def preview_dataset(data):
    """
    Preview the dataset structure.

    Args:
        data (dict): The dataset dictionary containing context, action, reward, and propensity score.
    """
    print("Dataset loaded!")
    print("Context shape:", data["context"].shape)
    print("Action shape:", data["action"].shape)
    print("Reward shape:", data["reward"].shape)
    print("Propensity score shape:", data["pscore"].shape)
    print("Number of actions:", data["n_actions"])
    # Print first entries
    print("\nFirst entries:")
    print("context", data['context'][0])
    print("action", data['action'][0])
    print("reward", data['reward'][0])
    print("propensity", data['pscore'][0])

# from the output, we can see:
# A user (or session) had a specific context vector — likely a sparse encoding (e.g., one-hot features)
# The system showed item 14
# The user did not click on it (reward = 0)
# The logging policy had a 1.25% probability of choosing that item in this context

#%% Run as script

if __name__ == "__main__":
    data = load_obp_dataset()
    preview_dataset(data)

# %%


