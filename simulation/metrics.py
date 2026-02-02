def init_metrics():
    return {
        "overall": {"S": [], "E": [], "I": [], "R": [], "D": []},
        "children": {"S": [], "E": [], "I": [], "R": [], "D": []},
        "adults": {"S": [], "E": [], "I": [], "R": [], "D": []},
        "cumulative_infections": 0,
        "total_deaths": 0,
        "new_infections_per_day": [],
        "Rt": [],  # Effective reproduction number over time
        "attack_rate": 0.0,
        "incidence_rate": []
    }


def record_metrics(metrics, population, mortality_rate=0.0, generation_time=5.0):
    # Vectorized counting - much faster than repeated list comprehensions
    import numpy as np
    
    # Count states for overall population
    state_counts = {"S": 0, "E": 0, "I": 0, "R": 0, "D": 0}
    child_counts = {"S": 0, "E": 0, "I": 0, "R": 0, "D": 0}
    adult_counts = {"S": 0, "E": 0, "I": 0, "R": 0, "D": 0}
    
    for agent in population:
        state = agent.get("state", "S")
        age_group = agent.get("age_group", "adult")
        
        state_counts[state] += 1
        
        if age_group == "child":
            child_counts[state] += 1
        else:
            adult_counts[state] += 1
    
    # Track cumulative infections (E + I + R + D = all who were infected)
    current_infections = state_counts["E"] + state_counts["I"] + state_counts["R"] + state_counts["D"]
    prev_cumulative = metrics.get("cumulative_infections", 0)
    if current_infections > prev_cumulative:
        metrics["cumulative_infections"] = current_infections
    
    # Track new infections per day (for Rt calculation)
    new_infections = current_infections - prev_cumulative
    metrics["new_infections_per_day"].append(new_infections)
    
    # Calculate Rt (effective reproduction number) using exponential growth method
    # Rt = (I_t / I_(t-τ))^(τ/generation_time) where τ is the time window
    if len(metrics["overall"]["I"]) >= int(generation_time) + 1:
        current_I = state_counts["I"]
        past_I = metrics["overall"]["I"][-int(generation_time)]
        if past_I > 0 and current_I > 0:
            Rt = (current_I / past_I) ** (generation_time / generation_time)
            # Cap Rt at reasonable bounds
            Rt = max(0.0, min(Rt, 10.0))
        else:
            Rt = 0.0
        metrics["Rt"].append(Rt)
    else:
        metrics["Rt"].append(0.0)
    
    # Calculate attack rate (cumulative infections / initial susceptible)
    total_pop = len(population)
    if total_pop > 0:
        metrics["attack_rate"] = current_infections / total_pop
    
    # Calculate incidence rate (new cases per 100,000 per day)
    incidence = (new_infections / total_pop * 100000) if total_pop > 0 else 0.0
    metrics["incidence_rate"].append(incidence)
    
    # Count deaths from recovered population using mortality rate
    if "total_deaths" not in metrics:
        metrics["total_deaths"] = 0
    
    # Append counts
    for state in ["S", "E", "I", "R", "D"]:
        metrics["overall"][state].append(state_counts.get(state, 0))
        metrics["children"][state].append(child_counts.get(state, 0))
        metrics["adults"][state].append(adult_counts.get(state, 0))
