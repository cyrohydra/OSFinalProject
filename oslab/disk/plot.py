"""Head-movement plot for disk scheduling results."""


def plot_head_movement(results, filename="disk_movement.png"):
    """One subplot per algorithm: head position vs. step."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(len(results), 1, figsize=(8, 2.2 * len(results)), sharex=False)
    for ax, r in zip(axes, results):
        ax.plot(r["path"], range(len(r["path"])), marker="o")
        ax.invert_yaxis()
        ax.set_title(f'{r["algorithm"]}  (total = {r["total"]})', fontsize=10)
        ax.set_xlabel("cylinder")
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    return filename
