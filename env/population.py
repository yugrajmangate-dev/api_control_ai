import numpy as np
import random
from config.base_params import AGE_PARAMS

def generate_population(n_agents=1000, virus_config=None, spatial=True, grid_size=1.0):
    """
    Generate population with optional spatial positioning
    
    Args:
        n_agents: Number of agents to create
        virus_config: Virus configuration dictionary
        spatial: Whether to assign (x, y) positions
        grid_size: Size of the spatial grid (0 to grid_size)
    
    Returns:
        List of agent dictionaries
    """
    population = []

    for i in range(n_agents):
        age_group = np.random.choice(
            ["child", "adult"], p=[0.3, 0.7]
        )

        base_immunity = AGE_PARAMS[age_group]["immunity"]

        if virus_config and age_group == "child":
            base_immunity += virus_config["child_immunity_boost"]

        agent = {
            "id": i,
            "age_group": age_group,
            "state": "S",
            "days_in_state": 0,
            "immunity": min(base_immunity, 0.95),
            "severity": AGE_PARAMS[age_group]["severity"],
            "contact_rate": AGE_PARAMS[age_group]["contact_rate"]
        }
        
        # Add spatial coordinates for geographical visualization
        if spatial:
            agent["x"] = np.random.uniform(0, grid_size)
            agent["y"] = np.random.uniform(0, grid_size)
            agent["home_x"] = agent["x"]  # Home location (for movement)
            agent["home_y"] = agent["y"]

        population.append(agent)

    return population


def update_agent_positions(population, movement_radius=0.1):
    """
    Simulate agent movement within a limited radius
    
    Args:
        population: List of agents
        movement_radius: Maximum distance agents can move from home
    """
    for agent in population:
        if "x" not in agent or "y" not in agent:
            continue
        
        # Random walk within movement radius of home
        dx = np.random.uniform(-movement_radius, movement_radius)
        dy = np.random.uniform(-movement_radius, movement_radius)
        
        # Keep agents near their home location
        agent["x"] = np.clip(agent["home_x"] + dx, 0, 1.0)
        agent["y"] = np.clip(agent["home_y"] + dy, 0, 1.0)


def get_nearby_agents(agent, population, radius=0.1):
    """
    Find agents within a certain radius of target agent
    
    Args:
        agent: Target agent
        population: Full population list
        radius: Search radius
    
    Returns:
        List of nearby agents
    """
    if "x" not in agent or "y" not in agent:
        return []
    
    nearby = []
    for other in population:
        if other["id"] == agent["id"]:
            continue
        
        if "x" not in other or "y" not in other:
            continue
        
        # Calculate Euclidean distance
        distance = np.sqrt((agent["x"] - other["x"])**2 + (agent["y"] - other["y"])**2)
        
        if distance <= radius:
            nearby.append(other)
    
    return nearby
