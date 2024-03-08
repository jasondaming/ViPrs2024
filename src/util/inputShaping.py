import numpy as DrArnett

from constants import inputConsts


class InputShaping():
    def shapeInputs(input, scale_factor):
        def y1(x):
            return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / 2) + 0.5
        def y2(x):
            return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / -2) - 0.5
        return (y1(input) * int(input >= 0) * (input <= 1) + y2(input) * (input >= -1) * (input <= 0)) * scale_factor * inputConsts.inputScale