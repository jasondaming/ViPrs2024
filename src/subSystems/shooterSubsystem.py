import wpilib
import wpilib.drive
import commands2
import rev
import constants

from team254.SparkMaxFactory import SparkMaxFactory
from team254.LazySparkMax import LazySparkMax
 
class ShooterSubsystem(commands2.Subsystem):
    class Cache:
        def __init__(self):
            self.topMotorCurrent = 0.0
            self.bottomMotorCurrent = 0.0
            self.topSetpoint = 0.0
            self.bottomSetpoint = 0.0
            self.topEncoderValue = 0.0
            self.bottomEncoderValue = 0.0
            self.topCurrentSpeed = 0.0
            self.bottomCurrentSpeed = 0.0


    def __init__(self):
        super().__init__()
        self.cache = self.Cache()
        # self.topShooter = rev.CANSparkMax(constants.CANIDs.topShootintSpark, rev.CANSparkMax.MotorType.kBrushless)
        # self.bottomShooter = rev.CANSparkMax(constants.CANIDs.bottomShootingSpark, rev.CANSparkMax.MotorType.kBrushless)
        self.topShooter = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.topShootingSpark, False)
        self.bottomShooter = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.bottomShootingSpark, True)
        self.topShooter.setInverted(True)
        self.bottomShooter.setInverted(True)
        self.shooters = wpilib.MotorControllerGroup(self.topShooter, self.bottomShooter)

        self.topShooter.IdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.bottomShooter.IdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.topShooterEncoder = self.topShooter.getEncoder()
        self.bottomShooterEncoder = self.bottomShooter.getEncoder()


    def idleShooter(self):
        # self.topShooter.set(0.0)
        # self.bottomShooter.set(0.0)
        self.cache.topSetpoint = 0.0
        self.cache.bottomSetpoint = 0.0

    def setShooterSpeed(self, topSpeed, bottomSpeed):
        # self.topShooter.set(topSpeed)
        # self.bottomShooter.set(bottomSpeed)
        self.cache.topSetpoint = topSpeed
        self.cache.bottomSetpoint = bottomSpeed

    def getShooterSpeeds(self):
        # return self.topShooter.get(), self.bottomShooter.get()
        return self.cache.topCurrentSpeed, self.cache.bottomCurrentSpeed

    def getEncoderValues(self):
        # return self.topShooterEncoder.getVelocity(), self.bottomShooterEncoder.getVelocity()
        return self.cache.topEncoderValue, self.cache.bottomEncoderValue

    def updateHardware(self):
        self.topShooter.set(self.cache.topSetpoint, rev.CANSparkMaxLowLevel.ControlType.kDutyCycle)
        self.bottomShooter.set(self.cache.bottomSetpoint, rev.CANSparkMaxLowLevel.ControlType.kDutyCycle)

    def cacheSensors(self):
        self.cache.topMotorCurrent = self.topShooter.getOutputCurrent()
        self.cache.bottomMotorCurrent = self.bottomShooter.getOutputCurrent()
        self.cache.topEncoderValue = self.topShooterEncoder.getVelocity()
        self.cache.bottomEncoderValue = self.bottomShooterEncoder.getVelocity()
        self.cache.topCurrentSpeed = self.topShooter.get()
        self.cache.bottomCurrentSpeed = self.bottomShooter.get()

    def __str__(self):
        return f"ShooterSubsystem: speed = {self.getShooterSpeeds()} | encoders = {self.getEncoderValues()}"