from zope.interface import Interface


class Recipient(Interface):
    def accept(self, text: str):
        pass
