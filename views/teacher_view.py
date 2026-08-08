from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt

console = Console()
class TeacherView:
    def __init__(self, teacher_controller):
        self.teacher_controller = teacher_controller



    def display_menu(self):
        while True:
            menu = """
    1. Add teacher
    2. Get teacher
    3. Get All teacher
    4. Update teacher
    5. Delete teacher
    6. Search teacher
    7. Count teacher
    0. back
    """
            console.clear()
            console.print(
                Align.center(
                    Panel.fit(
                        menu,
                        title= "[bold cyan]teacher Management[/bold cyan]",
                        border_style="cyan"
                    )
                )
            )
            choice = Prompt.ask(
                "[bold yellow]Choose an option[/bold yellow]"
            )

            
            if choice == "1":
                self.add_teacher()

            elif choice == "2":
                self.get_teacher()

            elif choice == "3":
                self.get_all_teacher()

            elif choice == "4":
                self.update_teacher()

            elif choice == "5":
                self.delete_teacher()

            elif choice == "6":
                self.search_teacher()

            elif choice == "7":
                self.count_teacher()

            elif choice == "0":
                break
                   
        return 


    def add_teacher(self):

        full_name = Prompt.ask("Full name")
        email = Prompt.ask("email")
        password = Prompt.ask("password")
        phone_number = Prompt.ask("phone number")

        # handl the errors of variabls if any variable not correct 
        try:

            result =self.teacher_controller.create_teacher(full_name, email, password, phone_number)
            console.print(f"[bold green]{result}[/]")

        except ValueError as error:
            console.print(
                f"[bodl red]{error}[/]"
            )
        Prompt.ask("\nPrees Enter to continue", default="")
    def get_teacher(self):
        try:
            teacher_id = int(Prompt.ask("teacher ID"))
        except ValueError:
            console.print(
                "[bold red]teacher ID must be an integer.[/]"
            )
            Prompt.ask("\nPress Enter to countinue", default="")
            return
        
        try:
            teacher = self.teacher_controller.get_teacher(teacher_id)
            console.print(
                Panel.fit(
                f"""
ID : {teacher.teacher_id}
Name : {teacher.full_name}
Email : {teacher.email}
Phone : {teacher.phone_number}

""",
                    title= "[bold cyan]teacher Information[/bold cyan]",
                    border_style="cyan"
                )
            )
        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )
            Prompt.ask("\nPress Enter to continue", default="")


    def get_all_teacher(self):
        try:
            teachers = self.teacher_controller.get_all_teachers()
            if not teachers:
                console.print(
                    "[bold yellow]No teachers found.[/]")
                Prompt.ask("\nPress Enter to continue", default="")
                return
                       
            tabel = Table(
                        title="teachers",
                        border_style="cyan")
            tabel.add_column("ID")
            tabel.add_column("Name")
            tabel.add_column("Email")
            tabel.add_column("Phone")
            tabel.add_column("")
                
            for teacher in teachers:
                tabel.add_row(
                    str(teacher.teacher_id),
                    teacher.full_name,
                    teacher.email,
                    teacher.phone_number,
               
                )
            console.print(
                Align.center(tabel)
            )
        except ValueError as error:
            console.print(
                f"[bold red] {error}[/]"
            )
        Prompt.ask("\nPress Enter to continue", default="")

    def update_teacher(self):
        try:
            teacher_id = int(Prompt.ask("teacher ID"))
            print("\nLeave a feild empty if you dont want to change it.")

            full_name = Prompt.ask("Full name", default="")
            email = Prompt.ask("email", default="")
            password = Prompt.ask("password", default="")
            phone_number = Prompt.ask("phone number", default="")

            updates = {}
            if full_name.strip():
                updates["full_name"] = full_name
            if email.strip():
                updates["email"] = email
            if password.strip():
                updates["password"] = password
            if phone_number.strip():
                updates["phone_number"] = phone_number
            if not updates:
                console.print("[bold yellow]No changes were provided.[/")
                return
            Prompt.ask("\nPress Enter to continue")
            result = self.teacher_controller.update_teacher(
                    teacher_id,
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



    def delete_teacher(self):
        try:
            teacher_id = int(Prompt.ask("teacher ID"))
            result = self.teacher_controller.delete_teacher(teacher_id)
            console.print(
                f"[bold green] {result}[/]"
            )
        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )
        Prompt.ask("\nPrees Enter to continue", default="")
    def search_teacher(self):
        try:
            name_teacher = Prompt.ask("Name of teacher")
            teachers = self.teacher_controller.search_teacher(name_teacher)
            tabel = Table(
                title="teacher Search",
                border_style="cyan"

            )
            tabel.add_column("ID")
            tabel.add_column("Name")
            tabel.add_column("Email")
            tabel.add_column("Phone")
            tabel.add_column("")
            for teacher in teachers:
                tabel.add_row(
                    str(teacher.teacher_id),
                    teacher.full_name,
                    teacher.email,
                    teacher.phone_number,
    
                )
                console.print(
                    Align.center(tabel)
                    
                )
        except ValueError as error :
            console.print(
                f"[bold red] {error}[/]")
        Prompt.ask("\nPress Enter to continue", default="")
    def count_teacher(self):
       
        count_of_teacher = self.teacher_controller.count_teachers()
        console.print(
            Panel.fit(f"[bold green]{count_of_teacher}[/]",
                  title="[bodl cyan]Total teacher[/]",
                  border_style="cyan")
                  
        )

        Prompt.ask("\nPress Enter to continue", default="")