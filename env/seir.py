import numpy as np

# Virus parameters (set at runtime)
BASE_BETA = 0.3
INCUBATION_DAYS = 5
INFECTIOUS_DAYS = 7
CURRENT_VIRUS_CONFIG = {}


def set_virus_params(config):
    global BASE_BETA, INCUBATION_DAYS, INFECTIOUS_DAYS, CURRENT_VIRUS_CONFIG

    BASE_BETA = config["base_beta"]
    INCUBATION_DAYS = config["incubation_days"]
    INFECTIOUS_DAYS = config["infectious_days"]
    CURRENT_VIRUS_CONFIG = config.copy()


def get_current_virus_config():
    """Get current virus configuration"""
    global CURRENT_VIRUS_CONFIG
    return CURRENT_VIRUS_CONFIG.copy()


# ------------------ SEED INITIAL INFECTION ------------------
def seed_infection(population, initial_infected=5):
    if len(population) == 0:
        return

    n = min(initial_infected, len(population))

    infected_agents = np.random.choice(
        population, n, replace=False
    )

    for agent in infected_agents:
        agent["state"] = "I"
        agent["days_in_state"] = 0


# ------------------ INFECTION PROBABILITY ------------------
def infection_probability(sus_agent):
    beta = BASE_BETA
    contact = sus_agent.get("effective_contact", sus_agent["contact_rate"])

    immunity = sus_agent["immunity"]

    return beta * contact * (1 - immunity)


# ------------------ DAILY SEIR UPDATE WITH MUTATION SUPPORT ------------------
def update_seir(population, avg_contacts_per_infected=None, mutation_tracker=None, current_day=0):
    """
    Update SEIR states with optional mutation checking
    
    Args:
        population: List of agents
        avg_contacts_per_infected: Average contacts per infected individual (auto-calculated if None)
        mutation_tracker: MutationTracker object (optional)
        current_day: Current simulation day (for mutation tracking)
    """
    # Calculate age-weighted contact rate if not provided
    if avg_contacts_per_infected is None:
        child_count = sum(1 for a in population if a.get("age_group") == "child")
        adult_count = len(population) - child_count
        # Children have 30% more contacts than adults (WHO POLYMOD study)
        child_contacts = 10.4  # Average for children aged 5-17
        adult_contacts = 8.0   # Average for adults 18-65
        avg_contacts_per_infected = (
            (child_count * child_contacts + adult_count * adult_contacts) / len(population)
            if len(population) > 0 else 8.0
        )
    from env.mutation import check_mutation_trigger, apply_mutation, select_mutation_severity
    
    # Vectorized filtering - much faster than list comprehensions
    pop_array = np.array(population)
    states = np.array([a["state"] for a in population])
    
    infectious_idx = np.where(states == "I")[0]
    susceptible_idx = np.where(states == "S")[0]
    
    infectious_agents = [population[i] for i in infectious_idx]
    susceptible_agents = [population[i] for i in susceptible_idx]
    
    new_exposed = []

    # ---- CHECK FOR MUTATION ----
    if mutation_tracker is not None and current_day > 0:
        # Check cooldown period (biological constraint)
        days_since_last = current_day - mutation_tracker.last_mutation_day
        if days_since_last >= 15:  # Minimum 15 days between mutations
            should_mutate, trigger_reason = check_mutation_trigger(
                population, current_day, 
                previous_mutations=mutation_tracker.mutation_count
            )
        else:
            should_mutate = False
            trigger_reason = None
        
        if should_mutate:
            # Get current infection rate for severity determination
            infection_rate = len(infectious_agents) / len(population) if len(population) > 0 else 0
            severity = select_mutation_severity(infection_rate, current_day)
            
            # Get old parameters
            old_config = get_current_virus_config()
            
            # Apply mutation
            new_config = apply_mutation(old_config, mutation_severity=severity)
            
            # Update global virus parameters
            set_virus_params(new_config)
            
            # Log mutation event
            mutation_event = mutation_tracker.log_mutation(
                day=current_day,
                trigger_reason=trigger_reason,
                old_params=old_config,
                new_params=new_config
            )
            mutation_tracker.last_mutation_day = current_day

    # ---- SPREAD ONLY IF SUSCEPTIBLE EXIST ----
    if len(susceptible_agents) > 0 and len(infectious_agents) > 0:
        # Batch process infections - much faster
        num_contacts = int(min(avg_contacts_per_infected * len(infectious_agents), len(susceptible_agents)))
        
        if num_contacts > 0:
            contacted = np.random.choice(
                susceptible_agents,
                size=min(num_contacts, len(susceptible_agents)),
                replace=True  # Allow reinfection attempts for efficiency
            )
            
            # Vectorized infection probability check
            infection_probs = np.array([infection_probability(sus) for sus in contacted])
            infected_mask = np.random.rand(len(contacted)) < infection_probs
            
            # Track unique new exposures
            exposed_set = set()
            for i, sus in enumerate(contacted):
                if infected_mask[i] and id(sus) not in exposed_set:
                    new_exposed.append(sus)
                    exposed_set.add(id(sus))
        
        # Update newly exposed
        for agent in new_exposed:
            agent["state"] = "E"
            agent["days_in_state"] = 0

    # ---- STATE TRANSITIONS (VECTORIZED) ----
    # Update days for all agents at once
    for agent in population:
        agent["days_in_state"] += 1
    
    # Batch state transitions
    for agent in population:
        state = agent["state"]
        days = agent["days_in_state"]
        
        if state == "E" and days >= INCUBATION_DAYS:
            agent["state"] = "I"
            agent["days_in_state"] = 0
        elif state == "I" and days >= INFECTIOUS_DAYS:
            agent["state"] = "R"
            agent["days_in_state"] = 0
