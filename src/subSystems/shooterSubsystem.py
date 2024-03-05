import wpilib
import wpilib.drive
import commands2
import rev
import constants
 
class ShooterSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.topShooter = rev.CANSparkMax(constants.CANIDs.topShootintSpark, rev.CANSparkMax.MotorType.kBrushless)
        self.bottomShooter = rev.CANSparkMax(constants.CANIDs.bottomShootingSpark, rev.CANSparkMax.MotorType.kBrushless)
        self.shooters = wpilib.MotorControllerGroup(self.topShooter, self.bottomShooter)

        self.topShooter.IdleMode(rev.CANSparkBase.IdleMode.kCoast)
        self.bottomShooter.IdleMode(rev.CANSparkBase.IdleMode.kCoast)

        self.topShooterEncoder = self.topShooter.getEncoder()
        self.bottomShooterEncoder = self.bottomShooter.getEncoder()


    def idleShooter(self):
        self.topShooter.set(0.0)
        self.bottomShooter.set(0.0)

    def __str__(self):
        print("ShooterSubsystem: ")