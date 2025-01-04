from enum import Enum

from kivy.uix.screenmanager import ScreenManager, NoTransition

from src.Screens.ChatScreen import ChatScreen
from src.Screens.EntryScreen import EntryScreen


class Screens(str, Enum):
    chat_screen = "chat_screen"
    entry_screen = "entry_screen"


class ScreenController(ScreenManager):
    def __init__(self, connect_driver, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(
            EntryScreen(
                Screens.entry_screen,
                connect_driver
            )
        )

        self.add_widget(
            ChatScreen(
                Screens.chat_screen,
                connect_driver
            )
        )

        self.transition = NoTransition()

    def open_chat_screen(self):
        self.current = Screens.chat_screen

    def open_entry_screen(self):
        self.current = Screens.entry_screen
