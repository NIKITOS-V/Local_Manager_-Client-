from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from jpype import JClass, java

from src.Formating.Palette import Palette
from src.Screens.CommonSettings import CommonSettings

Builder.load_file("src\\Screens\\EntryScreenView.kv")


class PortInput(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = Palette.get_color(60, 60, 60, 255)
        self.fg_color = CommonSettings.text_color


class IpInput(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = Palette.get_color(60, 60, 60, 255)
        self.fg_color = CommonSettings.text_color


class UserNameInput(TextInput):
    bg_color = ListProperty([1, 1, 1, 1])
    fg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = Palette.get_color(60, 60, 60, 255)
        self.fg_color = CommonSettings.text_color


class CheckConnectionButton(Button):
    bg_normal_color = ListProperty([1, 1, 1, 1])
    bg_active_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_normal_color = Palette.get_color(40, 40, 40, 255)
        self.bg_active_color = CommonSettings.button_active_color


class ConnectButton(Button):
    bg_normal_color = ListProperty([1, 1, 1, 1])
    bg_active_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_normal_color = Palette.get_color(40, 40, 40, 255)
        self.bg_active_color = CommonSettings.button_active_color


class ESBinder:
    def __init__(self, java_class: JClass):
        self.__java_class: JClass = java_class

    def check_connection(self, ip: str, port: int) -> bool:
        return self.__java_class.checkConnection(
            java.lang.String(ip),
            java.lang.Integer(port)
        )


class EntryScreen(Screen):
    label_text_color = ListProperty([1, 1, 1, 1])
    label_text_size = NumericProperty(24)
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, name: str, connect_driver, **kwargs):
        super().__init__(**kwargs)

        self.esBinder = ESBinder(connect_driver)
        self.name = name

        self.bg_color = Palette.get_color(20, 20, 20, 255)
        self.label_text_color = CommonSettings.text_color

    def check_connection(self, ip: str, port_str: str, *args):
        try:
            port: int = int(port_str)

            self.__show_mini_window(
                "Результат проверки",
                "Успешно" if self.esBinder.check_connection(ip, port) else "Не удалось"
            )

        except ValueError:
            self.__show_mini_window(
                "Результат",
                "Не удалось"
            )

    def connect_to_server(self):
        pass

    def __show_mini_window(self, title:str, text: str):
        layout = AnchorLayout()

        layout.add_widget(
            Label(
                font_size=24,
                color=CommonSettings.text_color,
                text=text
            )
        )

        Popup(
            title=title,
            content=layout,
            size_hint=(None, None),
            size=(400, 200)
        ).open()
