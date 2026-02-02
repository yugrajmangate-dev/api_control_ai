from env.population import generate_population
from env.policies import apply_policy
from env.seir import seed_infection, update_seir
from simulation.metrics import init_metrics, record_metrics

DAYS = 60
POP_SIZE = 1000

population = generate_population(POP_SIZE)
seed_infection(population, initial_infected=10)

metrics = init_metrics()

policy = {
    "mask_mandate": False,
    "school_closure": False,
    "vaccination": True
}

for day in range(DAYS):
    for agent in population:
        apply_policy(agent, policy)

    record_metrics(metrics, population)
    update_seir(population)

print("Simulation finished.")

from visualization.plots import plot_seir

plot_seir(metrics)

