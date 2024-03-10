import commands2

from subSystems.shooterSubsystem import ShooterSubsystem
import constants

class ShooterStartCmd(commands2.Command):
    def __init__(self, shooter: ShooterSubsystem):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(self.shooter)
        
    def initialize(self):
        # Start the shooter wheels at the desired speed
        self.shooter.setShooterSpeed(constants.shooterConsts.topShootHighSpeed, constants.shooterConsts.bottomShootHighSpeed)
    
    def isFinished(self):
        # This command continues until interrupted
        return False

    def end(self, interrupted):
        # Optionally, stop the shooter here if you want immediate response
        # Otherwise, you can rely on ShooterStopCommand to stop the shooter
        pass
