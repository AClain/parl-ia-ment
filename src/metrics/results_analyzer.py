from tqdm import tqdm
from bson import ObjectId
from random import choice
from typing import Any, List, Dict
from collections import Counter
from pprint import pprint
from databases.connector import Connector
from models.ExportFormat import ExportFormat
from models.Result import QuestionResult, CustomRunResult

connector = Connector(ExportFormat.JSON)


class ResultAnalyzer:
    """
    Defines a result set for a given question batch ID.

    Attributes
    ----------
    batch_id: str
        A unique batch identifier.
    batch_themes: Dict[str, int]
        All the themes represented in the batch associated with the
        occurrences of each theme.
    question_results: List[QuestionResult]
        A list of question results describing how each LLM predicted the label for
        all the questions in the question batch.
    """


class ResultsAnalyzer:
    """
    Defines a result pool for a given question batch ID.

    Attributes
    ----------
    batch_id: str
        A unique batch identifier.
    batch_themes: Dict[str, int]
        All the themes represented in the batch associated with the
        occurrences of each theme.
    question_results: List[QuestionResult]
        A list of question results describing how each LLM predicted the label for
        all the questions in the question batch.
    """

    def __init__(self, run_ids: List[str]) -> None:
        self.run_ids = run_ids
        self.runs = self.retrieve_prompt_runs()
        self.question_results = self.retrieve_question_results()

    def retrieve_prompt_runs(self) -> List[Dict[str, Any]] | Dict[str, Any]:
        if type(self.run_ids) is str:
            prompt_runs = connector.client.get_prompt_run(
                {"_id": ObjectId(self.run_ids)}
            )
            batch_ids = prompt_runs["batch_id"]  # type: ignore
        else:
            prompt_runs = connector.client.get_prompt_runs(
                {"_id": {"$in": [ObjectId(run_id) for run_id in self.run_ids]}}
            )
            prompt_runs = list(prompt_runs)

            batch_ids = list(set(prompt_run["batch_id"] for prompt_run in prompt_runs))

        if len(batch_ids) > 1 and type(self.run_ids) is list:
            raise ValueError("Bach ID must be the same across all prompt runs.")

        if type(self.run_ids) is list:
            self.batch = connector.client.get_batch({"_id": ObjectId(batch_ids[0])})
        else:
            self.batch = connector.client.get_batch({"_id": ObjectId(batch_ids)})  # type: ignore

        return prompt_runs

    def retrieve_question_results(self) -> List[QuestionResult]:
        """
        Retrieve all question results as predicted by the LLMs in the prompt runs.

        Returns
        -------
        List[QuestionResult]
            A list of question results describing how each LLM predicted the label for
            all the questions in the question batch.
        """

        if type(self.run_ids) is str:
            prompt_results = connector.client.get_prompt_results(
                {"run_id": str(self.runs["_id"])}  # type: ignore
            )
            prompt_results = list(prompt_results)
            question_ids = list(set([x["question_id"] for x in prompt_results]))
        else:
            prompt_results = connector.client.get_prompt_results(
                {"run_id": {"$in": [str(run["_id"]) for run in self.runs]}}
            )
            prompt_results = list(prompt_results)

            question_ids = list(set([x["question_id"] for x in prompt_results]))

        questions = connector.client.get_questions({"id": {"$in": question_ids}})
        questions = list(questions)

        question_results = [
            QuestionResult(
                **{
                    "question_id": x["id"],
                    "question_text": x["question_text"],
                    "database_label": x["theme"],
                    "results": [],
                }
            )
            for x in questions
        ]

        print("Retrieving all question results...")
        for question_result in tqdm(question_results):
            for result in prompt_results:
                if result["question_id"] == question_result.question_id:
                    if type(self.run_ids) is str:
                        current_run = self.runs
                    else:
                        current_run = [
                            run
                            for run in self.runs
                            if str(ObjectId(run["_id"])) == result["run_id"]
                        ][0]
                    question_result.results.append(
                        CustomRunResult(
                            **{
                                "prompt_id": result["prompt_id"],
                                "run_id": result["run_id"],
                                "predicted_label": result["final_answer"].strip(),
                                "gold_label": result["gold_label"],
                                "prompt": current_run["description"],
                            }
                        )
                    )

        return question_results

    def filter_at_least_one_disagrees(self) -> List[QuestionResult]:
        """
        Filter question results for which at least one LLM disagrees with the others.

        Returns
        -------
        List[QuestionResult]
            A list of filtered question results.
        """
        disagrements = []

        for question_result in tqdm(self.question_results):
            all_predicted_labels = [x.predicted_label for x in question_result.results]

            if len(set(all_predicted_labels)) > 1:
                disagrements.append(question_result)

        return disagrements

    def filter_all_agree(self) -> List[QuestionResult]:
        """
        Filter question results for which all LLMs agree on the predicted labels.

        Returns
        -------
        List[QuestionResult]
            A list of filtered question results.
        """
        agreements = []

        for question_result in tqdm(self.question_results):
            all_predicted_labels = [x.predicted_label for x in question_result.results]

            if len(set(all_predicted_labels)) == 1:
                agreements.append(question_result)

        return agreements

    def filter_at_least_one_is_wrong(self) -> List[QuestionResult]:
        """
        Filter question results for which at least one of the predicted label is wrong.

        Returns
        -------
        List[QuestionResult]
            A list of filtered question results.
        """
        differences = []

        for question_result in tqdm(self.question_results):
            association_list = [
                x.gold_label == x.predicted_label for x in question_result.results
            ]
            if not all(association_list):
                differences.append(question_result)

        return differences

    def filter_all_are_correct(self) -> List[QuestionResult]:
        """
        Filter question results for which all the predicted labels are correct.

        Returns
        -------
        List[QuestionResult]
            A list of filtered question results.
        """
        matches = []

        for question_result in tqdm(self.question_results):
            association_list = [
                x.gold_label == x.predicted_label for x in question_result.results
            ]

            if all(association_list):
                matches.append(question_result)

        return matches

    def filter_all_are_wrong(self) -> List[QuestionResult]:
        """
        Filter question results for which all the predicted labels are wrong.

        Returns
        -------
        List[QuestionResult]
            A list of filtered question results.
        """
        matches = []

        for question_result in tqdm(self.question_results):
            association_list = [
                x.gold_label != x.predicted_label for x in question_result.results
            ]

            if all(association_list):
                matches.append(question_result)

        return matches

    def filter_all_are_wrong_and_all_agree(self) -> List[QuestionResult]:
        """
        Filter question results for which all the predicted labels are both wrong
        but all annotators agree.

        Returns
        -------
        List[QuestionResult]
            A list of filtered question results.
        """
        all_agree = self.filter_all_agree()
        all_wrong = self.filter_all_are_wrong()
        merge = []
        for ag in all_agree:
            for wr in all_wrong:
                if ag == wr:
                    merge.append(ag)

        return merge

    @classmethod
    def themes_agreement_ratio_for_question_result(
        cls,
        question_result: QuestionResult,
    ) -> Dict[str, float]:
        """
        Compute the ratio agreement for a given question result.

        Parameters
        ----------
        question_result: QuestionResult
            A question result.
        """
        themes_agreement_ratio = {}

        predicted_themes = Counter(
            [x.predicted_label for x in question_result.results]
        ).most_common()
        predicted_themes = list(predicted_themes)

        for predicted_theme, occurrences in predicted_themes:
            themes_agreement_ratio[predicted_theme] = occurrences / len(
                question_result.results
            )

        return themes_agreement_ratio

    @classmethod
    def compute_confidence_for_question(
        cls, themes_agreement_ratio: Dict[str, float], gold_label: str
    ):
        tracker = {"predicted_label": "", "confidence": 0}
        results = []

        for k, v in themes_agreement_ratio.items():
            if v == tracker["confidence"]:
                results.append({"predicted_label": k, "confidence": v})
            if v > tracker["confidence"]:
                results = []
                tracker["confidence"] = v
                tracker["predicted_label"] = k
                results.append({"predicted_label": k, "confidence": v})

        return {
            "most_predicted_label": choice(results)["predicted_label"],
            "gold_label": gold_label,
            "is_prediction_correct": int(
                choice(results)["predicted_label"] == gold_label
            ),
            "confidence": choice(results)["confidence"],
        }


