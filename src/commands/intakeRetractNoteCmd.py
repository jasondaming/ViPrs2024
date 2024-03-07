import wpilib
import commands2
import commands2.cmd

from subSystems.intakeSubsystem import IntakeSubsystem

import constants

class IntakeRetractNoteCmd(commands2.CommandBase):
    def __init__(self, intake: IntakeSubsystem, retractSpeed: float, retractTime: float):
        super().__init__()
        self.intake = intake
        self.retractSpeed = retractSpeed  # This might be negative to reverse the intake
        self.retractTime = retractTime
        self.addRequirements([self.intake])
        self.initialTime = 0

    def initialize(self):
        self.initialTime = wpilib.Timer.getFPGATimestamp()

    def execute(self):
        self.intake.setIntakeSpeed(self.retractSpeed)

    def isFinished(self):
        # Stop after the specified retract time has passed
        return (wpilib.Timer.getFPGATimestamp() - self.initialTime) >= self.retractTime

    def end(self, interrupted):
        self.intake.setIntakeSpeed(0)
