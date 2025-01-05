from jpype import JImplements, JClass, java, JOverride

from src.Screens.Interfaces.RecipientMessages import RecipientMessages


@JImplements("Interfaces.RecipientMessages")
class CSBinder:
    def __init__(self, screen: RecipientMessages, java_connect_driver: JClass):
        self.__screen: RecipientMessages = screen
        self.__java_connect_driver: JClass = java_connect_driver

        self.__java_connect_driver.setCSBinder(self)

    def send_message(self, message: str) -> None:
        self.__java_connect_driver.sendMessage(java.lang.String(message))

    @JOverride()
    def accept_message(self, user_name: java.lang.String, message: java.lang.String) -> None:
        self.__screen.accept_message(user_name, message)

    def get_chat_history(self) -> None:
        self.__java_connect_driver.getChatHistory()

    @JOverride()
    def log_out_of_chat(self) -> None:
        self.__screen.log_out_of_chat()