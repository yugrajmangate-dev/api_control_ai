"""
Mutation Event System for Virus Evolution
Tracks infection rates and triggers mutations when conditions are met
"""
import numpy as np
import copy


class MutationTracker:
    """Tracks mutation events during simulation with biological context"""
    
    def __init__(self):
        self.mutations = []
        self.current_strain = 0
        self.mutation_count = 0
        self.last_mutation_day = -999  # Track cooldown
    
    def log_mutation(self, day, trigger_reason, old_params, new_params):
        """Record mutation event with changed parameters"""
        mutation_event = {
            "day": day,
            "strain_number": self.mutation_count + 1,
            "trigger": trigger_reason,
            "changes": {
                "R0": {
                    "old": old_params.get("R0", 0),
                    "new": new_params.get("R0", 0),
                    "change_pct": ((new_params.get("R0", 0) - old_params.get("R0", 0)) / old_params.get("R0", 1)) * 100
                },
                "base_beta": {
                    "old": old_params.get("base_beta", 0),
                    "new": new_params.get("base_beta", 0),
                    "change_pct": ((new_params.get("base_beta", 0) - old_params.get("base_beta", 0)) / old_params.get("base_beta", 1)) * 100
                },
                "infectious_days": {
                    "old": old_params.get("infectious_days", 0),
                    "new": new_params.get("infectious_days", 0)
                },
                "mortality_rate": {
                    "old": old_params.get("mortality_rate", 0),
                    "new": new_params.get("mortality_rate", 0),
                    "change_pct": ((new_params.get("mortality_rate", 0) - old_params.get("mortality_rate", 0)) / old_params.get("mortality_rate", 0.001)) * 100
                }
            }
        }
        
        self.mutations.append(mutation_event)
        self.mutation_count += 1
        return mutation_event
    
    def get_summary(self):
        """Get summary of all mutations"""
        return {
            "total_mutations": self.mutation_count,
            "events": self.mutations
        }


def check_mutation_trigger(population, day, mutation_config=None, previous_mutations=0):
    """
    Check if mutation should occur based on biological factors:
    - Viral replication cycles (high viral load = more replication errors)
    - Transmission chains (longer chains = more opportunities)
    - Population immunity pressure (selective advantage for escape variants)
    
    Args:
        population: List of agents
        day: Current simulation day
        mutation_config: Dictionary with thresholds (optional)
        previous_mutations: Number of mutations already occurred
    
    Returns:
        (should_mutate: bool, trigger_reason: str)
    """
    if mutation_config is None:
        mutation_config = {
            "infection_threshold": 0.30,  # 30% infected
            "min_day": 14,                # Don't mutate before day 14
            "max_mutations": 3,           # Maximum 3 mutations per simulation
            "cooldown_days": 15           # Wait at least 15 days between mutations
        }
    
    # Don't mutate too early (need viral replication cycles)
    if day < mutation_config.get("min_day", 14):
        return False, None
    
    # Limit total mutations (biological constraint)
    if previous_mutations >= mutation_config.get("max_mutations", 3):
        return False, None
    
    # Calculate infection metrics
    total_agents = len(population)
    infected_count = sum(1 for a in population if a["state"] == "I")
    exposed_count = sum(1 for a in population if a["state"] == "E")
    recovered_count = sum(1 for a in population if a["state"] == "R")
    
    infection_rate = infected_count / total_agents if total_agents > 0 else 0
    active_rate = (infected_count + exposed_count) / total_agents if total_agents > 0 else 0
    immunity_rate = recovered_count / total_agents if total_agents > 0 else 0
    
    # Calculate cumulative replication burden (proxy for mutation probability)
    # Higher viral load × longer time = more replication errors
    replication_burden = infected_count * day
    mutation_probability = min(replication_burden / (total_agents * 100), 0.15)  # Cap at 15%
    
    # Biological triggers:
    
    # 1. High viral load (replication errors)
    if infection_rate >= mutation_config.get("infection_threshold", 0.30):
        if np.random.random() < mutation_probability:
            return True, f"High viral replication: {infection_rate:.1%} infected, {mutation_probability:.1%} mutation chance"
    
    # 2. Immune pressure (escape variant advantage)
    if immunity_rate >= 0.40 and active_rate >= 0.10:
        if np.random.random() < 0.20:  # 20% chance under immune pressure
            return True, f"Immune selection pressure: {immunity_rate:.1%} recovered"
    
    # 3. Long transmission chains (accumulated mutations)
    if day > 30 and infected_count > 50:
        if np.random.random() < 0.03:  # 3% chance per day after day 30
            return True, f"Extended transmission chains (day {day})"
    
    # 4. Superspreader-driven mutation (rare but impactful)
    if infection_rate >= 0.20 and np.random.random() < 0.02:
        return True, "Superspreading event mutation"
    
    return False, None


