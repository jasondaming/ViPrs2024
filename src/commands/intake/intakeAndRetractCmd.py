from commands2 import Command
from subSystems.intakeSubsystem import IntakeSubsystem
from constants import intakeConsts

class IntakeAndRetractCommand(Command):
    def __init__(self, intake: IntakeSubsystem, retractSpeed: float, retractTime: float):
        super().__init__()
        self.intake = intake
        self.retractSpeed = retractSpeed
        self.retractTime = retractTime
        self.hasGamePieceDetected = False
        self.addRequirements(intake)

    def initialize(self):
        # self.intake.setIntakeSpeed(intakeConsts.captureSpeed)  # Start intake
        self.hasGamePieceDetected = False

    def execute(self):
        hasGamePiece = self.intake.hasGamePiece()
        print(f"IntakeAndRetractCommand.execute() - {hasGamePiece}")
        if hasGamePiece:
            self.hasGamePieceDetected = True
            self.intake.setIntakeSpeed(self.retractSpeed)  # Start retracting

    def end(self, interrupted: bool):
        self.intake.setIntakeSpeed(0)  # Stop the intake motor

    def isFinished(self):
        # You could either finish after retracting for a certain time or immediately stop after detection
        # Here we're simply using the detection flag, but consider adding a timer for retracting
        return self.hasGamePieceDetected
