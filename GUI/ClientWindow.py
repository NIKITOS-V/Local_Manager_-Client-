from jpype import JClass
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.relativelayout import RelativeLayout

from GUI.Binder import Binder
from GUI.ScreenController import ScreenController, ScreenName
from GUI.Screens.ChatScreen import ChatScreen
from GUI.Formating.Colors import Colors
from GUI.Screens.EntryScreen import EntryScreen

Builder.load_file("Resources/KV/BackgroundView.kv")
Builder.load_file("Resources/KV/ChatScreenView.kv")
Builder.load_file("Resources/KV/EntryScreenView.kv")


class Background(RelativeLayout):
    bg_color = ListProperty(Colors.bg_color)


class ClientWindow(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__binder = None

    def build(self):
        chat_screen = ChatScreen(
            ScreenName.chat_screen,
        )

        entry_screen = EntryScreen(
            ScreenName.entry_screen
        )

        self.__binder = Binder(
            entry_screen,
            chat_screen,
            JClass("ru.NIKITOS_V.Client")()
        )

        screen_controller = ScreenController(
            entry_screen,
            chat_screen
        )

        background = Background()

        background.add_widget(screen_controller)

        screen_controller.open_entry_screen()

        return background

    def on_stop(self):
        self.__binder.disconnect()
