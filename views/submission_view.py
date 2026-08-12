from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.table import Table
from datetime import datetime

console = Console() 
class SubmissionView:
    def __init__(self, submission_controller):
        self.submission_controller = submission_controller


    def display_menu(self):
            while True:
                menu = """
1. Submit Exercise
2. Get Submission
3. My Submissions
4. Submissions by Exercise
0. Back
"""
                console.clear()
                console.print(Align.center(
                    Panel.fit(
                        menu,
                        title="[bold cyan]]submission Management[/]",
                        border_style="cyan"

                    )))
                choice = Prompt.ask("[bold yellow]Choice an option.", default="")
                if choice == "1":
                    self.add_submission()

                elif choice == "2":
                    self.get_submission()

                elif choice == "3":
                    self.my_submissions()

                elif choice == "4":
                    self.submissions_by_exercise()
                elif choice == "0":
                    break
            return
    def add_submission(self):
        try:
            student_id = int(Prompt.ask("Student ID"))
            exercise_id = int(Prompt.ask("Exercise ID"))
            file_path = Prompt.ask("File path")
            status = Prompt.ask("Status", default="submitted")

            submission_date = datetime.now()

            result = self.submission_controller.create_submission(
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            )

            console.print(
                f"[bold green]{result}[/]"
            )

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask(
            "\nPress Enter to continue",
            default=""
        )
    def get_submission(self):
        try:
            submission_id = int(
                Prompt.ask("Submission ID")
            )

            submission = self.submission_controller.get_submission(
                submission_id
            )

            console.print(
                Panel.fit(
                    f"""
    ID : {submission.submission_id}
    Student : {submission.student.full_name}
    Exercise : {submission.exercise.exercise_name}
    Submission Date : {submission.submission_date}
    File : {submission.file_path}
    Status : {submission.status}
    """,
                    title="Submission",
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
    def my_submissions(self):
        try:
            student_id = int(
                Prompt.ask("Student ID")
            )

            submissions = self.submission_controller.search_submission_by_student(
                student_id
            )

            table = Table(
                title="My Submissions",
                border_style="cyan"
            )

            table.add_column("ID")
            table.add_column("Exercise")
            table.add_column("Date")
            table.add_column("File")
            table.add_column("Status")

            for submission in submissions:
                table.add_row(
                    str(submission.submission_id),
                    submission.exercise.exercise_name,
                    str(submission.submission_date),
                    submission.file_path,
                    submission.status
                )

            console.print(Align.center(table))

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask(
            "\nPress Enter to continue",
            default=""
        )
    def submissions_by_exercise(self):
        try:
            exercise_id = int(
                Prompt.ask("Exercise ID")
            )

            submissions = self.submission_controller.search_submission_by_exercise(
                exercise_id
            )

            table = Table(
                title="Submissions",
                border_style="cyan"
            )

            table.add_column("ID")
            table.add_column("Student")
            table.add_column("Exercise")
            table.add_column("Date")
            table.add_column("File")
            table.add_column("Status")

            for submission in submissions:
                table.add_row(
                    str(submission.submission_id),
                    submission.student.full_name,
                    submission.exercise.exercise_name,
                    str(submission.submission_date),
                    submission.file_path,
                    submission.status
                )

            console.print(Align.center(table))

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask(
            "\nPress Enter to continue",
            default=""
        )

    