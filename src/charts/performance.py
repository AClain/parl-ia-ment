import seaborn as sns
from typing import List
import matplotlib.pyplot as plt
from utils.database import prompt_run_from_run_id
from errors.WrongRunIdProvided import WrongRunIdProvided
from metrics.llm.performance import (
    compute_precision,
    compute_recall,
    compute_f1_score,
    compute_precision_to_df_from_run_ids,
    compute_recall_to_df_from_run_ids,
    compute_fscore_to_df_from_run_ids,
    compute_support_count,
)
from models.Charts import Styles
from utils.helpers import save_chart, remove_frame
from utils.helpers import get_unique_dicts_by_key
from models.Metrics import SupportComputed
from utils.dataframes import highlight_heatmap_highest_value
from models.Metrics import AverageMetricEnum
from metrics.llm.performance import (
    compute_average_precision,
    compute_average_recall,
    compute_average_f1_score,
)
from metrics.results_analyzer import compute_results_analysis


def plot_precision(run_id: str, save_folder: str = "images/charts") -> None:
    """
    Plot the precision scores for each theme in a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided(run_id)

    computed_precisions = compute_precision(run_id)

    themes = computed_precisions["themes"]
    precisions = computed_precisions["precisions"]

    with plt.style.context(Styles.SeabornMuted.value):
        title = f"Precision per Theme ({run['name']})"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.barh(themes, precisions, zorder=2)

        xticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        for bar, score in zip(bars, precisions):
            plt.text(
                bar.get_width() - 0.055,
                bar.get_y() + bar.get_height() / 2.0,
                f"{bar.get_width():.2f}",
                va="center",
                ha="left",
                fontsize=10,
                color="white",
            )

        plt.xlabel("Precision")
        plt.ylabel("Themes")

        for tick in xticks:
            plt.axvline(x=tick, color="lightgrey", linewidth=1, zorder=1)
        plt.xticks(ticks=xticks)

        plt.title(title, pad=20)
        plt.gca().set_facecolor((1.0, 1.0, 1.0))
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_average_precision(
    run_ids: List[str],
    average: AverageMetricEnum = AverageMetricEnum.Weighted,
    experiment_labels: List[str] | None = None,
    save_folder: str = "images/charts",
) -> None:
    computed_average_precisions = compute_average_precision(run_ids, average)
    number_of_results = len(computed_average_precisions["run_names"])

    if experiment_labels is None:
        experiment_labels = computed_average_precisions["run_names"]

    with plt.style.context(Styles.SeabornMuted.value):
        title = f"Average ({average.value}) precision per run"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.bar(
            experiment_labels,
            computed_average_precisions["precisions"],
            zorder=2,
        )

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height(),
                f"{bar.get_height():.2f}",
                ha="center",
                va="bottom",
                fontsize="small" if number_of_results >= 15 else "medium",
            )

        yticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Average precisions")
        plt.yticks(yticks)

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_precision_heatmap(
    run_ids: List[str],
    highlight: bool = True,
    save_folder: str = "images/charts",
    title: str = "Precision heatmap for each theme in specified runs",
) -> None:
    """
    Plot the precision scores for each theme in specified prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        The list of unique identifiers for the prompt runs to be analyzed.
    """
    precisions_df = compute_precision_to_df_from_run_ids(run_ids)

    with plt.style.context(Styles.SeabornMuted.value):
        plt.figure(figsize=(14, 8))
        ax = sns.heatmap(
            precisions_df,
            annot=True,
            cmap="Blues",
            linewidths=0.5,
            vmin=0.0,
            vmax=1.0,
            fmt=".2f",
        )

        if highlight:
            highlight_heatmap_highest_value(precisions_df, ax.texts)

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Themes")

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_recall(run_id: str, save_folder: str = "images/charts") -> None:
    """
    Plot the recall scores for each theme in a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided()

    computed_recalls = compute_recall(run_id)

    themes = computed_recalls["themes"]
    recalls = computed_recalls["recalls"]

    with plt.style.context(Styles.SeabornMuted.value):
        title = f"Recall per Theme ({run['name']})"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.barh(themes, recalls, zorder=2)

        xticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        for bar in bars:
            plt.text(
                bar.get_width() - 0.055,
                bar.get_y() + bar.get_height() / 2.0,
                f"{bar.get_width():.2f}",
                va="center",
                ha="left",
                fontsize=10,
                color="white",
            )

        plt.xlabel("Recall")
        plt.ylabel("Themes")

        for tick in xticks:
            plt.axvline(x=tick, color="lightgrey", linewidth=1, zorder=1)
        plt.xticks(ticks=xticks)

        plt.title(title, pad=20)
        plt.gca().set_facecolor((1.0, 1.0, 1.0))
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_average_recall(
    run_ids: List[str],
    average: AverageMetricEnum = AverageMetricEnum.Weighted,
    experiment_labels: List[str] | None = None,
    save_folder: str = "images/charts",
) -> None:
    computed_average_recalls = compute_average_recall(run_ids, average)
    number_of_results = len(computed_average_recalls["run_names"])

    if experiment_labels is None:
        experiment_labels = computed_average_recalls["run_names"]

    with plt.style.context(Styles.SeabornMuted.value):
        title = f"Average ({average.value}) recall per run"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.bar(
            experiment_labels,
            computed_average_recalls["recalls"],
            zorder=2,
        )

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height(),
                f"{bar.get_height():.2f}",
                ha="center",
                va="bottom",
                fontsize="small" if number_of_results >= 15 else "medium",
            )

        yticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Average recalls")
        plt.yticks(yticks)

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_recall_heatmap(
    run_ids: List[str],
    highlight: bool = True,
    save_folder: str = "images/charts",
    title: str = "Recall heatmap for each theme in specified runs",
) -> None:
    """
    Plot the recall scores for each theme in specified prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        The list of unique identifiers for the prompt runs to be analyzed.
    """
    recalls_df = compute_recall_to_df_from_run_ids(run_ids)

    with plt.style.context(Styles.SeabornMuted.value):
        plt.figure(figsize=(14, 8))
        ax = sns.heatmap(
            recalls_df,
            annot=True,
            cmap="Greens",
            linewidths=0.5,
            vmin=0.0,
            vmax=1.0,
        )

        if highlight:
            highlight_heatmap_highest_value(recalls_df, ax.texts)

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Themes")

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_f1_score(run_id: str, save_folder: str = "images/charts") -> None:
    """
    Plot the f1 scores for each theme in a given prompt run.

    Parameters
    ----------
    run_id : str
        The unique identifier for the prompt run to be analyzed.
    """
    run = prompt_run_from_run_id(run_id)
    if run is None:
        raise WrongRunIdProvided()

    computed_fscores = compute_f1_score(run_id)

    themes = computed_fscores["themes"]
    fscores = computed_fscores["fscores"]

    with plt.style.context(Styles.SeabornMuted.value):
        title = f"F1-score per Theme ({run['name']})"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.barh(themes, fscores, zorder=2)

        xticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

        for bar in bars:
            plt.text(
                bar.get_width() - 0.055,
                bar.get_y() + bar.get_height() / 2.0,
                f"{bar.get_width():.2f}",
                va="center",
                ha="left",
                fontsize=10,
                color="white",
            )

        plt.xlabel("F1-score")
        plt.ylabel("Themes")

        for tick in xticks:
            plt.axvline(x=tick, color="lightgrey", linewidth=1, zorder=1)
        plt.xticks(ticks=xticks)

        plt.title(title, pad=20)
        plt.gca().set_facecolor((1.0, 1.0, 1.0))
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_average_f1_score(
    run_ids: List[str],
    average: AverageMetricEnum = AverageMetricEnum.Weighted,
    experiment_labels: List[str] | None = None,
    save_folder: str = "images/charts",
) -> None:
    computed_average_fscores = compute_average_f1_score(run_ids, average)
    number_of_results = len(computed_average_fscores["run_names"])

    if experiment_labels is None:
        experiment_labels = computed_average_fscores["run_names"]

    with plt.style.context(Styles.SeabornMuted.value):
        title = f"Average ({average.value}) F1 scores per run"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.bar(
            experiment_labels,
            computed_average_fscores["fscores"],
            zorder=2,
        )

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height(),
                f"{bar.get_height():.2f}",
                ha="center",
                va="bottom",
                fontsize="small" if number_of_results >= 15 else "medium",
            )

        yticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        for tick in yticks:
            plt.axhline(y=tick, color="lightgrey", linewidth=1, zorder=1)

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Average F1 scores")
        plt.yticks(yticks)

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_f1_score_heatmap(
    run_ids: List[str],
    highlight: bool = True,
    save_folder: str = "images/charts",
    title: str = "F1 Score heatmap for each theme in specified runs",
) -> None:
    """
    Plot the f1 scores for each theme in specified prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        The list of unique identifiers for the prompt runs to be analyzed.
    """
    fscores_df = compute_fscore_to_df_from_run_ids(run_ids)

    with plt.style.context(Styles.SeabornMuted.value):
        palette = sns.color_palette("viridis", as_cmap=True).reversed()

        plt.figure(figsize=(14, 8))
        ax = sns.heatmap(
            fscores_df,
            annot=True,
            cmap=palette,
            linewidths=0.5,
            vmin=0.0,
            vmax=1.0,
        )

        if highlight:
            highlight_heatmap_highest_value(fscores_df, ax.texts)

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Themes")

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_support_count(
    support_count: SupportComputed, save_folder: str = "images/charts"
) -> None:
    """
    Plot the support count for the specified themes and save the chart.

    Parameters
    ----------
    support_count : SupportComputed
        A dictionary containing the support counts and themes to be plotted. It should have
        two keys: "support_count", a list of counts, and "themes", a list of corresponding themes.
    save_folder : str, default="images/charts"
        The folder where the generated chart will be saved.
    """
    paired_data = list(zip(support_count["support_count"], support_count["themes"]))

    sorted_paired_data = sorted(paired_data, key=lambda x: x[0])

    sorted_support_count, sorted_themes = zip(*sorted_paired_data)

    support_count["support_count"] = list(sorted_support_count)
    support_count["themes"] = list(sorted_themes)

    with plt.style.context(Styles.SeabornMuted.value):
        title = "Support count for specified runs"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.barh(
            support_count["themes"], support_count["support_count"], zorder=2
        )

        plt.ylabel("Themes")
        plt.xlabel("Support count")

        ax = plt.gca()
        xticks = ax.get_xticks()
        for tick in xticks:
            plt.axvline(x=tick, color="lightgrey", linewidth=1, zorder=1)

        for bar in bars:
            width = bar.get_width()
            plt.text(
                width - 0.5,
                bar.get_y() + bar.get_height() / 2,
                str(width),
                ha="right",
                va="center",
                color="white",
                fontsize=10,
            )

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()


