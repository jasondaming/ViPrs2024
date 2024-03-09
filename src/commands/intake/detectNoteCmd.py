from subSystems.intakeSubsystem import IntakeSubsystem
from commands2 import Command


class DetectNoteCommand(Command):
    def __init__(self, intakeSubsystem: IntakeSubsystem):
        self.intake = intakeSubsystem

    def execute(self):
        # This command might not need to do anything if it's just waiting for a sensor check
        pass

    def isFinished(self):
        # Return true when the note is detected
        return self.intake.hasGamePiece()
