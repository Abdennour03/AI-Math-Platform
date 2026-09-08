def validate_score(score, max_score):
    if not isinstance(score, (int, float)):
        raise ValueError("Score must be numeric.")
    if not isinstance(max_score, (int, float)) or max_score <= 0:
        raise ValueError("Exercise max_score must be a positive number.")
    if score < 0 or score > max_score:
        raise ValueError(f"Score must be between 0 and {max_score}.")


def validate_max_score(max_score):
    if not isinstance(max_score, (int, float)) or max_score <= 0:
        raise ValueError("max_score must be a positive number.")