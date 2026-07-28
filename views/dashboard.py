from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.columns import Columns 
from rich.align import Align

console = Console()

def show_dashboard(console):
    table = Table(title="Dash info", box=None)


    table.add_column("Total Student", )
    table.add_column("Courses", "6")
    table.add_column("Exercises", "45")
    table.add_column("Average Grade", "14.8")


    table.add_row("40", "6", "45", "14.8")



    activity_text = Text.assemble(
        ("• Ahmed completed Exercise 5\n", "bold"),
        ("• Sara submitted Homework\n", "bold"),
        ("• New course created", "bold")
    )

    activity_panel = Panel(activity_text, 
                        title="[green]Recent Activity[/green]",
                        expand=False,
                        width=35)
    dashboard_columns = Columns([table, activity_panel])
    ui_dash = Align.center(dashboard_columns)
    console.print(ui_dash)
    