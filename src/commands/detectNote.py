from subSystems.armSubsystem import ArmSubsystem
import commands2

class DetectNote(commands2.Command):
    def __init__(self, arm: ArmSubsystem):
        self.arm = arm

    def execute(self):
        # wait for sensor
        pass

    def isFinished(self) -> bool:
        return self.arm.isNoteLoaded()