def compute_results_analysis(run_ids: List[str]):
    analyzer = ResultsAnalyzer(run_ids)

    analysis = {
        "All agree": len(analyzer.filter_all_agree()),
        "At least one disagrees": len(analyzer.filter_at_least_one_disagrees()),
        "At least one is wrong": len(analyzer.filter_at_least_one_is_wrong()),
        "All are correct": len(analyzer.filter_all_are_correct()),
        "All are wrong": len(analyzer.filter_all_are_wrong()),
    }

    return analysis


def _find_ids_for_label(
    question_results: List[QuestionResult],
    label: str,
    predicted_label: bool,
    gold_label: bool,
) -> List[int]:
    """
    Filter question results that match the provided labels.

    Parameters
    ----------
    question_results: List[QuestionResult]
        The unfiletered list of question results.
    label: str
        The label to search for.
    predicted_label: bool
        Defines whether the label pattern should filter only predicted labels.
    gold_label: bool
        Defines whether the label pattern should filter only gold labels.

    Returns
    -------
    List[int]
        The list of question results IDs corresponding to the filters provided.
    """
    if predicted_label and gold_label:
        matched_ids = []
        for i, qr in enumerate(question_results):
            for res in qr.results:
                if res.predicted_label == label and res.gold_label == label:
                    matched_ids.append(i)
        return matched_ids
    if predicted_label:
        matched_ids = []
        for i, qr in enumerate(question_results):
            for res in qr.results:
                if res.predicted_label == label:
                    matched_ids.append(i)
        return matched_ids
    if gold_label:
        matched_ids = []
        for i, qr in enumerate(question_results):
            for res in qr.results:
                if res.gold_label == label:
                    matched_ids.append(i)
        return matched_ids

    return [i for i, _ in enumerate(question_results)]


