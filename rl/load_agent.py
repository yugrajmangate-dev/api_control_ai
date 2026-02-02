import pickle
import numpy as np
import os
from collections import defaultdict
from rl.agent import QLearningAgent

def load_trained_agent(action_size, virus_name="COVID-19"):
    """
    Load a trained Q-Learning agent from pickle file
    
    Args:
        action_size: Number of available actions
        virus_name: Name of virus model (matches VIRUS_CONFIGS keys)
    
    Returns:
        QLearningAgent with loaded Q-table
    """
    # Standardize filename (must match train.py format)
    virus_name_clean = virus_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "")
    filename = f"rl/q_table_{virus_name_clean}.pkl"
    
    # Also try alternative formats for backward compatibility
    alternative_filenames = [
        filename,
        f"rl/q_table_{virus_name.lower().replace(' ', '_').replace('-', '_')}.pkl",
        f"rl/q_table_{virus_name.lower()}.pkl",
        "rl/q_table_covid19.pkl",  # Legacy format
        "rl/q_table.pkl"  # Generic fallback
    ]
    
    # Try to find an existing Q-table file
    loaded_file = None
    for attempt_filename in alternative_filenames:
        if os.path.exists(attempt_filename):
            filename = attempt_filename
            loaded_file = attempt_filename
            break
    
    if loaded_file is None:
        raise FileNotFoundError(
            f"No trained Q-table found. Tried:\n" + 
            "\n".join([f"  - {f}" for f in alternative_filenames]) +
            f"\n\nPlease run 'python rl/train.py' first to train the agent."
        )
    
    # Load Q-table
    try:
        with open(filename, "rb") as f:
            loaded_q_table = pickle.load(f)
        
        print(f"✅ Loaded Q-table from: {filename}")
        print(f"   States in Q-table: {len(loaded_q_table)}")
        
    except Exception as e:
        raise RuntimeError(f"Failed to load Q-table from {filename}: {e}")
    
    # Create agent and load Q-table
    agent = QLearningAgent(action_size=action_size)
    agent.q_table = defaultdict(lambda: np.zeros(action_size))
    
    # Copy loaded values
    for state, values in loaded_q_table.items():
        # Ensure values are numpy array
        if isinstance(values, list):
            values = np.array(values)
        agent.q_table[state] = values
    
    # Disable exploration for deployment
    agent.epsilon = 0.0
    
    print(f"   Agent ready (epsilon={agent.epsilon})")
    
    return agent

