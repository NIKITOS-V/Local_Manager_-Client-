from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from jpype import JClass, JOverride, java
from zope.interface import Interface, implementer

from src.Formating.Palette import Palette
from src.Screens.CommonSettings import CommonSettings
from src.Screens.Interfaces.Recipient import Recipient


Builder.load_file("src\\Screens\\ChatScreenView.kv")


class MessagesPanel(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.readonly = True
        self.multiline = True

        self.bg_color = Palette.get_color(60, 60, 60, 255)
        self.fg_color = CommonSettings.text_color

    def add_text(self, text: str) -> None:
        text: list[str] = text.split("\n", 1)

        self.text += f"\n{text[0]}: {text[1]}"


class SendMessageButton(Button, RelativeLayout):
    bg_normal_color = ListProperty([1, 1, 1, 1])
    bg_active_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_normal_color = CommonSettings.button_normal_color
        self.bg_active_color = CommonSettings.button_active_color

        self.__image = Image(
            source="src\\Resources\\send_button_icon.png",
            size=self.size,
            pos=self.pos
        )

        self.add_widget(self.__image)

    def on_size(self, *args):
        self.__image.size = self.size
        self.width = self.height


class MessageInput(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = CommonSettings.text_input_bg_color
        self.fg_color = CommonSettings.text_color


class CSBinder:
    def __init__(self, screen: Recipient, java_class: JClass):
        self.__screen: Recipient = screen
        self.__java_class: JClass = java_class

        #self.__java_class.setBinder(self)

    def send_message(self, message: str):
        JClass.sendMessage(java.lang.String(message))

    def accept(self, text: str):
        self.__screen.accept(text)


@implementer(Recipient)
class ChatScreen(Screen):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, name: str, connect_driver: JClass, **kwargs):
        super().__init__(**kwargs)

        self.name = name

        self.__csBinder = CSBinder(self, connect_driver)

        self.bg_color = CommonSettings.background_color

    def accept(self, text: str):
        self.ids.messages_panel.add_text(text)

    def send_message(self, message: str, *args):
        self.__csBinder.send_message(message)

