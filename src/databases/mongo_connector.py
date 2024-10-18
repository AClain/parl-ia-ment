import os
import logging
from bson import ObjectId
from models.Batch import Batch
from models.Theme import Theme
from dotenv import load_dotenv
from pymongo.cursor import Cursor
from models.Question import Question
from pymongo.results import InsertOneResult
from utils.helpers import flatten_list
from typing import Any, Dict, List, Optional
from pymongo.command_cursor import CommandCursor
from models.Prompt import Prompt, PromptResult, PromptRun
from pymongo import MongoClient, ReturnDocument, ASCENDING, collation

load_dotenv()
french_collation = collation.Collation(locale="fr", strength=1)


class Mongo:
    """
    MongoDB connection wrapper and helper functions.
    """

    def __init__(self) -> None:
        self.MONGO_USER = os.getenv("MONGODB_ADMIN_USER")
        self.MONGO_PASSWORD = os.getenv("MONGODB_ADMIN_PASSWORD")
        self.MONGO_HOST = os.getenv("MONGO_DOMAIN_NAME")
        self.client = MongoClient(
            f"mongodb://{self.MONGO_USER}:"
            f"{self.MONGO_PASSWORD}@{self.MONGO_HOST}"
            "/?authSource=admin"
        )

        self.themes_collection = self.client["themes"]["Themes"]
        self.questions_collection = self.client["question_data"]["Question"]
        self.prompts_collection = self.client["prompts"]["Prompts"]
        self.prompt_runs_collection = self.client["prompts"]["PromptRuns"]
        self.prompt_results_collection = self.client["prompts"]["PromptResults"]
        self.batches_collection = self.client["batches"]["Batches"]
        try:
            self.client.admin.command("ping")
            logging.debug("Connexion réussie à MongoDB.")
        except Exception as e:
            logging.error(f"Erreur de connexion à MongoDB : {e}.")

    def upsert_theme(self, theme: Theme) -> Theme:
        """
        Insert or update a theme in the database.

        Parameters
        ----------
        theme : Theme
            The theme to insert or update.

        Returns
        -------
        Theme
            The updated or inserted theme.
        """

        collection = self.themes_collection
        theme = collection.find_one_and_update(
            {"unique_identifier": theme.unique_identifier},
            {"$set": theme.model_dump()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return theme

    def aggregate_themes(self, filters: List[Dict[str, Any]]) -> CommandCursor:
        """
        Aggregate themes based on specified filters.

        Parameters:
        ----------
        filters : List[Dict[str, Any]]
            A list of aggregation pipeline stages used to filter and process the themes.

        Returns:
        -------
        CommandCursor
            A cursor to iterate over the results of the aggregation query.
        """
        collection = self.themes_collection
        return collection.aggregate(filters)

    def get_theme(self, filters: Dict[str, Any]) -> Optional[Theme]:
        """
        Retrieve a single theme matching the given filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filter criteria.

        Returns
        -------
        Optional[Theme]
            The matching theme, if found.
        """
        collection = self.themes_collection
        theme = collection.find_one(filters)
        if theme:
            return Theme(**theme)
        raise ValueError(
            "There are no theme corresponding to your query in the database."
        )

    def get_themes(self, filters: Dict[str, Any]) -> Cursor:
        """
        Retrieve themes matching the given filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filter criteria.

        Returns
        -------
        Cursor
            A cursor with the matching themes.
        """
        collection = self.themes_collection
        return collection.find(filters)

    def get_sub_themes_list_from_theme(
        self, theme_identifier: str, flatten: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a list of sub-themes for a given theme identifier.

        Parameters
        ----------
        theme_identifier : str
            The unique identifier of the parent theme for which sub-themes are retrieved.
        flatten : bool
            If True, the result will be a flattened list of sub-themes. Defaults to False.

        Returns
        ----------
        List[Dict[str, Any]]:
            A list of dictionaries representing the sub-themes. If `flatten` is True, the list
            is flattened to include nested sub-themes at the top level.
        """
        collection = self.themes_collection
        children_themes = collection.find({"parent_theme_identifier": theme_identifier})

        themes = []

        for children_theme in children_themes:
            sub_themes = self.get_sub_themes_list_from_theme(
                children_theme["unique_identifier"], themes
            )
            if len(sub_themes):
                themes.append(
                    {
                        "name": children_theme["name"],
                        "level": children_theme["level"],
                        "total": children_theme["total"],
                        "children": sub_themes,
                    }
                )
            else:
                themes.append(
                    {
                        "name": children_theme["name"],
                        "level": children_theme["level"],
                        "total": children_theme["total"],
                    }
                )

        if flatten:
            return flatten_list(themes, "children")

        return themes

    def get_themes_by_level(self, level: int) -> Cursor:
        """
        Returns a Cursor of the themes of the given level (from 0 to 3), sorted ASC by name.
        """
        collection = self.themes_collection
        return (
            collection.find({"level": level})
            .sort([("name", ASCENDING)])
            .collation(french_collation)
        )

    def get_parent_theme_from_child_theme_name(
        self, child_theme_name: str, stop_at_level: int = 3, base_theme_level: int = 0
    ) -> Theme:
        """
        Retrieve the parent theme given a child theme name.

        Parameters
        ----------
        child_theme_name: str
            Name of the child theme.
        stop_at_level: int, default=3
            Define the theme mapping hierarchy level at which to stop.
        base_theme_level: int, default=0
            Define the level from which to start looking from the child theme.

        Returns
        -------
        Theme
            The parent theme.
        """
        child_theme = self.get_theme(
            {"name": child_theme_name, "level": base_theme_level}
        )

        if child_theme.parent_theme_identifier:
            parent_theme = self.get_parent_theme(
                child_theme.parent_theme_identifier,
                stop_at_level=stop_at_level,
                base_theme_level=base_theme_level,
            )

            return parent_theme

        raise ValueError(
            "There are corresponding parent theme to your query in the database."
        )

    def get_parent_theme(
        self,
        parent_theme_identifier: str,
        stop_at_level: int = 3,
        base_theme_level: int = 0,
    ) -> Theme:
        """
        Retrieve the top level theme of a theme. Takes the theme's parent theme
        identifier as parameter.

        Parameters
        ----------
        parent_theme_identifier: str
            Name of the parent theme.
        base_theme_level: int, default=0
            The theme level mapping where to start from. Change it if the
            base theme is not level 0.
        stop_at_level: int, default=3
            Define the theme mapping level where to stop.

        Returns
        -------
        Theme
            A parent theme.
        """
        parent_theme = self.get_theme(
            {
                "unique_identifier": parent_theme_identifier,
                "level": base_theme_level + 1,
            }
        )

        if parent_theme.level < 3 and parent_theme.level != stop_at_level:
            while parent_theme.parent_theme_identifier:
                parent_theme = self.get_theme(
                    {"unique_identifier": parent_theme.parent_theme_identifier}
                )

        return parent_theme

    def upsert_question(self, question: Question) -> Question | None:
        """
        Add a question to the database.

        Parameters
        ----------
        question: Question
            A question and its associated metadata.
        """
        collection = self.questions_collection
        question = collection.find_one_and_update(
            {"id": question.id},
            {"$set": question.model_dump()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return question

    def get_question(self, filters: Dict[str, Any]) -> Optional[Question]:
        """
        Retrieve a single question matching the given filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filter criteria.

        Returns
        -------
        Optional[Question]
            The matching question, if found.
        """
        collection = self.questions_collection
        return collection.find_one(filters)

    def get_questions(
        self, filters: Dict[str, Any], projection: Optional[Dict[str, int]] = None
    ) -> Cursor:
        """
        Retrieve questions matching the given filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filter criteria.
        projection : Optional[Dict[str, int]]
            Fields to include or exclude.

        Returns
        -------
        Cursor
            A cursor with the matching questions.
        """
        collection = self.questions_collection
        questions = collection.find(filters)
        if questions:
            return questions
        raise ValueError(
            "There are no question corresponding to your query in the database."
        )

    def aggregate_questions(self, filters: List[Dict[str, Any]]) -> CommandCursor:
        """
        Aggregate questions based on specified filters.

        Parameters:
        ----------
        filters : List[Dict[str, Any]]
            A list of aggregation pipeline stages used to filter and process the themes.

        Returns:
        -------
        CommandCursor
            A cursor to iterate over the results of the aggregation query.
        """
        collection = self.questions_collection
        return collection.aggregate(filters)

    def get_random_questions(
        self,
        number_of_questions: int = 1000,
        legislature: Optional[int] = None,
        accepted_themes: Optional[List[str]] = None,
        remove_empty_questions: bool = True,
    ) -> CommandCursor:
        """
        Sample a set of random questions from the database.

        Parameters
        ----------
        number_of_questions: int, default=1000
            The number of questions to sample.
        legislature: int | None, default=None
            If not None, defines a given legislature from which to sample questions
            from.
        accepted_themes: List[str] | None, default=None
            The list of themes from which to filter the questions to be sampled from.
        remove_empty_questions: bool, default=True
            Defines if empty questions can be sampled.

        Returns
        -------
        CommandCursor
            A PyMongo cursor from which to iterate on the result set.
        """
        collection = self.questions_collection
        pipeline = []

        if accepted_themes:
            pipeline.append({"$match": {"theme": {"$in": accepted_themes}}})

        if legislature is not None:
            regex = rf"{legislature}-.*"
            pipeline.append({"$match": {"id": {"$regex": regex}}})

        if remove_empty_questions:
            pipeline.append({"$match": {"question_text": {"$ne": ""}}})

        pipeline.append({"$match": {"congressman": {"$ne": None}}})

        pipeline.append({"$sample": {"size": number_of_questions}})

        return collection.aggregate(pipeline)

    def count_documents_by_theme(self, theme: str) -> int:
        """
        Count documents based on a specified theme name.

        Parameters
        ----------
        theme: theme
            A given theme name.

        Returns
        -------
        int
            The number of documents found.
        """
        collection = self.questions_collection
        return collection.count_documents({"theme": theme})

    def check_question(self, question_id: str) -> bool:
        """
        Verify if the question is already registered in the database.

        Parameters
        ----------
        question: str
            A question and its associated metadata.

        Returns
        -------
        bool
            True if the question is already registered.
        """
        collection = self.questions_collection
        existing_document = collection.find_one({"id": question_id})
        if existing_document:
            logging.debug(
                "La question associée à l'ID " f"{question_id} est déjà présente."
            )
            return True
        else:
            return False

    def upsert_prompt(self, prompt: Prompt) -> Prompt:
        """
        Upsert a prompt in the database.

        Parameters
        ----------
        prompt: Prompt
            A given prompt.

        Returns
        -------
        Prompt
            The inserted prompt.
        """
        collection = self.prompts_collection
        prompt = collection.find_one_and_update(
            {"unique_identifier": prompt.unique_identifier},
            {"$set": prompt.model_dump()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return Prompt(**prompt)  # type: ignore

    def get_prompt(self, filters: Dict[str, Any] = {}) -> Prompt:
        """
        Retrieve a prompt in the database following given filters.

        Parameters
        ----------
        filters: Dict[str, Any]
            A custom mongo query.

        Returns
        -------
        Prompt
            The first corresponding prompt.

        Raises
        ------
        ValueError
            If no prompt could be retrieved given the provided filters.
        """
        collection = self.prompts_collection
        prompt = collection.find_one(filters)

        if prompt:
            return Prompt(**prompt)

        raise ValueError(
            "There are no prompt corresponding to your query in the database."
        )

    def get_prompts(self, filters: Dict[str, Any] = {}) -> Cursor:
        """
        Retrieve prompts matching the given filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filter criteria.

        Returns
        -------
        Cursor
            A cursor with the matching prompts.
        """
        collection = self.prompts_collection
        return collection.find(filters)

    def get_prompt_results(self, filters: Dict[str, Any] = {}) -> Cursor:
        """
        Retrieve prompt results in the database following the given filters.

        Parameters
        ----------
        filters: Dict[str, Any], default={}
            A custom mongo query.

        Returns
        -------
        Cursor
            A cursor to iterate over the result set.

        Raises
        ------
        ValueError
            If no prompt result be retrieved given the provided filters.
        """
        collection = self.prompt_results_collection
        prompt_results = collection.find(filters)
        if prompt_results:
            return prompt_results
        raise ValueError(
            "There are no prompt result corresponding to your query in the database."
        )

    def add_prompt_result(self, prompt_result: PromptResult) -> InsertOneResult:
        """
        Inserts a new prompt result document into the PromptResults collection.

        Parameters
        ----------
        prompt_result : PromptResult
            The PromptResult object to be inserted into the collection.

        Returns
        -------
        InsertOneResult
            The result of the insert operation.
        """
        collection = self.prompt_results_collection
        return collection.insert_one(prompt_result.model_dump())

    def add_prompt_run(self, prompt_run: PromptRun) -> InsertOneResult:
        """
        Inserts a new prompt run document into the PromptRuns collection.

        Parameters
        ----------
        prompt_run : PromptRun
            The PromptRun object to be inserted into the collection.

        Returns
        -------
        InsertOneResult
            The result of the insert operation.
        """
        collection = self.prompt_runs_collection
        return collection.insert_one(prompt_run.model_dump())

    def get_prompt_run(self, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single prompt run document from the PromptRuns collection based on the provided filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filters to apply when retrieving a prompt run from the collection.

        Returns
        -------
        Optional[Dict[str, Any]]
            The prompt run document if found, otherwise None.
        """
        collection = self.prompt_runs_collection
        return collection.find_one(filters)

    def get_prompt_runs(self, filters: Dict[str, Any] = {}) -> Cursor:
        """
        Retrieve prompt runs in the database following the given filters.

        Parameters
        ----------
        filters: Dict[str, Any]
            A custom mongo query.

        Returns
        -------
        CommandCursor
            A cursor to iterate over the result set.
        """
        collection = self.prompt_runs_collection
        prompt_runs = collection.find(filters)
        if prompt_runs:
            return prompt_runs
        raise ValueError(
            "There are no prompt runs corresponding to your query in the database."
        )

    def upsert_prompt_result(
        self, prompt_result: PromptResult, prompt_result_id: ObjectId
    ) -> PromptResult:
        """
        Insert or update a prompt result.

        Parameters:
        ----------
        prompt_result : PromptResult
            The PromptResult object containing the data to be inserted or updated in the collection.
        prompt_result_id : ObjectId
            The unique identifier of the prompt result to be updated. If it does not exist, a new document is inserted.

        Returns:
        -------
        PromptResult
            The updated or inserted PromptResult document from the database, after the upsert operation.
        """
        collection = self.prompt_results_collection
        prompt_result = collection.find_one_and_update(
            {"_id": prompt_result_id},
            {"$set": prompt_result.model_dump()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return prompt_result

    def update_many_prompt_results(
        self, updates: Dict[str, Any], filters: Dict[str, Any] = {}
    ) -> None:
        """
        Updates multiple documents in the PromptResults collection based on the given filters and updates.

        Parameters
        ----------
        updates : Dict[str, Any]
            The update operations to apply to the matched documents.
        filters : Dict[str, Any], default={}
            The filters used to match the documents to be updated.

        Returns
        -------
        None
            The function does not return any value.
        """

        collection = self.prompt_results_collection
        collection.update_many(filters, updates)

    def update_many_prompt_runs(
        self, updates: Dict[str, Any], filters: Dict[str, Any] = {}
    ) -> None:
        """
        Updates multiple documents in the PromptRuns collection based on the given filters and updates.

        Parameters
        ----------
        updates : Dict[str, Any]
            The update operations to apply to the matched documents.
        filters : Dict[str, Any], default={}
            The filters used to match the documents to be updated.

        Returns
        -------
        None
            The function does not return any value.
        """

        collection = self.prompt_runs_collection
        collection.update_many(filters, updates)

    def add_batch(self, batch: Batch) -> InsertOneResult:
        """
        Inserts a new batch document into the Batches collection.

        Parameters
        ----------
        batch : Batch
            The Batch object to be inserted into the collection.

        Returns
        -------
        InsertOneResult
            The result of the insert operation.
        """
        collection = self.batches_collection
        return collection.insert_one(batch.model_dump())

    def get_batch(self, filters: Dict[str, Any]) -> Dict:
        """
        Retrieve a batch in the database following given filters.

        Parameters
        ----------
        filters: Dict[str, Any]
            A custom mongo query.

        Returns
        -------
        Prompt
            The first corresponding batch.

        Raises
        ------
        ValueError
            If no batch could be retrieved given the provided filters.
        """
        collection = self.batches_collection
        batch = collection.find_one(filters)
        if batch:
            return batch

        raise ValueError(
            "There are no prompt corresponding to your query in the database."
        )

    def get_batches(self, filters: Dict[str, Any]) -> Cursor:
        """
        Retrieves batches from the Batches collection based on the provided filters.

        Parameters
        ----------
        filters : Dict[str, Any]
            The filters to apply when retrieving batches from the collection.

        Returns
        -------
        Cursor
            A PyMongo cursor to iterate over the matched batch documents.
        """
        collection = self.batches_collection
        return collection.find(filters)

    def add_question_ids_to_batch(
        self, question_ids: List[str], batch_id: ObjectId
    ) -> None:
        collection = self.batches_collection
        collection.update_one(
            {"_id": batch_id},
            {"$push": {"question_ids": {"$each": question_ids}}},
        )
