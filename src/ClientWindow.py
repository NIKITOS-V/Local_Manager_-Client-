from kivy.app import App

from src.ScreenController import ScreenController


class ClientWindow(App):
    def __init__(self, java_connect_driver, **kwargs):
        super().__init__(**kwargs)

        self.__java_connect_driver = java_connect_driver

    def build(self):
        screen_controller = ScreenController(self.__java_connect_driver)

        screen_controller.open_entry_screen()

        return screen_controller

    def on_stop(self):
        self.__java_connect_driver.closeConnection()
