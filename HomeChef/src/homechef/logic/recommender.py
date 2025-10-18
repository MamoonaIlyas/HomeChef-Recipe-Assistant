from typing import List, Dict, Tuple

def match_score(user_ingredients: List[str], recipe_ingredients: List[str]) -> Tuple[float, list]:
    u = {i.lower().strip() for i in user_ingredients if i.strip()}
    r = {i.lower().strip() for i in recipe_ingredients if i.strip()}
    if not r:
        return 0.0, []
    overlap = u.intersection(r)
    missing = list(r - u)
    score = len(overlap) / len(r)
    return score, missing
