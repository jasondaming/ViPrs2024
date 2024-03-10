import commands2

from subSystems.shooterSubsystem import ShooterSubsystem
import constants

class StopShooterCmd(commands2.Command):
    def __init__(self, shooter: ShooterSubsystem):
        self.shooter = shooter
        self.addRequirements(self.shooter)
    
    def execute(self):
        self.shooter.setShooterSpeed(0.0)

    def isFinished(self):
        # This command should finish immediately to proceed to the next step
        return True