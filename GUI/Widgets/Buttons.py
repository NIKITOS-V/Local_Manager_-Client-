from enum import Enum
from typing import Final

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.graphics import RenderContext
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from GUI.Formating.Colors import Colors
from GUI.Formating.Palette import Palette


class State(str, Enum):
    normal = "normal"
    down = "down"


class CButton(Button):
    bg_normal = ListProperty(Colors.button_normal_bg_color)
    bg_down = ListProperty(Colors.button_down_bg_color)

    def __init__(self, **kwargs):
        self.background_normal = ""
        self.background_down = ""

        self.background_color = self.bg_normal

        super().__init__(**kwargs)

    def on_state(self, instance, state):
        if state == State.normal:
            self.background_color = self.bg_normal
            self.do_on_state_normal()

        else:
            self.background_color = self.bg_down
            self.do_on_state_down()

    def on_bg_normal(self, instance, color):
        if self.state == State.normal:
            self.background_color = color

    def on_bg_down(self, instance, color):
        if self.state == State.down:
            self.background_color = color

    def do_on_state_normal(self):
        pass

    def do_on_state_down(self):
        pass


class IconButton(ButtonBehavior, RelativeLayout):
    SHADER_SOURCE: Final[str] = "Resources/GLSL/Shader.glsl"

    bg_normal = ListProperty(Colors.button_normal_bg_color)
    bg_down = ListProperty(Colors.button_down_bg_color)

    source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__image = None

        self.bg_color = self.bg_normal

        self.__init__shader()
        self.__init_image()
        self.__start_shader()

    def __init__shader(self):
        EventLoop.ensure_window()

        self.canvas = RenderContext(
            use_parent_projection=True,
            use_parent_modelview=True
        )

        self.canvas.shader.source = self.SHADER_SOURCE

    def __init_image(self):
        self.__image = Image(
            fit_mode="contain",
            source=self.source
        )

        self.add_widget(
            self.__image
        )

    def __start_shader(self):
        Clock.schedule_interval(self.provide_color, 0)

    def provide_color(self, *dt):
        self.canvas["bg_color"] = tuple(self.bg_color)

    def on_size(self, instance, size):
        self.__image.size = size

    def on_state(self, instance, state):
        if state == State.normal:
            self.bg_color = self.bg_normal
            self.do_on_state_normal()

        else:
            self.bg_color = self.bg_down
            self.do_on_state_down()

    def on_source(self, instance, path):
        self.__image.source = path

    def on_bg_normal(self, instance, color):
        if self.state == State.normal:
            self.bg_color = color

    def on_bg_down(self, instance, color):
        if self.state == State.down:
            self.bg_color = color

    def do_on_state_normal(self):
        pass

    def do_on_state_down(self):
        pass
