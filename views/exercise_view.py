from controllers.exercise_controller import ExerciseController
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.table import Table


console = Console() 
class ExerciseView:
    def __init__(self, exercise_controller):
        self.exercise_controller = exercise_controller


    def display_menu(self):
            while True:
                menu = """
    1. Add Exercise
    2. Get Exercise
    3. Get All Exercises
    4. Update Exercise
    5. Delete Exercise
    6. Search Exercise
    7. Count Exercises
    0. back
    """
                console.clear()
                console.print(Align.center(
                    Panel.fit(
                        menu,
                        title="[bold cyan]]exercise Management[/]",
                        border_style="cyan"

                    )))
                choice = Prompt.ask("[bold yellow]Choice an option.", default="")
                if choice == "1":
                    self.add_exercise()

                if choice == "2":
                    self.get_exercise()

                if choice == "3":
                    self.get_all_exercises()

                if choice == "4":
                    self.update_exercise()

                if choice == "5":
                    self.delete_exercise()

                if choice == "6":
                    self.search_exercise()

                if choice == "7":
                    self.count_exercises()
                if choice == "0":
                    break
            return           

    def add_exercise(self):
        exercise_name = Prompt.ask("exercise Name :", default="")
        level = Prompt.ask("Level :", default="")
        course_id = int(Prompt.ask("course ID :", default=""))

        try:
            result = self.exercise_controller.create_exercise(exercise_name, course_id, level)
            console.print(f"[bold green]{result}[/]")
        except ValueError as error :
            console.print(f"[bold red]{error}[/]")
        Prompt.ask("[bold yellow]Press Enter to continou", default="")
    def get_exercise(self):

        try:
            exercise_id = int(Prompt.ask("exercise ID", default=""))
        except ValueError :
            console.print(
                "[bold red]Exercise ID must be an integer.[/]"
            )
            Prompt.ask("\nPress Enter to countinue", default="")
            return           
        
        try:
            exercise = self.exercise_controller.get_exercise(exercise_id)

            console.print(Panel.fit(f"""
ID : {exercise.exercise_id}
exercise Name : {exercise.exercise_name}
level : {exercise.course}
course : {exercise.level}


"""))
            
        except ValueError as error:
            console.print(f"[bold red]{error}[/]")
            Prompt.ask("\nPress Enter to continue", default="")
    def get_all_exercises(self):
            
        try:
            exercises = self.exercise_controller.get_all_exercises()
            if not exercises:
                console.print("[bold red]No exercises found.[/]")
                console.print("[bold yellow]Press Enter to continue[/]")
                return
            tabel = Table(title="exercises", border_style="cyan")
            tabel.add_column("Exercise ID")
            tabel.add_column("exercise Name")
            tabel.add_column("Level")
            tabel.add_column("course ID")
            for exercise in exercises:
                    tabel.add_row(
                        str(exercise.exercise_id),
                        exercise.exercise_name,
                        str(exercise.course.course_id),
                        exercise.level,
                        
                
                    )
            console.print(
                    Align.center(tabel)
                )
                    
        except ValueError as error:
            console.print(
                f"[bold red] {error}[/]"
            )
        Prompt.ask("\nPress Enter to continue", default="")

    def update_exercise(self):
        try:
            exercise_id = int(Prompt.ask("exercise ID"))
            print("\nLeave a feild empty if you dont want to change it.")

            exercise_name = Prompt.ask("Full name", default="")
            level = Prompt.ask("email", default="level")
            course_id = int(Prompt.ask("course", default=""))

            updates = {}
            if exercise_name.strip():
                updates["exercise name"] = exercise_name
            if level.strip():
                updates["level"] = level
            if course_id.strip():

                try:
                    updates["course"] = course_id
                except ValueError:
                    raise ValueError(
                        "Course ID must be an integer."
                    )

            if not updates:
                console.print("[bold yellow]No changes were provided.[/")
                return
            Prompt.ask("\nPress Enter to continue")

            result = self.exercise_controller.update_exercise(
                    exercise_id,
                    **updates
                )
            console.print(
                f"[bold green]{result}[/]]"
            )
        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )
        Prompt.ask("\Press Enter to continue", default="")
        
    def delete_exercise(self):
        try:    
            exercise_id = int(Prompt.ask("[bold cyan]exercise ID", default=""))
            result = self.exercise_controller.delete_exercise(exercise_id)
            console.print(f"[bold green]{result}[/]")
        except ValueError as error:
            console.print(f"[bold red]{error}[/]")

        Prompt.ask("\Press Enter to continue", default="")

    def search_exercise(self):
        try:
            exercise_name = Prompt.ask("exercise Name", default="")
            exercises = self.exercise_controller.search_exercise(exercise_name)
            tabel = Table(title="exercises",
                  border_style="cyan")
            
            tabel.add_column("exercise ID")
            tabel.add_column("exercise Name")
            tabel.add_column("Level")
            tabel.add_column("course ID")
            
            for exercise in exercises:
                tabel.add_row(
                    str(exercise.exercise_id),
                    exercise.exercise_name,
                    str(exercise.course.course_id),
                    exercise.level
                )
            console.print(Align.center(tabel))
        except ValueError as error:
            console.print(
                f"[bold red] {error}[/]"
            )
        Prompt.ask("\nPress Enter to continue", default="")
    def count_exercise(self):
         
        count_of_exercises = self.exercise_controller.count_exercises()
        console.print(Panel.fit(f"[bold green]{count_of_exercises}[/]",
                                title= "Count of exercises",
                                border_style="cyan"))
        
        Prompt.ask("\nPress Enter to continue", default="")
