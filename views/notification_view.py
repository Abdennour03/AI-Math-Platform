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
1. Send notification
2. Get notification
3. Get All notifications
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
    def get_notification(self):
        try:
            notification_id = int(Prompt.ask("Notification ID.", default=""))
            notification = self.notification_controller.get_notification(
                notification_id
            )
            console.print(
                Panel.fit(
                f"""
ID : {notification.notification_id}
Title : {notification.title}
Message : {notification.message}
Teacher : {notification.teacher.full_name}
Created at : {notification.created_at}
""",
title="Notification",
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

    def get_all_notifications(self):
        try:
            notifications = (self.notification_controller.get_all_notifications())
            if not notifications:

                console.print(
                    "[bold red]No notifications found.[/]"
                )
                Prompt.ask(
                    "Press Enter to continue",
                    default=""
                )
                return
            tabel = Table(title="Notifications", border_style="cyan")
            tabel.add_column("ID")
            tabel.add_column('Title')
            tabel.add_column("Message")
            tabel.add_column("Teacher")
            tabel.add_column("Created At")

            for notification in notifications:
                tabel.add_row(
                str(notification.notification_id),
                notification.title,
                notification.message,
                notification.teacher.full_name,
                str(notification.created_at)
            )
            console.print(Align.center(tabel))
        except ValueError as error:
            console.print(
                f"[bold red]{error}[/]"
            )     
        Prompt.ask(
        "\nPress Enter to continue",
        default=""
    )

