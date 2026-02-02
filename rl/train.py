from rl.env import EpiControlEnv
from rl.agent import QLearningAgent
from rl.utils import discretize_state
from env.seir import set_virus_params
from data.virus_configs import VIRUS_CONFIGS

import pickle
import os
import time
import numpy as np

# =====================
# CONFIG
# =====================
EPISODES = 200
POP_SIZE = 1000
DAYS = 60
VIRUS_NAME = "COVID-19"   # Choose from VIRUS_CONFIGS keys

# =====================
# LOAD VIRUS PARAMETERS
# =====================
if VIRUS_NAME not in VIRUS_CONFIGS:
    print(f"⚠️  Warning: '{VIRUS_NAME}' not found in VIRUS_CONFIGS")
    print(f"Available viruses: {list(VIRUS_CONFIGS.keys())}")
    print("Using 'COVID-19' as default...")
    VIRUS_NAME = "COVID-19"

virus_config = VIRUS_CONFIGS[VIRUS_NAME].copy()
set_virus_params(virus_config)

print("=" * 60)
print(f"  RL TRAINING: {VIRUS_NAME}")
print("=" * 60)
print(f"Episodes: {EPISODES}")
print(f"Population: {POP_SIZE}")
print(f"Days per Episode: {DAYS}")
print(f"Virus R0: {virus_config['R0']}")
print(f"Base Beta: {virus_config['base_beta']}")
print(f"Incubation: {virus_config['incubation_days']} days")
print(f"Infectious: {virus_config['infectious_days']} days")
print("=" * 60)

# =====================
# ENV + AGENT
# =====================
env = EpiControlEnv(population_size=POP_SIZE, days=DAYS, virus_config=virus_config)
agent = QLearningAgent(action_size=env.action_space.n)

print(f"\nAction Space: {env.action_space.n} actions")
print(f"Observation Space: {env.observation_space.shape}")
print(f"Learning Rate (α): {agent.alpha}")
print(f"Discount Factor (γ): {agent.gamma}")
print(f"Initial Epsilon: {agent.epsilon}")
print(f"Epsilon Decay: {agent.epsilon_decay}")
print(f"Min Epsilon: {agent.epsilon_min}")
print("\nStarting training...")

# =====================
# TRAINING LOOP
# =====================
reward_history = []
start_time = time.time()

for episode in range(EPISODES):
    # Reset virus parameters each episode (in case they changed)
    set_virus_params(virus_config)
    
    obs = env.reset()
    state = discretize_state(obs)
    done = False
    total_reward = 0
    steps = 0

    while not done:
        action = agent.choose_action(state)
        next_obs, reward, done, _ = env.step(action)
        next_state = discretize_state(next_obs)

        agent.learn(state, action, reward, next_state)

        state = next_state
        total_reward += reward
        steps += 1

    agent.decay_epsilon()
    reward_history.append(total_reward)

    if episode % 20 == 0:
        avg_reward = np.mean(reward_history[-20:]) if len(reward_history) >= 20 else np.mean(reward_history)
        print(f"Episode {episode:3d}/{EPISODES} | Reward: {total_reward:7.2f} | Avg: {avg_reward:7.2f} | Epsilon: {agent.epsilon:.3f} | States: {len(agent.q_table)}")

training_time = time.time() - start_time

print("\n✅ Training completed!")
print(f"   Training time: {training_time:.1f} seconds ({training_time/60:.1f} minutes)")
print(f"   Average reward (last 20): {np.mean(reward_history[-20:]):.2f}")
print(f"   Best reward: {max(reward_history):.2f}")
print(f"   Worst reward: {min(reward_history):.2f}")

# =====================
# SAFE Q-TABLE SAVE
# =====================
print("\n💾 Saving Q-table...")

# Create rl directory if it doesn't exist
os.makedirs("rl", exist_ok=True)

# Convert defaultdict to regular dict for safe pickling
q_table_safe = {}
for state, values in agent.q_table.items():
    # Ensure values are numpy arrays
    if isinstance(values, np.ndarray):
        q_table_safe[state] = values.copy()
    else:
        q_table_safe[state] = np.array(values)

# Standardize filename (must match load_agent.py format)
virus_name_clean = VIRUS_NAME.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "")
filename = f"rl/q_table_{virus_name_clean}.pkl"

try:
    with open(filename, "wb") as f:
        pickle.dump(q_table_safe, f)
    print(f"✅ Q-table saved successfully as: {filename}")
except Exception as e:
    print(f"❌ Error saving Q-table: {e}")
    raise

print(f"   States learned: {len(q_table_safe)}")
print(f"   Final epsilon: {agent.epsilon:.4f}")

# Validate saved file
try:
    with open(filename, "rb") as f:
        test_load = pickle.load(f)
    print(f"   Validation: ✅ File loads correctly ({len(test_load)} states)")
except Exception as e:
    print(f"   Validation: ❌ File corrupted: {e}")

# =====================
# SAVE TRAINING METADATA
# =====================
metadata = {
    "virus_name": VIRUS_NAME,
    "virus_config": virus_config,
    "episodes": EPISODES,
    "population_size": POP_SIZE,
    "days": DAYS,
    "final_epsilon": agent.epsilon,
    "states_learned": len(q_table_safe),
    "training_time_seconds": training_time,
    "avg_reward_last_20": float(np.mean(reward_history[-20:])),
    "best_reward": float(max(reward_history)),
    "worst_reward": float(min(reward_history)),
    "reward_history": [float(r) for r in reward_history],
    "hyperparameters": {
        "alpha": agent.alpha,
        "gamma": agent.gamma,
        "epsilon_decay": agent.epsilon_decay,
        "epsilon_min": agent.epsilon_min
    }
}

metadata_file = filename.replace(".pkl", "_metadata.pkl")
try:
    with open(metadata_file, "wb") as f:
        pickle.dump(metadata, f)
    print(f"   Metadata saved as: {metadata_file}")
except Exception as e:
    print(f"   Warning: Could not save metadata: {e}")

print("\n" + "=" * 60)
print("   TRAINING SUMMARY")
print("=" * 60)
print(f"   Virus Model: {VIRUS_NAME}")
print(f"   Episodes Completed: {EPISODES}")
print(f"   States Explored: {len(q_table_safe)}")
print(f"   Training Time: {training_time/60:.1f} minutes")
print(f"   Final Performance: {np.mean(reward_history[-20:]):.2f} avg reward")
print(f"   Files Created:")
print(f"      - {filename}")
print(f"      - {metadata_file}")
print("=" * 60)
print("\n✅ Ready to use! Run 'streamlit run app.py' to test the agent.")
print("=" * 60)
