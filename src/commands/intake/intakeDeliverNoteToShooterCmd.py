import commands2
import wpilib

from subSystems.intakeSubsystem import IntakeSubsystem
import constants

class IntakeDeliverNoteToShooterCmd(commands2.Command):
    def __init__(self, intake: IntakeSubsystem, duration: float):
        super().__init__()
        self.intake = intake
        self.duration = duration
        self.addRequirements(self.intake)
        self.timer = wpilib.Timer()
        
    def initialize(self):
        # Start delivery to the shooter
        self.intake.setIntakeSpeed(constants.intakeConsts.deliverToShooterSpeed)
        self.timer.reset()
        self.timer.start()
    
    def isFinished(self):
        # Wait for the duration to deliver the note
        return self.timer.hasElapsed(self.duration)
    
    def end(self, interrupted):
        # Ensure everything is stopped
        self.intake.setIntakeSpeed(constants.intakeConsts.offSpeed)
