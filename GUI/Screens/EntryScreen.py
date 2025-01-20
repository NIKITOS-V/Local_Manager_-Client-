from kivy.clock import mainthread
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from GUI.Formating.Errors import IpError, UserNameError
from GUI.Interfaces.Binders import EBinder
from GUI.Formating.Colors import Colors
from GUI.Widgets.Layouts import ARLayout
from GUI.Widgets.TextInputs import CTextInput


class EntryScreen(Screen):
    text_color = ListProperty(Colors.text_color)
    text_size = NumericProperty(24)

    notifier_label_text = StringProperty("")

    bg_color = ListProperty(Colors.bg_color)

    text_input_bg_color = ListProperty(Colors.text_input_bg_color)

    button_normal_color = ListProperty(Colors.button_normal_bg_color)
    button_active_color = ListProperty(Colors.button_down_bg_color)

    def __init__(self, screen_name: str, **kwargs):
        super().__init__(**kwargs)

        self.__binder = None

        self.name = screen_name

    def set_binder(self, binder: EBinder) -> None:
        self.__binder = binder

    def __lock_inputs(self):
        self.ids.ip_input.readonly = True
        self.ids.port_input.readonly = True
        self.ids.user_name_input.readonly = True

        self.ids.check_connection_button.disabled = True
        self.ids.entry_button.disabled = True

        self.notifier_label_text = "Попытка подключения..."

    def __unlock_inputs(self):
        self.ids.ip_input.readonly = False
        self.ids.port_input.readonly = False
        self.ids.user_name_input.readonly = False

        self.ids.check_connection_button.disabled = False
        self.ids.entry_button.disabled = False

        self.notifier_label_text = ""

    def check_connection(self, ip: str, port_str: str, *args) -> None:
        try:
            if not self.__check_input(ip):
                raise IpError(message="Некорректный ip")

            port: int = int(port_str)

            self.__lock_inputs()

            self.__binder.check_connection(ip, port)

        except IpError as ie:
            self.__unlock_inputs()

            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. " + ie.message
            )

        except ValueError:
            self.__unlock_inputs()

            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. Некорректный порт"
            )

        except Exception:
            self.__unlock_inputs()

            self.__show_mini_window(
                "Результат подключения",
                "Не удалось"
            )

    @mainthread
    def accept_check_connection_result(self, result: bool) -> None:
        self.__show_mini_window(
            "Результат подключения",
            "Успешно" if result else "Не удалось"
        )

        self.__unlock_inputs()

    @mainthread
    def connect_to_server(self, ip: str, port_str: str, user_name: str, *args) -> None:
        try:
            if not self.__check_input(ip):
                raise IpError(message="Некорректный ip")

            port: int = int(port_str)

            if not self.__check_input(user_name):
                raise UserNameError("Некорректное имя пользователя")

            self.__lock_inputs()

            self.__binder.connect(ip, port, user_name)

        except UserNameError as une:
            self.__unlock_inputs()

            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. " + une.message
            )

        except IpError as ie:
            self.__unlock_inputs()

            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. " + ie.message
            )

        except ValueError:
            self.__unlock_inputs()

            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. Некорректный порт"
            )

    @mainthread
    def accept_connection_result(self, result: bool) -> None:
        if result:
            self.manager.open_chat_screen()

        else:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось"
            )

        self.__unlock_inputs()

    def __show_mini_window(self, title: str, text: str) -> None:
        layout = AnchorLayout()

        layout.add_widget(
            Label(
                font_size=24,
                color=Colors.text_color,
                text=text
            )
        )

        Popup(
            title=title,
            content=layout,
            size_hint=(None, None),
            size=(600, 200)
        ).open()

    def __check_input(self, text: str) -> bool:
        return text != ""
