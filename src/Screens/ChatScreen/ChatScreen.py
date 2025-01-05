from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from jpype import JClass, java
from zope.interface import implementer

from src.Formating.Palette import Palette
from src.Screens.CommonSettings import CommonSettings
from src.Screens.Interfaces.RecipientMessages import RecipientMessages
from src.Screens.ChatScreen.CSBinder import CSBinder


Builder.load_file("Resources/ChatScreenView.kv")


class MessagesPanel(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.readonly = True
        self.multiline = True

        self.bg_color = Palette.get_color(60, 60, 60, 255)
        self.fg_color = CommonSettings.text_color

    def add_text(self, user_name: java.lang.String, message: java.lang.String) -> None:
        self.text += f"{user_name}: {message}\n"

    def clear_panel(self) -> None:
        self.text = ""


class SendMessageButton(Button, RelativeLayout):
    bg_normal_color = ListProperty([1, 1, 1, 1])
    bg_active_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_normal_color = CommonSettings.button_normal_color
        self.bg_active_color = CommonSettings.button_active_color

        self.__image = Image(
            source="Resources\\send_button_icon.png",
            size=self.size,
            pos=self.pos
        )

        self.add_widget(self.__image)

    def on_size(self, *args):
        self.__image.size = self.size
        self.width = self.height


@implementer(RecipientMessages)
class ChatScreen(Screen):
    bg_color = ListProperty([1, 1, 1, 1])

    text_color = ListProperty([1, 1, 1, 1])
    text_size = NumericProperty(22)

    message_input_color = ListProperty([1, 1, 1, 1])

    def __init__(self, screen_name: str, connect_driver: JClass, **kwargs):
        super().__init__(**kwargs)

        self.name = screen_name

        self.__csBinder = CSBinder(self, connect_driver)

        self.bg_color = CommonSettings.background_color
        self.text_color = CommonSettings.text_color
        self.message_input_color = CommonSettings.text_input_bg_color

    @mainthread
    def log_out_of_chat(self) -> None:
        self.manager.open_entry_screen()
        self.ids.messages_panel.clear_panel()

    @mainthread
    def accept_message(self, user_name: java.lang.String, message: java.lang.String) -> None:
        self.ids.messages_panel.add_text(user_name, message)

    @mainthread
    def send_message(self, message: str, *args) -> None:
        self.__csBinder.send_message(message)

    def on_pre_enter(self, *args):
        self.__csBinder.get_chat_history()