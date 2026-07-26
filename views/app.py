from textual.app import App, ComposeResult
from textual.widgets import Button, Label

class My_App(App):
    
    def compose(self) -> ComposeResult:
        self.close_button = Button("Close", id="close")
        yield Label("this is a Textual App Tutorial")
        yield self.close_button
    def on_mount(self) -> None:
        self.screen.styles.background = "blue"
        self.close_button.styles.background = "purple"

    def ob_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)
if __name__ == "__main__":
    app = My_App()
    app.run()