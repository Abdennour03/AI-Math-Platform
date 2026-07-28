from rich.panel import Panel
from rich import print
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.prompt import IntPrompt
from rich.console import Group
from dashboard import show_dashboard


console = Console()
title = Text("EDUINSIGHT AI", style="bold magenta", justify="center")

header_content = Group(
    title,
    "\n",
    Align.center(Text("Student Performance Analysis", style="italic cyan"))
)
text_list = Text.assemble(
    ("1. Dashboard\n"),
    ("2. Students\n"),
    ("3. Courses\n"),
    ("4. Exercices\n"),
    ("5. Analytics\n"),
    ("6. Exit\n")
)
app_panel = Panel(Align.center(header_content),
                expand = False,
                padding=(1, 4),
                width=60)

panel_list = Panel(
    text_list,
    title="[bold]list of Choice",
    expand=False,
    padding=(1, 4),
    width=60
)
ui_group = Group(
    Align.center(app_panel),
    "\n",
    Align.center(panel_list)

)
console.print(ui_group)
def main():
    while True:
        console.clear()
        choice = IntPrompt.ask("\n[bold]Choice", choices=[str(i) for i in range(1, 7)])
        if choice == 1:
            console.print("[green]Opening Dashboard...[/green]")
            show_dashboard(console)
            console.input("\n[dim]Press Enter to continue...")

        elif choice ==2:
            console.print("[green]Opening Student...[/green]")
            console.input("\n[dim]Press Enter to continue...")

        elif choice ==3:
            console.print("[green]Opening Courses...[/green]")
            console.input("\n[dim]Press Enter to continue...")

        elif choice ==4:
            console.print("[green]Opening Exercices...[/green]")
            console.input("\n[dim]Press Enter to continue...")

        elif choice ==5:
            console.print("[green]Opening Analytics...[/green]")
            console.input("\n[dim]Press Enter to continue...")

        elif choice ==6:
            console.print("[green]Exiting...[/green]")
        console.input("\n[dim]Press Enter to continue...")

if __name__ == "__main__":
    main()

                      