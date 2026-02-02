import numpy as np

def discretize_state(obs):
    """
    Convert continuous observation to discrete bins
    """
    infected, child_inf, adult_inf, hospital, econ = obs

    return (
        int(infected * 10),
        int(child_inf * 10),
        int(adult_inf * 10),
        int(hospital * 10)
    )
