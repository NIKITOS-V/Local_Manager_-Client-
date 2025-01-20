from kivy.uix.textinput import TextInput


class CTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_active = ""
        self.background_normal = ""
