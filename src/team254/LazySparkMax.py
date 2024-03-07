from rev import CANSparkMax

"""
This class is a thin wrapper around the CANTalon that reduces CAN bus / CPU
overhead by skipping duplicate set commands.
"""

class LazySparkMax(CANSparkMax):
    def __init__(self, device_number: int):
        super().__init__(device_number, CANSparkMax.MotorType.kBrushless)
        self.m_last_set = float('nan')
        self.m_last_control_type = None
        self.m_leader = None

    @property
    def leader(self):
        return self.m_leader

    def follow(self, leader: CANSparkMax):
        self.m_leader = leader
        return super().follow(leader)

    def set(self, type: CANSparkMax.ControlType, setpoint: float):
        if setpoint != self.m_last_set or type != self.m_last_control_type:
            self.m_last_set = setpoint
            self.m_last_control_type = type
            super().getPIDController().setReference(setpoint, type)
