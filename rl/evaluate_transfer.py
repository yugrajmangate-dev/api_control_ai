"""
Transfer Learning Demonstration: City A → City B
Shows how a policy learned in one environment can be applied to another
"""
from rl.env import EpiControlEnv
from rl.agent import QLearningAgent
from rl.utils import discretize_state
from env.city import CITY_A, CITY_B
from env.seir import set_virus_params
from data.virus_configs import VIRUS_CONFIGS
from simulation.metrics import init_metrics, record_metrics
import pickle
import os

print("=" * 60)
print("  TRANSFER LEARNING DEMO: City A → City B")
print("=" * 60)

# ========== STEP 1: LOAD TRAINED AGENT FROM CITY A ==========
print("\n[1] Loading agent trained on City A...")

# Get virus config for consistency
VIRUS_NAME = "COVID-19"
virus_config = VIRUS_CONFIGS[VIRUS_NAME].copy()
set_virus_params(virus_config)

env_A = EpiControlEnv(**CITY_A, virus_config=virus_config)
agent = QLearningAgent(action_size=env_A.action_space.n)

# Try to load pre-trained Q-table
virus_name_clean = VIRUS_NAME.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "")
q_table_path = f"rl/q_table_{virus_name_clean}.pkl"

if os.path.exists(q_table_path):
    with open(q_table_path, "rb") as f:
        agent.q_table = pickle.load(f)
    print(f"✅ Loaded Q-table from {q_table_path}")
    print(f"   Q-table size: {len(agent.q_table)} states")
else:
    print(f"⚠️  No pre-trained model found at {q_table_path}")
    print("   Agent will use random policy (train.py should be run first)")

# Disable exploration for transfer evaluation
agent.epsilon = 0.0
print("   Exploration disabled (epsilon = 0.0)")

# ========== STEP 2: EVALUATE ON CITY A (BASELINE) ==========
print("\n[2] Evaluating on City A (original environment)...")

set_virus_params(virus_config)
obs = env_A.reset()
state = discretize_state(obs)
done = False
total_reward_A = 0
metrics_A = init_metrics()

while not done:
    action = agent.choose_action(state)
    obs, reward, done, _ = env_A.step(action)
    state = discretize_state(obs)
    total_reward_A += reward
    record_metrics(metrics_A, env_A.population)

peak_infected_A = max(metrics_A["overall"]["I"])
final_recovered_A = metrics_A["overall"]["R"][-1]

print(f"   Total Reward: {total_reward_A:.2f}")
print(f"   Peak Infected: {peak_infected_A}")
print(f"   Final Recovered: {final_recovered_A}")

# ========== STEP 3: DEPLOY ON CITY B (TRANSFER) ==========
print("\n[3] Deploying on City B (transfer learning)...")
print(f"   Population: {CITY_A['population_size']} → {CITY_B['population_size']}")

env_B = EpiControlEnv(**CITY_B, virus_config=virus_config)

set_virus_params(virus_config)
obs = env_B.reset()
state = discretize_state(obs)
done = False
total_reward_B = 0
metrics_B = init_metrics()

action_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

while not done:
    action = agent.choose_action(state)
    action_counts[action] += 1
    
    obs, reward, done, _ = env_B.step(action)
    state = discretize_state(obs)
    total_reward_B += reward
    record_metrics(metrics_B, env_B.population)

peak_infected_B = max(metrics_B["overall"]["I"])
final_recovered_B = metrics_B["overall"]["R"][-1]

print(f"   Total Reward: {total_reward_B:.2f}")
print(f"   Peak Infected: {peak_infected_B}")
print(f"   Final Recovered: {final_recovered_B}")

# ========== STEP 4: ANALYSIS ==========
print("\n" + "=" * 60)
print("  TRANSFER LEARNING RESULTS")
print("=" * 60)

print("\n📊 Performance Comparison:")
print(f"   City A Reward: {total_reward_A:.2f}")
print(f"   City B Reward: {total_reward_B:.2f}")
print(f"   Reward Change: {((total_reward_B - total_reward_A) / abs(total_reward_A) * 100):+.1f}%")

print("\n🦠 Infection Metrics:")
print(f"   Peak Infected A: {peak_infected_A} ({peak_infected_A/CITY_A['population_size']*100:.1f}%)")
print(f"   Peak Infected B: {peak_infected_B} ({peak_infected_B/CITY_B['population_size']*100:.1f}%)")

print("\n💊 Recovery Metrics:")
print(f"   Final Recovered A: {final_recovered_A} ({final_recovered_A/CITY_A['population_size']*100:.1f}%)")
print(f"   Final Recovered B: {final_recovered_B} ({final_recovered_B/CITY_B['population_size']*100:.1f}%)")

print("\n🎯 Policy Actions Used (City B):")
action_names = {
    0: "No Action",
    1: "Mask Mandate",
    2: "School Closure",
    3: "Mask + School",
    4: "Vaccination"
}

for action_id, count in action_counts.items():
    percentage = (count / sum(action_counts.values())) * 100
    print(f"   {action_names[action_id]}: {count} times ({percentage:.1f}%)")

print("\n✅ Transfer Learning Evaluation Complete!")
print("=" * 60)

# ========== STEP 5: SAVE RESULTS ==========
transfer_results = {
    "city_a": {
        "reward": total_reward_A,
        "peak_infected": peak_infected_A,
        "final_recovered": final_recovered_A,
        "population": CITY_A["population_size"]
    },
    "city_b": {
        "reward": total_reward_B,
        "peak_infected": peak_infected_B,
        "final_recovered": final_recovered_B,
        "population": CITY_B["population_size"]
    },
    "action_distribution": action_counts
}

with open("rl/transfer_results.pkl", "wb") as f:
    pickle.dump(transfer_results, f)

print("\n💾 Results saved to rl/transfer_results.pkl")

