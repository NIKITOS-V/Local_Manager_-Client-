from jpype import java
from zope.interface import Interface


class RecipientConnectionResult(Interface):
    def accept_check_connection_result(self, result: bool): pass
    def accept_connection_result(self, result: bool): pass
