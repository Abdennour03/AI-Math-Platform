class ExerciseRepo:
    def __init__(self):
        self.exercises = []
        self.next_id = 1

    def add_exercise(self, exercise):
        exercise.exercise_id = self.next_id
        self.next_id += 1
        self.exercises.append(exercise)

    def get_exercise(self, exercise_id):
        for exercise in self.exercises:
            if exercise.exercise_id == exercise_id:
                return exercise
        return None 


    def get_all_exercises(self):
        return self.exercises

    def update_exercise(self, exercise_id, **kwargs):
        for exercise in self.exercises:
            if exercise.exercise_id == exercise_id:
                for key, value in kwargs.items():
                    if hasattr(exercise, key):
                        setattr(exercise, key, value)
                return True 
        return False

    def delete_exercise(self, exercise_id):
        for index, exercise in enumerate(self.exercises):
            if exercise.exercise_id == exercise_id:
                del self.exercises[index]
                return True
        return False

    def search_exercise(self, query):
        result_exercises = []
        for exercise in self.exercises:
            if query.lower() in exercise.exercise_name.lower() :
                result_exercises.append(exercise)
        return result_exercises


    def count_exercises(self):
        return len(self.exercises)