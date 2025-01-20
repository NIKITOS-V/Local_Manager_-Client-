from kivy.clock import mainthread
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen

from jpype import java
from zope.interface import implementer

from GUI.Formating.Palette import Palette
from GUI.Formating.Colors import Colors
from GUI.Interfaces.Recipients import RecipientMessages
from GUI.Interfaces.Binders import CSBinder
from GUI.Widgets.Buttons import CButton
from GUI.Widgets.TextInputs import CTextInput


class MessagesPanel(CTextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.readonly = True
        self.multiline = True

        self.bg_color = Palette.get_color(60, 60, 60, 255)
        self.fg_color = Colors.text_color

    def add_text(self, user_name: java.lang.String, message: java.lang.String) -> None:
        self.text += f"{user_name}: {message}\n"

    def clear_panel(self) -> None:
        self.text = ""


class SendMessageButton(Button, RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
    text_color = ListProperty(Colors.text_color)
    text_size = NumericProperty(22)

    message_input_color = ListProperty(Colors.text_input_bg_color)

    def __init__(
            self,
            screen_name: str,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.name = screen_name

        self.__binder = None

    def set_binder(self, binder: CSBinder) -> None:
        self.__binder = binder

    @mainthread
    def log_out_of_chat(self) -> None:
        self.manager.open_entry_screen()
        self.ids.messages_panel.clear_panel()

    @mainthread
    def accept_message(self, user_name: java.lang.String, message: java.lang.String) -> None:
        self.ids.messages_panel.add_text(user_name, message)

    @mainthread
    def send_message(self, message_input, *args) -> None:
        if message_input.text != "" and message_input.text.count(" ") != len(message_input.text):
            self.__binder.send_message(message_input.text)
            message_input.text = ""

    def disconnect(self) -> None:
        self.__binder.disconnect()

    def on_pre_enter(self, *args):
        self.__binder.get_chat_history()
