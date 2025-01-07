from jpype import java
from zope.interface import Interface


class RecipientMessages(Interface):
    def accept_message(self, user_name: java.lang.String, message: java.lang.String) -> None: pass

    def log_out_of_chat(self) -> None: pass
