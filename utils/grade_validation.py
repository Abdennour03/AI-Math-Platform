class GradeValidator:
    @staticmethod
    def validation_score(score):
        if not isinstance(score, (int, float)):
            raise ValueError("Score must be numeric.")

        if score < 0 or score > 20:
            raise ValueError("Score must be between 0 and 20")

        