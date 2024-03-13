from team4646.PID import PID

class SimplePIDController:
    def __init__(self, PIDValues: PID, deadband=0.0):
        self.PIDVals = PIDValues
        self.deadband = deadband
        self.setpoint = 0  # Desired setpoint
        self.integral = 0  # Integral term
        self.prev_error = 0  # Previous error
        self.ff = 0

    def set_setpoint(self, setpoint, ff):
        """
        Updates the desired setpoint.
        """
        self.setpoint = setpoint
        self.ff = ff
        self.reset()

    def reset(self):
        """
        Resets the integral term and previous error.
        This is useful when the controller starts controlling a new setpoint.
        """
        self.integral = 0
        self.prev_error = 0

    def update(self, current_value, dt, aff=0.0):
        """
        Calculates the control action for a new iteration.

        :param current_value: The current value of the process variable.
        :param dt: Time interval since the last update.
        :param aff: Arbitrary feed forward, dynamically updated
        :return: The control variable to be applied.
        """
        error = self.setpoint - current_value
        
        if abs(error) <= self.deadband:
            return 0
        
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0

        output = (self.PIDVals.P * error) + (self.PIDVals.I * self.integral) + (self.PIDVals.D * derivative) + aff

        self.prev_error = error

        # print(f"SPIDC.update({current_value}, {dt}, {aff}) - error: {error}, self.integral = {self.integral}, derivative = {derivative}, output = {output}")
        print(f"SPIDC.update cv:{current_value}, error:{error}")
        return output
