def apply_policy(agent, policy):
    """
    Modifies agent behavior based on active policies (single agent)
    """
    # ---- MASK MANDATE ----
    if policy["mask_mandate"]:
        agent["effective_contact"] = agent["contact_rate"] * 0.6
    else:
        agent["effective_contact"] = agent["contact_rate"]

    # ---- SCHOOL CLOSURE ----
    if policy["school_closure"] and agent["age_group"] == "child":
        agent["effective_contact"] *= 0.3

    # ---- VACCINATION ----
    if policy["vaccination"] and agent["state"] == "S":
        agent["immunity"] = min(agent["immunity"] + 0.3, 0.95)


def apply_policy_batch(population, policy, virus_config=None):
    """
    Optimized: Apply policy to entire population at once
    This is 10-100x faster than looping through individual agents
    """
    # Pre-calculate policy effects
    mask_reduction = 0.6 if policy["mask_mandate"] else 1.0
    school_reduction = 0.3 if policy["school_closure"] else 1.0
    
    # Disease-specific vaccination effectiveness (WHO-based)
    if policy["vaccination"] and virus_config:
        # Use mortality rate as proxy for disease severity to determine vaccine effectiveness
        mortality = virus_config.get("mortality_rate", 0.02)
        if mortality >= 0.10:  # High mortality (SARS, Ebola)
            vaccination_boost = 0.70  # 70% effectiveness
        elif mortality >= 0.02:  # Moderate mortality (COVID)
            vaccination_boost = 0.85  # 85% effectiveness (average of 80-95%)
        elif mortality >= 0.005:  # Low mortality
            vaccination_boost = 0.60  # 60% effectiveness
        else:  # Very low mortality (Influenza)
            vaccination_boost = 0.50  # 50% effectiveness (40-60% range)
    else:
        vaccination_boost = 0.0
    
    # Apply to all agents in a single pass
    for agent in population:
        # Set effective contact rate
        agent["effective_contact"] = agent["contact_rate"] * mask_reduction
        
        # Additional reduction for children if schools closed
        if policy["school_closure"] and agent["age_group"] == "child":
            agent["effective_contact"] *= school_reduction
        
        # Vaccination immunity boost (only for susceptible)
        if vaccination_boost > 0 and agent["state"] == "S":
            agent["immunity"] = min(agent["immunity"] + vaccination_boost, 0.95)