def plot_support_counts(run_ids: List[str], save_folder: str = "images/charts"):
    """
    Plot the support counts for each batch of prompt runs.

    Parameters
    ----------
    run_ids : List[str]
        A list of unique identifiers for the prompt runs to be analyzed.
    save_folder : str, default="images/charts"
        The folder where the generated support count plots will be saved.

    Raises:
    ------
    WrongRunIdProvided
        If any of the provided run_ids is invalid or does not match a prompt run.
    """
    runs = [prompt_run_from_run_id(run_id) for run_id in run_ids]
    if len(runs) < len(run_ids):
        raise WrongRunIdProvided()

    support_counts = {run_id: {} for run_id in run_ids}
    for run_id in run_ids:
        support_count = compute_support_count(run_id)
        support_counts[run_id] = support_count

    unique_batches_support_count = get_unique_dicts_by_key(
        support_counts.values(), "batch_id"
    )

    for unique_batch_support_count in unique_batches_support_count:
        plot_support_count(unique_batch_support_count, save_folder)


def plot_results_analysis(run_ids: List[str], save_folder: str = "images/charts"):
    analyzer = compute_results_analysis(run_ids)

    with plt.style.context(Styles.SeabornMuted.value):
        title = "Analysis"

        plt.figure(figsize=(10, 6))
        remove_frame(plt)

        bars = plt.bar(
            analyzer.keys(),
            analyzer.values(),
            zorder=2,
        )

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() - 75,
                f"{bar.get_height()}",
                ha="center",
                va="bottom",
                color="white",
            )

        yticks = [0, 250, 500, 750, 1000, 1250, 1500]
        for tick in yticks:
            plt.axhline(y=tick, color="lightgrey", linewidth=1, zorder=1)

        plt.ylabel("Runs")
        plt.xticks(
            rotation=50,
            ha="right",
            rotation_mode="anchor",
        )
        plt.xlabel("Analysis")
        plt.yticks(yticks)

        plt.gca().set_facecolor((1.0, 1.0, 1.0))

        plt.title(title, pad=20)
        plt.tight_layout()

        save_chart(plt, title, save_folder)

        plt.show()
