import wpilib
import commands2
import commands2.cmd

from subSystems.intakeSubsystem import IntakeSubsystem

import constants

class IntakeCollectNoteCmd(commands2.Command):
    def __init__(self, intake: IntakeSubsystem, targetSpeed: float):
        #print(f"IntakeCollectNoteCmd.__init__({intake}, {targetSpeed})")
        super().__init__()
        self.intake = intake
        self.targetSpeed = targetSpeed
        self.addRequirements(self.intake)

    def execute(self):
        #print("IntakeCollectNoteCmd.execute()")
        self.intake.setIntakeSpeed(self.targetSpeed)

    def isFinished(self):
        #print("IntakeCollectNoteCmd.isFinsihed()")
        # Assume hasGamePiece() returns True when the note is detected
        return self.intake.hasGamePiece()

    def end(self, interrupted):
        #print(f"IntakeCollectNoteCmd.end({interrupted})")
        # Optionally, stop the intake here or leave it for the retract command
        self.intake.setIntakeSpeed(0)
