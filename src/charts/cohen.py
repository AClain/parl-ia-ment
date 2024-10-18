import pandas as pd
import seaborn as sns
from typing import List, Optional
import matplotlib.pyplot as plt
from utils.helpers import save_chart
from metrics.agreement.cohen import compute_cohen_kappa


def plot_cohen_kappa(
    run_ids: List[str], save_folder: str = "images/charts", alias: Optional[str] = None
) -> None:
    cohen_kappa_scores = compute_cohen_kappa(run_ids)

    strategies = sorted(
        set(
            [pair[0] for pair in cohen_kappa_scores.keys()]
            + [pair[1] for pair in cohen_kappa_scores.keys()]
        )
    )
    matrix = pd.DataFrame(index=strategies, columns=strategies)

    for (strategy_1, strategy_2), value in cohen_kappa_scores.items():
        matrix.loc[strategy_1, strategy_2] = value
        matrix.loc[strategy_2, strategy_1] = value

    matrix = matrix.astype(float)

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        matrix,
        annot=True,
        cmap="coolwarm",
        cbar=True,
        square=True,
        fmt=".2f",
        linewidths=0.5,
        vmin=0.0,
        vmax=1.0,
    )
    plt.title("Pair wise Cohen's Kappa")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    if alias is not None:
        save_chart(plt, f"Cohen's Kappa Heatmap ({alias})", save_folder)
    else:
        save_chart(plt, "Cohen's Kappa Heatmap", save_folder)

    plt.show()
