from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt
console = Console()

class MainView:
    def display_menu(self):





            title = Text(


            """

                          ███████╗██████╗ ██╗   ██╗██╗███╗   ██╗███████╗██╗ ██████╗ ██╗  ██╗████████╗
                          ██╔════╝██╔══██╗██║   ██║██║████╗  ██║██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝
                        █████╗  ██║  ██║██║   ██║██║██╔██╗ ██║███████╗██║██║  ███╗███████║   ██║
                        ██╔══╝  ██║  ██║██║   ██║██║██║╚██╗██║╚════██║██║██║   ██║██╔══██║   ██║
                        ███████╗██████╔╝╚██████╔╝██║██║ ╚████║███████║██║╚██████╔╝██║  ██║   ██║
                        ╚══════╝╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝

"""









                  , justify="center", style="bold cyan")
            subtitle = Text(
                  "Smart Education Management System",
                  justify="center",
                  style="italic green"
            )
            menu =""" 
1. Students
2. Teacher
3. Courses
4. Exercises
5. Grades
6. Submissions
7. Notifications
0. Exit
"""
            console.clear()   
            console.print(Align.center(title))
            console.print(Align.center(subtitle))
            console.print()

            console.print(
                 Align.center(
                      Panel.fit(
                           menu,
                           title="[bold cyan]Main Menu[/bold cyan]",
                           border_style="cyan",
                           
                      )
                 )
            )
            choice = Prompt.ask(
                  "[bold yellow]Choose an option[/bold yellow]"
                  )
            return choice