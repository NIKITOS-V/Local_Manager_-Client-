from jpype import JImplements, JClass, java, JOverride

from src.Screens.Interfaces.RecipientConnectionResult import RecipientConnectionResult


@JImplements("Interfaces.RecipientConnectionResult")
class ESBinder:
    def __init__(self, screen: RecipientConnectionResult, java_connect_driver: JClass):
        self.__java_connect_driver: JClass = java_connect_driver
        self.__screen = screen

        self.__java_connect_driver.setESBinder(self)

    def check_connection(self, ip: str, port: int):
        self.__java_connect_driver.checkConnection(
            java.lang.String(ip),
            java.lang.Integer(port)
        )

    def connect(self, ip: str, port: int, user_name: str):
        self.__java_connect_driver.connect(
            java.lang.String(ip),
            java.lang.Integer(port),
            java.lang.String(user_name)
        )

    @JOverride()
    def accept_check_connection_result(self, result: java.lang.Boolean):
        self.__screen.accept_check_connection_result(result)

    @JOverride()
    def accept_connection_result(self, result: java.lang.Boolean):
        self.__screen.accept_connection_result(result)
