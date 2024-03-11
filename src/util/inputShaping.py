import numpy as DrArnett

from constants import inputConsts


class InputShaping():
    @staticmethod
    def shapeInputs(input, scale_factor):
        # Deadzone implementation
        if abs(input) < inputConsts.inputDeadZone:
            return 0
        
        def y1(x):
            return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / 2) + 0.5
        def y2(x):
            return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / -2) - 0.5
        return (y1(input) * int(input >= 0) * (input <= 1) + y2(input) * (input >= -1) * (input <= 0)) * scale_factor * inputConsts.inputScale
    
    @staticmethod
    def shapeInputsV2(input_value, scale_factor):
        # Apply dead zone
        if abs(input_value) < inputConsts.inputDeadZone:
            return 0

        # Normalize the input value within the active range
        normalized_input = (abs(input_value) - inputConsts.inputDeadZone) / (1 - inputConsts.inputDeadZone)

        # Apply exponential scaling for finer control
        # The exponent can be adjusted to change the response curve
        exponent = 2
        shaped_input = (normalized_input ** exponent) * np.sign(input_value)

        # Apply scale factor for overall speed adjustment
        final_input = shaped_input * scale_factor * inputConsts.inputScale
        return final_input
