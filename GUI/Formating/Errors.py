class ColorError(Exception):
    def __init__(self, message: str = "Uncorrected rgb value", *args):
        self.message: str = message

    def __str__(self):
        return self.message


class InstantError(Exception):
    def __init__(self, message: str = "This class should not be instantiated", *args):
        self.message: str = message

    def __str__(self):
        return self.message


class ConnectError(Exception):
    def __init__(self, message: str = "Couldn't connect", *args):
        self.message: str = message

    def __str__(self):
        return self.message


class PortError(Exception):
    def __init__(self, message: str = "Uncorrected port", *args):
        self.message: str = message

    def __str__(self):
        return self.message


class IpError(Exception):
    def __init__(self, message: str = "Uncorrected ip", *args):
        self.message: str = message

    def __str__(self):
        return self.message


class UserNameError(Exception):
    def __init__(self, message: str = "Uncorrected user name", *args):
        self.message: str = message

    def __str__(self):
        return self.message
