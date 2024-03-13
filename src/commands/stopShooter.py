import commands2
from subSystems.armSubsystem import ArmSubsystem

class StopShooter(commands2.Command):
    def __init__(self, arm: ArmSubsystem):
        super().__init__()
        self.arm = arm

    def initialize(self):
        print("stop the motors")
        self.arm.disableShooter()

    def isFinished(self):
        return False