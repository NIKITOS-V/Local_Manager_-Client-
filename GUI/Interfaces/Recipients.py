from jpype import java
from zope.interface import Interface

from GUI.Interfaces.Binders import EBinder, CSBinder


class RecipientConnectionResult(Interface):
    def accept_check_connection_result(self, result: bool) -> None: pass
    def accept_connection_result(self, result: bool) -> None: pass

    def set_binder(self, binder: EBinder) -> None: pass


class RecipientMessages(Interface):
    def accept_message(self, user_name: java.lang.String, message: java.lang.String) -> None: pass

    def log_out_of_chat(self) -> None: pass

    def set_binder(self, binder: CSBinder) -> None: pass