def apply_mutation(virus_config, mutation_severity="moderate", random_variation=True):
    """
    Apply mutation to virus configuration
    
    Args:
        virus_config: Current virus parameters
        mutation_severity: "mild", "moderate", or "severe"
        random_variation: Add randomness to mutation effects
    
    Returns:
        Updated virus_config with mutated parameters
    """
    # Define mutation multipliers
    mutation_profiles = {
        "mild": {
            "R0_mult": (1.1, 1.3),
            "beta_mult": (1.1, 1.25),
            "infectious_days_add": (0, 2),
            "mortality_mult": (1.0, 1.2)
        },
        "moderate": {
            "R0_mult": (1.3, 1.6),
            "beta_mult": (1.25, 1.5),
            "infectious_days_add": (1, 3),
            "mortality_mult": (1.1, 1.4)
        },
        "severe": {
            "R0_mult": (1.6, 2.2),
            "beta_mult": (1.5, 2.0),
            "infectious_days_add": (2, 5),
            "mortality_mult": (1.3, 1.8)
        }
    }
    
    profile = mutation_profiles.get(mutation_severity, mutation_profiles["moderate"])
    
    # Create a copy to avoid modifying original
    new_config = copy.deepcopy(virus_config)
    
    # Apply mutations with random variation
    if random_variation:
        r0_mult = np.random.uniform(*profile["R0_mult"])
        beta_mult = np.random.uniform(*profile["beta_mult"])
        days_add = np.random.randint(*profile["infectious_days_add"])
        mort_mult = np.random.uniform(*profile["mortality_mult"])
    else:
        # Use midpoint values
        r0_mult = np.mean(profile["R0_mult"])
        beta_mult = np.mean(profile["beta_mult"])
        days_add = int(np.mean(profile["infectious_days_add"]))
        mort_mult = np.mean(profile["mortality_mult"])
    
    # Update parameters
    new_config["R0"] = round(new_config["R0"] * r0_mult, 2)
    new_config["base_beta"] = round(new_config["base_beta"] * beta_mult, 3)
    new_config["infectious_days"] = int(new_config["infectious_days"] + days_add)
    new_config["mortality_rate"] = round(new_config["mortality_rate"] * mort_mult, 4)
    
    # Also slightly reduce immunity effectiveness (virus evades immune system)
    if "child_immunity_boost" in new_config:
        new_config["child_immunity_boost"] = max(0, new_config["child_immunity_boost"] - 0.05)
    
    return new_config


def select_mutation_severity(infection_rate, day):
    """
    Determine mutation severity based on infection dynamics
    
    Args:
        infection_rate: Current proportion of infected individuals
        day: Current simulation day
    
    Returns:
        Severity level: "mild", "moderate", or "severe"
    """
    # Higher infection rates and later days tend toward more severe mutations
    severity_score = (infection_rate * 2) + (day / 60)
    
    if severity_score < 0.5:
        return "mild"
    elif severity_score < 1.0:
        return "moderate"
    else:
        return "severe"


# Global mutation tracker instance
_global_tracker = None

def get_mutation_tracker():
    """Get or create global mutation tracker"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = MutationTracker()
    return _global_tracker

def reset_mutation_tracker():
    """Reset global mutation tracker"""
    global _global_tracker
    _global_tracker = MutationTracker()
    return _global_tracker
