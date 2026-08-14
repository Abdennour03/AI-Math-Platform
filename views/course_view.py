from controllers.course_controller import CourseController
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.table import Table


console = Console() 
class CourseView:
    def __init__(self, course_controller):
        self.course_controller = course_controller


    def display_menu(self):
            while True:
                menu = """
    1. Add course
    2. Get course
    3. Get All course
    4. Update course
    5. Delete course
    6. Search course
    7. Count course
    0. back
    """
                console.clear()
                console.print(Align.center(
                    Panel.fit(
                        menu,
                        title="[bold cyan]]course Management[/]",
                        border_style="cyan"

                    )))
                choice = Prompt.ask("[bold yellow]Choice an option.", default="")
                if choice == "1":
                    self.add_course()

                if choice == "2":
                    self.get_course()

                if choice == "3":
                    self.get_all_courses()

                if choice == "4":
                    self.update_course()

                if choice == "5":
                    self.delete_course()

                if choice == "6":
                    self.search_course()

                if choice == "7":
                    self.count_course()
                if choice == "0":
                    break
            return           

    def add_course(self):
        course_name = Prompt.ask("Course Name :", default="")
        teacher_id = int(Prompt.ask("Teacher ID :", default=""))
        level = Prompt.ask("Level :", default="")
        semester = Prompt.ask("Semester :", default="")

        try:
            result = self.course_controller.create_course(course_name, teacher_id , level, semester)
            console.print(f"[bold green]{result}[/]")
        except ValueError as error :
            console.print(f"[bold red]{error}[/]")
        Prompt.ask("[bold yellow]Press Enter to continou", default="")
    def get_course(self):

        try:
            course_id = int(Prompt.ask("Course ID", default=""))
        except ValueError :
            console.print(
                "[bold red]teacher ID must be an integer.[/]"
            )
            Prompt.ask("\nPress Enter to countinue", default="")
            return           
        
        try:
            course = self.course_controller.get_course(course_id)

            console.print(Panel.fit(f"""
ID : {course.course_id}
Course Name : {course.course_name}
Level : {course.level}
Semester : {course.semester}

"""))
            
        except ValueError as error:
            console.print(f"[bold red]{error}[/]")
            Prompt.ask("\nPress Enter to continue", default="")
    def get_all_courses(self):

        try:
            courses = self.course_controller.get_all_courses()

            if not courses:
                console.print("[bold red]No courses found.[/]")
                console.print("[bold yellow]Press Enter to continue[/]")
                return

            table = Table(
                title="Courses",
                border_style="cyan"
            )

            table.add_column("ID")
            table.add_column("Course Name")
            table.add_column("Teacher")
            table.add_column("Level")
            table.add_column("Semester")

            for course in courses:
                table.add_row(
                    str(course.course_id),
                    course.course_name,
                    course.teacher.full_name,
                    course.level,
                    course.semester
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

    def update_course(self):
        try:
            course_id = int(Prompt.ask("course ID"))
            
            print("\nLeave a feild empty if you dont want to change it.")

            course_name = Prompt.ask("Full name", default="")
            level = Prompt.ask("email", default="level")
            semester = Prompt.ask("semester", default="")

            updates = {}
            if course_name.strip():
                updates["full_name"] = course_name
            if level.strip():
                updates["email"] = level
            if semester.strip():
                updates["password"] = semester
            if not updates:
                console.print("[bold yellow]No changes were provided.[/")
                return
            Prompt.ask("\nPress Enter to continue")
            result = self.course_controller.update_course(
                    course_id,
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
        
    def delete_course(self):
        try:    
            course_id = int(Prompt.ask("[bold cyan]Course ID", default=""))
            result = self.course_controller.delete_course(course_id)
            console.print(f"[bold green]{result}[/]")
        except ValueError as error:
            console.print(f"[bold red]{error}[/]")

        Prompt.ask("\Press Enter to continue", default="")

    def search_course(self):
        try:
            course_name = Prompt.ask("Course Name", default="")
            courses = self.course_controller.search_course(course_name)
            tabel = Table(title="Courses",
                  border_style="cyan")
            
            tabel.add_column("COurse ID")
            tabel.add_column("Course Name")
            tabel.add_column("Level")
            tabel.add_column("Semester")
            
            for course in courses:
                tabel.add_row(
                    int(course.course_id),
                    course.course_name,
                    course.level,
                    course.semester
                )
            console.print(Align.center(tabel))
        except ValueError as error:
            console.print(
                f"[bold red] {error}[/]"
            )
        Prompt.ask("\nPress Enter to continue", default="")
    def count_course(self):
         
        count_of_courses = self.course_controller.count_courses()
        console.print(Panel.fit(f"[bold green]{count_of_courses}[/]",
                                title= "Count of Courses",
                                border_style="cyan"))
        
        Prompt.ask("\nPress Enter to continue", default="")
