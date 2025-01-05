from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen

from jpype import java

from src.Formating.Palette import Palette
from src.Formating.Errors import IpError, UserNameError
from src.Screens.CommonSettings import CommonSettings
from src.Screens.EntryScreen.ESBuilder import ESBinder


Builder.load_file("Resources/EntryScreenView.kv")


class ARLayout(RelativeLayout):
    ratio = NumericProperty(16 / 9)

    def do_layout(self, *args):
        for child in self.children:
            self.apply_ratio(child)
        super(ARLayout, self).do_layout()

    def apply_ratio(self, child):
        child.size_hint = None, None
        child.pos_hint = {"center_x": .5, "center_y": .5}

        w, h = self.size
        h2 = w * self.ratio
        if h2 > self.height:
            w = h / self.ratio
        else:
            h = h2
        child.size = w, h


class EntryScreen(Screen):
    text_color = ListProperty([1, 1, 1, 1])
    text_size = NumericProperty(24)

    notifier_label_text = StringProperty("")

    bg_color = ListProperty([1, 1, 1, 1])

    text_input_bg_color = ListProperty([1, 1, 1, 1])

    button_normal_color = ListProperty([1, 1, 1, 1])
    button_active_color = ListProperty([1, 1, 1, 1])

    def __init__(self, screen_name: str, connect_driver, **kwargs):
        super().__init__(**kwargs)

        self.esBinder = ESBinder(
            self,
            connect_driver
        )

        self.name = screen_name

        self.bg_color = Palette.get_color(20, 20, 20, 255)
        self.text_color = CommonSettings.text_color

        self.text_input_bg_color = Palette.get_color(60, 60, 60, 255)

        self.button_normal_color = Palette.get_color(40, 40, 40, 255)
        self.button_active_color = CommonSettings.button_active_color

    def __lock_inputs(self, ):
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

    def check_connection(self, ip: str, port_str: str, *args):
        try:
            if not self.__check_input(ip):
                raise IpError(message="Некорректный ip")

            port: int = int(port_str)

            self.__lock_inputs()

            self.esBinder.check_connection(ip, port)

        except IpError as ie:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. " + ie.message
            )

        except ValueError:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. Некорректный порт"
            )

        except Exception:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось"
            )

    @mainthread
    def accept_check_connection_result(self, result: java.lang.Boolean):
        self.__show_mini_window(
            "Результат подключения",
            "Успешно" if result else "Не удалось"
        )

        self.__unlock_inputs()

    @mainthread
    def connect_to_server(self, ip: str, port_str: str, user_name: str, *args):
        try:
            if not self.__check_input(ip):
                raise IpError(message="Некорректный ip")

            port: int = int(port_str)

            if not self.__check_input(user_name):
                raise UserNameError("Некорректное имя пользователя")

            self.__lock_inputs()

            self.esBinder.connect(ip, port, user_name)

        except UserNameError as une:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. " + une.message
            )

        except IpError as ie:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. " + ie.message
            )

        except ValueError:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось. Некорректный порт"
            )

    @mainthread
    def accept_connection_result(self, result: java.lang.Boolean):
        if result:
            self.manager.open_chat_screen()

        else:
            self.__show_mini_window(
                "Результат подключения",
                "Не удалось"
            )

        self.__unlock_inputs()

    def __show_mini_window(self, title: str, text: str):
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
            size=(600, 200)
        ).open()

    def __check_input(self, text: str) -> bool:
        return text != ""
