from models.exercise import exercise
from utils.validation_exercise import ExerciseValidator
from models.exercise import Exercise
class ExerciseController:
    def __init__(self, exercise_repo):
        self.exercise_repo = exercise_repo

    def create_execise(self, exercise_name, exercise, level):

        ExerciseValidator.validation_exercise_name(exercise_name)
        ExerciseValidator.validation_level(level)
        if not isinstance(exercise, exercise):
            raise ValueError("invalid exercise.")
        exercise = Exercise(None, exercise_name, exercise, level)

        self.exercise_repo.add_exercise(exercise)
        return "Exercise created successfully."

    def get_exercise(self, exercise_id):

        if not isinstance(exercise_id, int):
            raise ValueError("exercise ID must be an int")
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError("exercise not found.")
        return exercise

    def get_all_exercises(self):
        return self.exercise_repo.get_all_exercises()

    def update_exercise(self, exercise_id, **kwargs):
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None :
            raise ValueError("exercise not found")
        if "exercise_name" in kwargs:
            ExerciseValidator.validation_exercise_name(kwargs["exercise_name"])

        self.exercise_repo.update_exercise(exercise_id, **kwargs)
        return "exercise updated successfully."

    
    def delete_exercise(self, exercise_id):
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError('exercise ID not found.')
        self.exercise_repo.delete_exercise(exercise_id)
        return "exercise deleted successfully"

    def search_exercise(self, query):
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")

        exercises = self.exercise_repo.search_exercise(query)
        if not exercise:
            raise ValueError("No exercise found.")
        return exercises

    def count_exercise(self):
        return self.exercise_repo.count_exercise()