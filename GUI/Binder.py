from jpype import JClass, JOverride, java, JImplements
from zope.interface import implementer

from GUI.Interfaces.Binders import CSBinder, EBinder
from GUI.Interfaces.Recipients import RecipientConnectionResult, RecipientMessages


@JImplements("ru.NIKITOS_V.PyInterfaces.Recipient")
@implementer(CSBinder, EBinder)
class Binder:
    def __init__(
            self,
            entry_screen: RecipientConnectionResult,
            chat_screen: RecipientMessages,
            java_connect_driver: JClass
    ):
        self.__java_connect_driver = java_connect_driver

        self.__java_connect_driver.setBinder(self)

        self.__entry_screen = entry_screen
        self.__chat_screen = chat_screen

        self.__entry_screen.set_binder(self)
        self.__chat_screen.set_binder(self)

    def check_connection(self, ip: str, port: int) -> None:
        self.__java_connect_driver.checkConnection(
            java.lang.String(ip),
            java.lang.Integer(port)
        )

    def connect(self, ip: str, port: int, user_name: str) -> None:
        self.__java_connect_driver.connect(
            java.lang.String(ip),
            java.lang.Integer(port),
            java.lang.String(user_name)
        )

    @JOverride()
    def accept_check_connection_result(self, result: bool) -> None:
        self.__entry_screen.accept_check_connection_result(result)

    @JOverride()
    def accept_connection_result(self, result: bool) -> None:
        self.__entry_screen.accept_connection_result(result)

    def send_message(self, message: str) -> None:
        self.__java_connect_driver.sendMessage(java.lang.String(message))

    @JOverride()
    def accept_message(self, user_name: java.lang.String, message: java.lang.String) -> None:
        self.__chat_screen.accept_message(user_name, message)

    def get_chat_history(self) -> None:
        self.__java_connect_driver.getChatHistory()

    @JOverride()
    def log_out_of_chat(self) -> None:
        self.__chat_screen.log_out_of_chat()

    def disconnect(self):
        self.__java_connect_driver.closeConnection()