def visualize_results(
    question_results: List[QuestionResult],
    id: int,
    predicted_label: str | None = None,
    gold_label: str | None = None,
) -> None:
    """
    Visualize results for close reading.

    Parameters
    ----------
    question_result: QuestionResult
        A given question result.
    predicted_label: str | None, default=None
        Filter only questions predicted as the provided label.
    gold_label: str | None, default=None
        Filter only questions that has the provided label as ground-truth.
    id: int
        ID of the question result in the final question result list.
    """

    if gold_label and predicted_label:
        list_ids = _find_ids_for_label(
            question_results,
            label=predicted_label,
            predicted_label=True,
            gold_label=True,
        )
        pprint(question_results[list_ids[id]].question_id)
        pprint(question_results[list_ids[id]].question_text)
        pprint(
            [
                {"predicted": r.predicted_label, "gold": r.gold_label}
                for r in question_results[list_ids[id]].results
                if r.predicted_label == predicted_label and r.gold_label == gold_label
            ]
        )

    if predicted_label:
        list_ids = _find_ids_for_label(
            question_results,
            label=predicted_label,
            predicted_label=True,
            gold_label=False,
        )
        pprint(question_results[list_ids[id]].question_id)
        pprint(question_results[list_ids[id]].question_text)
        pprint(
            [
                {"predicted": r.predicted_label, "gold": r.gold_label}
                for r in question_results[list_ids[id]].results
                if r.predicted_label == predicted_label
            ]
        )
        return

    if gold_label:
        list_ids = _find_ids_for_label(
            question_results,
            label=gold_label,
            predicted_label=False,
            gold_label=True,
        )
        pprint(question_results[list_ids[id]].question_id)
        pprint(question_results[list_ids[id]].question_text)
        pprint(
            [
                {"predicted": r.predicted_label, "gold": r.gold_label}
                for r in question_results[list_ids[id]].results
                if r.gold_label == gold_label
            ]
        )
        return

    pprint(question_results[id].question_id)
    pprint(question_results[id].question_text)
    pprint(
        [
            {"predicted": r.predicted_label, "gold": r.gold_label}
            for r in question_results[id].results
        ]
    )
