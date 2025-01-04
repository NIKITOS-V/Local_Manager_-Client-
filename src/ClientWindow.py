from kivy.app import App

from src.ScreenController import ScreenController


class ClientWindow(App):
    def __init__(self, connect_driver, **kwargs):
        super().__init__(**kwargs)

        self.connect_driver = connect_driver

    def build(self):
        screen_controller = ScreenController(self.connect_driver)

        screen_controller.open_entry_screen()

        return screen_controller
