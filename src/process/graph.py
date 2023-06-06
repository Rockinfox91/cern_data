import matplotlib.pyplot as plt


def get_easy_time_graph(df, coly):
    if isinstance(coly, str):
        coly = [coly]

    num_plots = len(coly)
    fig, axes = plt.subplots(2, 2, figsize=(10, 10), squeeze=False)
    axes = axes.flatten()

    for i in range(num_plots):
        ax = axes[i]
        ax.plot(df["time"], df[coly[i]])
        ax.set_xlabel("time")
        ax.set_ylabel(coly[i])

    if num_plots == 1:
        fig.suptitle(f"Graphe de {coly[0]} en fonction du temps")
    else:
        fig.suptitle("4 graphes")
        for i, col in enumerate(coly):
            axes[i].set_title(col)

    plt.tight_layout()
    plt.show()