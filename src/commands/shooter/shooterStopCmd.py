import commands2

from subSystems.shooterSubsystem import ShooterSubsystem
from subSystems.intakeSubsystem import IntakeSubsystem
import constants

class ShooterStopCmd(commands2.Command):
    def __init__(self, shooter: ShooterSubsystem, intake: IntakeSubsystem):
        super().__init__()
        self.shooter = shooter
        self.intake = intake
        self.addRequirements(self.shooter, self.intake)
        
    def initialize(self):
        # Stop both the shooter and the intake
        self.shooter.idleShooter()
        self.intake.setIntakeSpeed(constants.intakeConsts.offSpeed)
    
    def isFinished(self):
        return True
