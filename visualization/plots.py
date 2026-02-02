import matplotlib.pyplot as plt


def plot_seir(metrics):
    days = range(len(metrics["overall"]["S"]))

    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # ---- OVERALL ----
    axes[0].plot(days, metrics["overall"]["S"], label="S")
    axes[0].plot(days, metrics["overall"]["E"], label="E")
    axes[0].plot(days, metrics["overall"]["I"], label="I")
    axes[0].plot(days, metrics["overall"]["R"], label="R")
    axes[0].set_title("Overall SEIR")
    axes[0].legend()

    # ---- CHILDREN ----
    axes[1].plot(days, metrics["children"]["S"], label="S")
    axes[1].plot(days, metrics["children"]["E"], label="E")
    axes[1].plot(days, metrics["children"]["I"], label="I")
    axes[1].plot(days, metrics["children"]["R"], label="R")
    axes[1].set_title("Children SEIR")
    axes[1].legend()

    # ---- ADULTS ----
    axes[2].plot(days, metrics["adults"]["S"], label="S")
    axes[2].plot(days, metrics["adults"]["E"], label="E")
    axes[2].plot(days, metrics["adults"]["I"], label="I")
    axes[2].plot(days, metrics["adults"]["R"], label="R")
    axes[2].set_title("Adults SEIR")
    axes[2].legend()

    plt.xlabel("Days")
    plt.tight_layout()
    plt.show()
