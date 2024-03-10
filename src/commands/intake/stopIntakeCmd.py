from subSystems.intakeSubsystem import IntakeSubsystem
from commands2 import Command

class StopIntakeCmd(Command):
    def __init__(self, intakeSubsystem: IntakeSubsystem):
        self.intake = intakeSubsystem

    def execute(self):
        self.intake.setIntakeSpeed(0.0)

    def isFinished(self):
        # This command should finish immediately to proceed to the next step
        return True