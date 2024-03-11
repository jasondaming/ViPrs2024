import commands2

from subSystems.shooterSubsystem import ShooterSubsystem
from subSystems.intakeSubsystem import IntakeSubsystem
import constants

class ShooterStopCmd(commands2.Command):
    def __init__(self, shooter: ShooterSubsystem):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)
        
    def initialize(self):
        # Stop both the shooter and the intake
        self.shooter.idleShooter()
    
    def isFinished(self):
        return True
