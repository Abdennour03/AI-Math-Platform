class ExerciseValidator:
    @staticmethod
    def validation_exercise_name(exercise_name):
        exercise_name=exercise_name.strip()
        if not exercise_name:
            raise ValueError("Exercise name canot be empty.")
        if len(exercise_name) <3 or len(exercise_name)>100:
            raise ValueError("exercise name must contain at last 3 or not exceed 100 char...")
        return exercise_name
    
    @staticmethod
    def validation_level(level):
        level = level.strip()
        allowed_levels = {"3AC",
                          "TC",
                          "1BAC",
                          "2BAC"}
        if level not in allowed_levels:
            raise ValueError("Invalid level")