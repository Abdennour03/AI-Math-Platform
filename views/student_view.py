from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt

console = Console()
class StudentView:
    def __init__(self, student_controller, notification_controller):
        self.student_controller = student_controller
        self.notification_controller = notification_controller


    def display_menu(self):
        while True:
            menu = """
    1. Add Student
    2. Get Student
    3. Get All Student
    4. Update Student
    5. Delete Student
    6. Search Student
    7. Count Student
    8. My Notifications
    9. Mark Notification as Read
    0. back
    """
            console.clear()
            console.print(
                Align.center(
                    Panel.fit(
                        menu,
                        title= "[bold cyan]Student Management[/bold cyan]",
                        border_style="cyan"
                    )
                )
            )
            choice = Prompt.ask(
                "[bold yellow]Choose an option[/bold yellow]"
            )

            
            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.get_student()

            elif choice == "3":
                self.get_all_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                self.search_student()

            elif choice == "7":
                self.count_student()

            elif choice == "8":
               self.get_my_notification()

            elif choice == "9":
                self.mark_notification_as_read()
            elif choice == "0":
                break
                   
        return 


    def add_student(self):

        full_name = Prompt.ask("Full name")
        email = Prompt.ask("email")
        password = Prompt.ask("password")
        phone_number = Prompt.ask("phone number")
        level = Prompt.ask("level")

        # handl the errors of variabls if any variable not correct 
        try:

            result =self.student_controller.create_student(full_name, email, password, phone_number, level)
            console.print(f"[bold green] {result} [/bold green]")

        except ValueError as error:
            console.print(
                f"[bodl red] {error} [/bold red]"
            )
        Prompt.ask("\nPrees Enter to continue", default="")
    def get_student(self):
        try:
            student_id = int(Prompt.ask("Student ID"))
        except ValueError:
            console.print(
                "[bold red]Student ID must be an integer.[/bold red]"
            )
            Prompt.ask("\nPress Enter to countinue", default="")
            return
        
        try:
            student = self.student_controller.get_student(student_id)
            console.print(
                Panel.fit(
                f"""
ID : {student.student_id}
Name : {student.full_name}
Email : {student.email}
Phone : {student.phone_number}
Level : {student.level}
""",
                    title= "[bold cyan]Student Information[/bold cyan]",
                    border_style="cyan"
                )
            )
        except ValueError as error:
            console.print(
                f"[bold red] {error} [/bold red]"
            )
            Prompt.ask("\nPress Enter to continue", default="")

    def get_my_notification(self):
        try:
            student_id = int(Prompt.ask("Student ID"))

            notifications = self.notification_controller.get_student_notifications(
                student_id
            )

            if not notifications:
                console.print(
                    "[bold yellow]No notifications found.[/]"
                )
                Prompt.ask("\nPress Enter to continue", default="")
                return

            table = Table(
                title="My Notifications",
                border_style="cyan"
            )

            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Message")
            table.add_column("Status")

            for student_notification in notifications:
                notification = student_notification.notification

                status = (
                    "Read"
                    if student_notification.is_read
                    else "Unread"
                )

                table.add_row(
                    str(student_notification.student_notification_id),
                    notification.title,
                    notification.message,
                    status
                )

            console.print(Align.center(table))

        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )

        Prompt.ask("\nPress Enter to continue", default="")
    def get_all_student(self):
        try:
            students = self.student_controller.get_all_students()
            if not students:
                console.print(
                    "[bold yellow]No students found.[/bold yellow]")
                Prompt.ask("\nPress Enter to continue", default="")
                return
                       
            tabel = Table(
                        title="Students",
                        border_style="cyan")
            tabel.add_column("ID")
            tabel.add_column("Name")
            tabel.add_column("Email")
            tabel.add_column("Phone")
            tabel.add_column("Level")
                
            for student in students:
                tabel.add_row(
                    str(student.student_id),
                    student.full_name,
                    student.email,
                    student.phone_number,
                    student.level
                )
            console.print(
                Align.center(tabel)
            )
        except ValueError as error:
            console.print(
                f"[bold red] {error} [/bold red]"
            )
        Prompt.ask("\nPress Enter to continue", default="")
    def mark_notification_as_read(self):
        try:
            student_notification_id = int(
                Prompt.ask("Notification ID")
            )

            result = self.notification_controller.mark_as_read(
                student_notification_id
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
    def update_student(self):
        try:
            student_id = int(Prompt.ask("Student ID"))
            print("\nLeave a feild empty if you dont want to change it.")

            full_name = Prompt.ask("Full name", default="")
            email = Prompt.ask("email", default="")
            password = Prompt.ask("password", default="")
            phone_number = Prompt.ask("phone number", default="")
            level = Prompt.ask("level", default="")

            updates = {}
            if full_name.strip():
                updates["full_name"] = full_name
            if email.strip():
                updates["email"] = email
            if password.strip():
                updates["password"] = password
            if phone_number.strip():
                updates["phone_number"] = phone_number
            if level.strip():
                updates["level"] = level
            if not updates:
                console.print("[bold yellow]No changes were provided.[/")
                return
            Prompt.ask("\nPress Enter to continue")
            result = self.student_controller.update_student(
                    student_id,
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



    def delete_student(self):
        try:
            student_id = int(Prompt.ask("Student ID"))
            result = self.student_controller.delete_student(student_id)
            console.print(
                f"[bold green] {result}[/]"
            )
        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )
        Prompt.ask("\nPrees Enter to continue", default="")
    def search_student(self):
        try:
            name_student = Prompt.ask("Name of Student")
            students = self.student_controller.search_student(name_student)
            tabel = Table(
                title="Student Search",
                border_style="cyan"

            )
            tabel.add_column("ID")
            tabel.add_column("Name")
            tabel.add_column("Email")
            tabel.add_column("Phone")
            tabel.add_column("Level")
            for student in students:
                tabel.add_row(
                    str(student.student_id),
                    student.full_name,
                    student.email,
                    student.phone_number,
                    student.level
                )
                console.print(
                    Align.center(tabel)
                    
                )
        except ValueError as error :
            console.print(
                f"[bold red] {error}[/]")
        Prompt.ask("\nPress Enter to continue", default="")
    def count_student(self):
       
        count_of_student = self.student_controller.count_students()
        console.print(
            Panel.fit(f"[bold green]{count_of_student}[/]",
                  title="[bodl cyan]Total Student[/]",
                  border_style="cyan")
                  
        )

        Prompt.ask("\nPress Enter to continue", default="")