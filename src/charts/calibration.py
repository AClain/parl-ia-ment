import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import List
from models.LLMOutput import ConfidenceType
from metrics.llm.confidence import (
    _accuracy_in_bin,
    _confidence_in_bin,
    _samples_in_bin,
    compute_ece,
)
from models.Charts import Styles
from errors.WrongRunIdProvided import WrongRunIdProvided
from utils.database import prompt_run_from_run_id
from utils.helpers import save_chart


def plot_confidence_calibration_curve(
    run_ids: List[str] | str,
    confidence_type: ConfidenceType,
    num_of_bins: int = 10,
    plot_title: str = "Calibration curve",
    save_folder: str = "images/charts",
) -> None:
    """
    Plot the calibration graph for the prompt results associated
    to the run_ids provided.

    Parameters
    ----------
    run_ids: List[str] | str
        Either a list of run_ids or a single run_id.
    confidence_type: ConfidenceType
        The type of confidence measure.
    num_of_bins: int, default=10
        The number of bins following which the confidence intervals are built.
    plot_title: str, default="Calibration curve"
        Title of the plot.
    """
    run = None
    if isinstance(run_ids, str):
        run = prompt_run_from_run_id(run_ids)
        if run is None:
            raise WrongRunIdProvided()

    bin_boundaries = np.linspace(0, 1, num_of_bins + 1)
    top = bin_boundaries[1:]
    bot = bin_boundaries[:-1]

    ece, data = compute_ece(  # type: ignore
        run_ids, confidence_type, num_of_bins, with_data=True
    )

    # Build metrics
    confidences = []
    accuracies = []
    s_in_bin = []
    for bot, top in zip(bot, top):
        s_in_bin.append(len(_samples_in_bin(data, bot, top)))
        confidences.append(_confidence_in_bin(data, bot, top))
        accuracies.append(_accuracy_in_bin(data, bot, top))

    s_offset = np.array(s_in_bin) + 1e-10

    # Build color mapping
    blues = plt.cm.Blues  # type: ignore
    norm = mpl.colors.LogNorm(min(s_offset), max(s_offset))  # type: ignore

    bin_boundaries = np.linspace(0, 1, num_of_bins + 1)
    bin_centers = 0.5 * (bin_boundaries[:-1] + bin_boundaries[1:])

    with plt.style.context(Styles.SeabornMuted.value):
        if run is not None:
            title = f"{plot_title} for {run['name']}"
        else:
            title = f"{plot_title}"

        plt.figure(figsize=(6, 6))

        plt.bar(
            bin_centers,
            accuracies,
            color=blues(norm(s_in_bin)),
            width=np.diff(bin_boundaries),
            edgecolor="darkgray",
            align="center",
        )
        plt.plot([0, 1], [0, 1], linestyle="--", color="black", alpha=0.4)
        plt.text(
            0.2,
            0.8,
            f"ECE: {ece:.3f}",
            color=blues((max(s_in_bin) - min(s_in_bin)) / len(s_in_bin)),
            fontsize=20,
            fontweight="bold",
        )

        plt.xlabel("Confidence")
        plt.ylabel("Accuracy")
        plt.title(title)

        ax = plt.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()
