class ExerciseRepo:
    def __init__(self):
        self.exercices = []

    def add_exercice(self, exercice):
        self.exercices.append(exercice)

    def get_exercice(self, exercice_id):
        for exercice in self.exercices:
            if exercice.exercice_id == exercice_id:
                return exercice
        return None 


    def get_all_exercices(self):
        return self.exercices

    def update_exercice(self, exercice_id, **kwargs):
        for exercice in self.exercices:
            if exercice.exercice_id == exercice_id:
                for key, value in kwargs.items():
                    if hasattr(exercice, key):
                        setattr(exercice, key, value)
                return True 
        return False

    def delete_exercice(self, exercice_id):
        for index, exercice in enumerate(self.exercices):
            if exercice.exercice_id == exercice_id:
                del self.exercices[index]
                return True
        return False

    def search_exercice(self, query):
        result_exercices = []
        for exercice in self.exercices:
            if query.lower() in exercice.exercice_name.lower() :
                result_exercices.append(exercice)
        return result_exercices


    def count_exercices(self):
        return len(self.exercices)