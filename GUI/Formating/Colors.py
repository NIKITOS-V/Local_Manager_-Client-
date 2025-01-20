from typing import Final

from GUI.Formating.Objectless import Objectless
from GUI.Formating.Palette import Palette


class Colors(Objectless):
    bg_color: Final[list[float]] = Palette.get_color(20, 20, 20, 255)

    text_input_bg_color: Final[list[float]] = Palette.get_color(55, 55, 55, 255)
    text_color: Final[list[float]] = Palette.get_color(255, 255, 255, 255)

    button_down_bg_color: Final[list[float]] = Palette.get_color(70, 70, 70, 255)
    button_normal_bg_color: Final[list[float]] = Palette.get_color(40, 40, 40, 255)
