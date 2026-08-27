from models.exercise import Exercise
from utils.validation_exercise import ExerciseValidator
from models.exercise import Exercise
class ExerciseController:
    def __init__(self, exercise_repo, course_repo):
        self.exercise_repo = exercise_repo
        self.course_repo = course_repo

    def create_exercise(self, exercise_name, course_id):

        ExerciseValidator.validation_exercise_name(exercise_name)

        #find the course id of the exrcise we need 
        course = self.course_repo.get_course(course_id)
        if course is None:
            raise ValueError("No course found.")
        exercise = Exercise(None, exercise_name, course)

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
        if "course_id" in kwargs:
            course = self.course_repo.get_course(
                kwargs["course_id"]
            )
            if course is None:
                raise ValueError("Course not found.")
            kwargs["course"] = course
            del kwargs["course_id"]

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
        if not exercises:
            raise ValueError("No exercise found.")
        return exercises

    def count_exercise(self):
        return self.exercise_repo.count_exercises()

    
    def get_exercises_by_level(self, level):

        ExerciseValidator.validation_level(level)

        return self.exercise_repo.get_exercises_by_level(level)