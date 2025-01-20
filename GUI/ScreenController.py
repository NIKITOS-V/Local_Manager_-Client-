from enum import Enum

from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen


class Direction(str, Enum):
    right = "right"
    left = "left"


class ScreenName(str, Enum):
    chat_screen = "chat_screen"
    entry_screen = "entry_screen"


class ScreenController(ScreenManager):
    def __init__(
            self,
            entry_screen: Screen,
            chat_screen: Screen,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.add_widget(entry_screen)
        self.add_widget(chat_screen)

        self.transition = SlideTransition(duration=0.5)

    def open_chat_screen(self):
        self.transition.direction = Direction.left
        self.current = ScreenName.chat_screen

    def open_entry_screen(self):
        self.transition.direction = Direction.right
        self.current = ScreenName.entry_screen
