from zope.interface import Interface


class CSBinder(Interface):
    pass


class EBinder(Interface):
    def check_connection(self, ip: str, port: int) -> None: pass

    def connect(self, ip: str, port: int, user_name: str) -> None: pass
