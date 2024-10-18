import random
import uuid
import hashlib
from typing import List
from bson import ObjectId
from models.Prompt import PromptResult
from prompting.get_themes_list import selected_level_1_themes_first_version


def generate_prompt_results(n: int) -> List[PromptResult]:
    themes_list, _ = selected_level_1_themes_first_version()
    random_level_0_themes_list = [
        "Agroalimentaire",
        "Engrais",
        "Horticulture",
        "Produits agricoles et alimentaires",
        "enseignement supérieur : personnel",
        "enseignement technique et professionnel : personnel",
        "Logement : aides et prets.",
    ]

    prompt_results = []
    for _ in range(n):
        legislature = random.randint(8, 16)
        question_id = f"{legislature}-{random.randint(100000, 999999)}QE"
        prompt_id = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        batch_id = str(ObjectId())
        run_id = str(ObjectId())
        response_tokens = random.randint(1, 10)
        prompt_tokens = random.randint(400, 450)
        question_theme = random.choice(random_level_0_themes_list)
        gold_label = random.choice(themes_list)
        final_answer = (
            gold_label if random.randint(1, 5) == 1 else random.choice(themes_list)
        )
        response = final_answer

        prompt_result = PromptResult(
            question_id=question_id,
            response=response,
            final_answer=final_answer,
            prompt_id=prompt_id,
            batch_id=batch_id,
            run_id=run_id,
            response_tokens=response_tokens,
            prompt_tokens=prompt_tokens,
            legislature=legislature,
            question_theme=question_theme,
            gold_label=gold_label,
        )
        prompt_results.append(prompt_result)

    return prompt_results
