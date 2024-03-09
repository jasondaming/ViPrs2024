from subSystems.intakeSubsystem import IntakeSubsystem
from commands2 import Command

class IntakeStartCmd(Command):
    def __init__(self, intakeSubsystem: IntakeSubsystem, speed: float):
        self.intake = intakeSubsystem
        self.intakeSpeed = speed

    def execute(self):
        self.intake.setIntakeSpeed(self.intakeSpeed)

    def isFinished(self):
        # This command should finish immediately to proceed to the next step
        return True