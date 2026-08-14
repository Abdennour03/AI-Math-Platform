from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class GradeView:

    def __init__(self, grade_controller):
        self.grade_controller = grade_controller

    def display_menu(self):

        while True:

            menu = """
1. Add Grade
2. Get Grade
3. My Grades
4. Grades by Exercise
0. Back
"""

            console.clear()

            console.print(
                Align.center(
                    Panel.fit(
                        menu,
                        title="[bold cyan]Grade Management[/]",
                        border_style="cyan"
                    )
                )
            )

            choice = Prompt.ask(
                "[bold yellow]Choice an option[/]",
                default=""
            )

            if choice == "1":
                self.add_grade()

            elif choice == "2":
                self.get_grade()

            elif choice == "3":
                self.my_grades()

            elif choice == "4":
                self.grades_by_exercise()

            elif choice == "0":
                break

    def add_grade(self):
        try:
            student_id = int(Prompt.ask("Student ID"))
            exercise_id = int(Prompt.ask("Exercise ID"))
            score = float(Prompt.ask("Score"))
            result = self.grade_controller.create_grade(score, student_id, exercise_id)
            console.print(f"[bold green]{result}[/]")
        except ValueError as error:
            console.print(f"[bold red]{error}[/]")

    def get_grade(self):
        try:
            grade_id = int(
                Prompt.ask("Grade ID")
            )

            grade = self.grade_controller.get_grade(
                grade_id
            )

            console.print(
                Panel.fit(
                    f"""
    ID : {grade.grade_id}
    Score : {grade.score}
    Student : {grade.student.full_name}
    Exercise : {grade.exercise.exercise_name}
    """,
                    title="Grade",
                    border_style="cyan"
                )
            )

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask(
            "\nPress Enter to continue",
            default=""
        )

    # search grade by student id
    def my_grades(self):
        try:
            student_id = int(Prompt.ask("Student ID"))

            grades = self.grade_controller.search_grade_by_student(
                student_id
            )

            table = Table(
                title="My Grades",
                border_style="cyan")

            table.add_column("ID")
            table.add_column("Exercise")
            table.add_column("Score")

            for grade in grades:
                table.add_row(
                    str(grade.grade_id),
                    grade.exercise.exercise_name,
                    str(grade.score)
                )

            console.print(
                Align.center(table)
            )

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask(
            "\nPress Enter to continue",
            default=""
        )

    def grades_by_exercise(self):
        try:
            exercise_id = int(
                Prompt.ask("Exercise ID")
            )

            grades = self.grade_controller.search_grade_by_exercise(
                exercise_id
            )

            table = Table(
                title="Grades by Exercise",
                border_style="cyan"
            )

            table.add_column("Grade ID")
            table.add_column("Student")
            table.add_column("Score")

            for grade in grades:
                table.add_row(
                    str(grade.grade_id),
                    grade.student.full_name,
                    str(grade.score)
                )

            console.print(
                Align.center(table)
            )

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask(
            "\nPress Enter to continue",
            default=""
        )