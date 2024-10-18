import itertools
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, TypedDict
from scipy.stats import kruskal, mannwhitneyu, wilcoxon, ks_2samp
from models.Prompt import PromptRun
from metrics.llm.performance import get_metric
from utils.database import prompt_run_from_run_id


class RunIds(TypedDict):
    id: str
    score: str

class ResultMetrics(TypedDict):
    themes: List[str]
    metrics: List[float]

def plot_distribution(data: List[float], metric: str) -> None: 
    plt.hist(data)
    plt.title('Distribution of metric ' + metric)
    plt.xlabel(metric)
    plt.show()

def get_tests_metrics_dict(run_ids: RunIds, metric: str) -> ResultMetrics: 
    all_metrics = {}
    for run_id in run_ids:
        prompt_run = prompt_run_from_run_id(run_id)
        prompt = PromptRun(**prompt_run)
        matrix_data = get_metric(run_id, metric)
        all_metrics[prompt.description] = matrix_data['metrics']
    return all_metrics

def do_test(
    all_scores: dict[str, List[float]],
    name: str,
    p_threshold: float
) -> pd.DataFrame:
    results = []
    tests = list(all_scores.keys())
    for compared1, compared2 in itertools.combinations(tests, 2):
        p = 0.0
        if (name == "mannwhitney"):
            _, p = mannwhitneyu(all_scores[compared1], all_scores[compared2])
        elif (name == "wilcoxon"):
            _, p = wilcoxon(all_scores[compared1], all_scores[compared2])
        elif (name == "ks"):
            _, p = ks_2samp(all_scores[compared1], all_scores[compared2])
        diff = ""
        if (p < p_threshold):
            diff = "significative"
        results.append((compared1, compared2, p, diff))

    return pd.DataFrame(results, columns=['prompt1', 'prompt2', 'p-value', ""])
    
def mannwhitney_test(all_scores: dict[str, List[float]]) -> pd.DataFrame: 
    return do_test(all_scores, "mannwhitney")

def wilcoxon_test(all_scores: dict[str, List[float]]) -> pd.DataFrame: 
    return do_test(all_scores, "wilcoxon")

def kruskal_test(all_scores: dict[str, List[float]]) -> float:
    params = [scores for scores in all_scores.values()]
    _, p = kruskal(*params)
    return p

def kolmogorov_smirnov(all_scores: dict[str, List[float]]):
    return do_test(all_scores, "ks")
