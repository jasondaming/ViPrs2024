import numpy as DrArnett

from constants import inputConsts


class InputShaping():
    last_input = 0.0  # Class variable to store the last input value for ramping

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
        print(f"inputShaping.shapeInputV2({input_value}, {scale_factor})")

        # Apply dead zone
        if abs(input_value) < inputConsts.inputDeadZone:
            return 0

        # Normalize the input value within the active range
        normalized_input = (abs(input_value) - inputConsts.inputDeadZone) / (1 - inputConsts.inputDeadZone)
        print(f"-- shapeInputV2 : normalized_input = {normalized_input}")

        # Apply exponential scaling for finer control
        # The exponent can be adjusted to change the response curve
        exponent = 2
        shaped_input = (normalized_input ** exponent) * np.sign(input_value)
        print(f"-- shapeInputV2 : shaped_input = {shaped_input}")

        # Apply scale factor for overall speed adjustment
        final_input = shaped_input * scale_factor * inputConsts.inputScale
        print(f"-- shapeInputV2 : final_input = {final_input}")

        return final_input
    
    @staticmethod
    def rampInput(current_input, ramp_rate):
        """
        Apply ramping to the input to smooth out transitions between different input levels.
        
        :param current_input: The current input value.
        :param ramp_rate: The maximum rate of change of the input per call.
        :return: The ramped input value.
        """
        print(f"inputShaping.rampInput({current_input}, {ramp_rate})")

        input_difference = current_input - InputShaping.last_input
        print(f"-- rampInput : input_difference = {input_difference}")

        # Clamp the change in input to the ramp rate
        if input_difference > ramp_rate:
            ramped_input = InputShaping.last_input + ramp_rate
        elif input_difference < -ramp_rate:
            ramped_input = InputShaping.last_input - ramp_rate
        else:
            ramped_input = current_input
        # Update the last input value
        InputShaping.last_input = ramped_input

        print(f"-- rampInputs : ramped_input = {ramped_input}")

        return ramped_input

    @staticmethod
    def shapeInputsV3(input_value, scale_factor):
        print(f"inputShaping.shapeInputsV3({input_value}, {scale_factor})")

        # Apply dead zone
        if abs(input_value) < inputConsts.inputDeadZone:
            input_value = 0
        else:
            input_value = np.sign(input_value) * ((abs(input_value) - inputConsts.inputDeadZone) / (1 - inputConsts.inputDeadZone))
        
        # Apply ramping to the input to smooth transitions
        ramped_input = InputShaping.rampInput(input_value, inputConsts.rampRate)
        print(f"-- shapeInputsV3 : ramped_input = {ramped_input}")
        
        # Apply scaling for overall speed adjustment
        final_input = ramped_input * scale_factor * inputConsts.inputScale
        

        return final_input
