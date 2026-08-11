from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.table import Table


console = Console() 
class NotificationView:
    def __init__(self, notification_controller):
        self.notification_controller = notification_controller


    def display_menu(self):
            while True:
                menu = """
    1. Add notification
    2. Get notification
    3. Get All notifications
    4. Update notification
    5. Delete notification
    6. Search notification
    7. Count notifications
    0. back
    """
                console.clear()
                console.print(Align.center(
                    Panel.fit(
                        menu,
                        title="[bold cyan]]notification Management[/]",
                        border_style="cyan"

                    )))
                choice = Prompt.ask("[bold yellow]Choice an option.", default="")
                if choice == "1":
                    self.add_notification()

                if choice == "2":
                    self.get_notification()

                if choice == "3":
                    self.get_all_notifications()

                if choice == "4":
                    self.update_notification()

                if choice == "5":
                    self.delete_notification()

                if choice == "6":
                    self.search_notification()

                if choice == "7":
                    self.count_notifications()
                if choice == "0":
                    break
            return           

    def add_notification(self):
        titel = Prompt.ask("Notification titel :", default="")
        message = Prompt.ask("Message :", default="")
        
        try:
            teacher_id = int(Prompt.ask("Teacher ID"))
            # create notification
            notification = self.notification_controller.create_notification(titel, message, teacher_id)
            console.print(f"[bold green]{notification}[/]")
            console.print("1. All students")
            console.print("2. One students")
            choice = Prompt.ask("Choice an option",
                                choices = ["1", "2"])

            if choice == "1":
                result = self.notification_controller.send_to_all_students(
                notification
            )
            else:
                student_id = int(Prompt.ask("Student ID"))
                result = self.notification_controller.send_to_student(
                notification,
                student_id
            )
            console.print(f"[bold green]{result}[/]")
        
        except ValueError as error :
            console.print(f"[bold red]{error}[/]")
        Prompt.ask("[bold yellow]Press Enter to continou", default="")

