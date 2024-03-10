import wpilib
import commands2

from subSystems.intakeSubsystem import IntakeSubsystem
import constants

class IntakeExpelNoteCmd(commands2.Command):
    def __init__(self, intake: IntakeSubsystem, expelSpeed: float, delay: float):
        super().__init__()
        self.intake = intake
        self.expelSpeed = -1.0 * expelSpeed
        self.delay = delay  # Time delay in seconds
        self.addRequirements(self.intake)
        self.timer = wpilib.Timer()
        self.hasNoteBeenDetected = False

    def initialize(self):
        # Reset and start the timer
        self.timer.reset()
        self.timer.start()
        # Initially set the intake speed to expel the note
        self.intake.setIntakeSpeed(self.expelSpeed)
        self.hasNoteBeenDetected = False

    def execute(self):
        # Check if the note sensor reads false for the first time
        if not self.intake.hasGamePiece() and not self.hasNoteBeenDetected:
            self.hasNoteBeenDetected = True
            self.timer.reset()  # Reset the timer when the note is first detected as absent

    def isFinished(self):
        # If the note has been detected as absent and the delay time has passed, finish the command
        return self.hasNoteBeenDetected and self.timer.hasElapsed(self.delay)

    def end(self, interrupted):
        # Once the command is finished or interrupted, stop the intake
        self.intake.setIntakeSpeed(constants.intakeConsts.offSpeed)
        self.timer.stop()
