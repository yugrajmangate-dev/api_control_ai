import numpy as np
try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:
    import gym
    from gym import spaces

from env.population import generate_population
from env.seir import seed_infection, update_seir
from env.policies import apply_policy, apply_policy_batch
from simulation.metrics import init_metrics, record_metrics


class EpiControlEnv(gym.Env):
    """
    RL environment for epidemic control
    """

    def __init__(self, population_size=1000, days=60, virus_config=None):
        super().__init__()

        self.population_size = population_size
        self.days = days
        self.current_day = 0
        self.virus_config = virus_config

        # ---- ACTION SPACE ----
        # 0: No policy
        # 1: Mask
        # 2: School closure
        # 3: Mask + School closure
        # 4: Vaccination
        self.action_space = spaces.Discrete(5)

        # ---- OBSERVATION SPACE ----
        # [total_infected, child_infected, adult_infected, hospital_load, econ_cost]
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(5,), dtype=np.float32
        )

        self.reset()

    # ----------------------------------------------------
    def reset(self):
        self.population = generate_population(self.population_size, virus_config=self.virus_config)
        seed_infection(self.population, initial_infected=10)

        self.metrics = init_metrics()
        self.current_day = 0
        self.total_cost = 0.0

        return self._get_observation()

    # ----------------------------------------------------
    def step(self, action):
        policy = self._action_to_policy(action)

        apply_policy_batch(self.population, policy)

        record_metrics(self.metrics, self.population)
        update_seir(self.population)

        reward = self._calculate_reward(policy)

        self.current_day += 1
        done = self.current_day >= self.days

        obs = self._get_observation()

        return obs, reward, done, {}

    # ----------------------------------------------------
    def _get_observation(self):
        pop = self.population

        total = len(pop)
        infected = sum(a["state"] == "I" for a in pop)

        child_inf = sum(
            a["state"] == "I" and a["age_group"] == "child" for a in pop
        )
        adult_inf = sum(
            a["state"] == "I" and a["age_group"] == "adult" for a in pop
        )

        hospital_load = adult_inf / total
        econ_cost = self.total_cost

        return np.array([
            infected / total,
            child_inf / total,
            adult_inf / total,
            hospital_load,
            econ_cost
        ], dtype=np.float32)

    # ----------------------------------------------------
    def _action_to_policy(self, action):
        policy = {
            "mask_mandate": False,
            "school_closure": False,
            "vaccination": False
        }

        if action == 1:
            policy["mask_mandate"] = True
        elif action == 2:
            policy["school_closure"] = True
        elif action == 3:
            policy["mask_mandate"] = True
            policy["school_closure"] = True
        elif action == 4:
            policy["vaccination"] = True

        return policy

    # ----------------------------------------------------
    def _calculate_reward(self, policy):
        infected_ratio = sum(
            a["state"] == "I" for a in self.population
        ) / self.population_size

        # Economic penalty
        cost = 0
        if policy["school_closure"]:
            cost += 0.2
        if policy["mask_mandate"]:
            cost += 0.1
        if policy["vaccination"]:
            cost += 0.15

        self.total_cost += cost

        # Reward (negative loss)
        reward = - (infected_ratio * 10 + cost)

        return reward
