# load_opb.py
# We will load the OBP dataset and do basic preprocessing if necessary.

from obp.dataset import OpenBanditDataset
import pandas as pd
import numpy as np
from pathlib import Path


def load_obp_dataset(campaign="all", behavior_policy="random", 
                     n_rounds=50000, use_raw_csv=False, data_path="./open_bandit_dataset"):
    """
    Load OBP dataset either via OBP API or from raw CSV.

    Args:
        campaign (str): 'all', 'men', or 'women'
        behavior_policy (str): 'random' or 'bts'
        n_rounds (int): Max number of rounds to load
        use_raw_csv (bool): If True, loads full raw CSV via pandas
        data_path (str): Path to local OBP data folder

    Returns:
        If use_raw_csv=False: dict with context, action, reward, pscore, n_actions
        If use_raw_csv=True: pd.DataFrame with full raw data
    """
    if use_raw_csv:
        csv_path = f"{data_path}/{behavior_policy}/{campaign}/{campaign}.csv"
        df = pd.read_csv(csv_path)
        if n_rounds is not None and n_rounds < len(df):
            df = df.iloc[:n_rounds]
        print(f"Loaded raw OBP CSV: {len(df)} rows")
        return df

    # OBP-structured loading
    data_path = Path(data_path)  # Convert to Path object
    dataset = OpenBanditDataset(
        behavior_policy=behavior_policy,
        campaign=campaign,
        data_path=data_path
    )
    bandit_feedback = dataset.obtain_batch_bandit_feedback()
    max_available = bandit_feedback["context"].shape[0]

    if n_rounds is None:
        n_rounds = max_available
    elif n_rounds > max_available:
        print(f"Warning: Requested {n_rounds} rounds, but only {max_available} available.")
        n_rounds = max_available

    data = {
        "context": bandit_feedback["context"][:n_rounds],
        "action": bandit_feedback["action"][:n_rounds],
        "reward": bandit_feedback["reward"][:n_rounds],
        "pscore": bandit_feedback["pscore"][:n_rounds],
        "n_actions": dataset.n_actions,
    }
    print(f"Loaded OBP dataset: {n_rounds} rounds, {data['n_actions']} actions")
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

# Run as script

if __name__ == "__main__":
    data = load_obp_dataset()
    preview_dataset(data)



