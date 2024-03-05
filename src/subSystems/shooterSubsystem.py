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

    def setShooterSpeed(self, topSpeed, bottomSpeed):
        self.topShooter.set(topSpeed)
        self.bottomShooter.set(bottomSpeed)

    def getShooterSpeeds(self):
        return self.topShooter.get(), self.bottomShooter.get()

    def getEncoderValues(self):
        return self.topShooterEncoder.getVelocity(), self.bottomShooterEncoder.getVelocity()

    def __str__(self):
        return f"ShooterSubsystem: speed = {self.getShooterSpeeds()} | encoders = {self.getEncoderValues()}"