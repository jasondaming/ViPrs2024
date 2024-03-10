import wpilib
import wpilib.drive
import commands2
import rev
import constants
from team254.SparkMaxFactory import SparkMaxFactory
from team254.LazySparkMax import LazySparkMax
 
class IntakeSubsystem(commands2.Subsystem):
    class Cache:
        def __init__(self):
            self.setpoint = 0.0
            self.currentAmps = 0.0
            self.encoderValue = 0.0
            self.sensorValue = False
            self.currentSpeed = 0.0

    def __init__(self):
        super().__init__()
        self.cache = self.Cache()

        self.intake = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.intakeSpark)
        self.intake.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)

        self.intakeEncoder = self.intake.getEncoder() 
        
        self.noteSensor = wpilib.DigitalInput(constants.sensorConsts.noteSensorDIO) 

    def getIntakeSpeed(self):
        # return self.intake.get()
        return self.cache.currentSpeed

    def setIntakeSpeed(self, speed):
        # self.intake.set(rev.CANSparkLowLevel.ControlType.kDutyCycle, speed)
        self.cache.setpoint = speed

    def getIntakeEncoder(self):
        # return self.intakeEncoder.getVelocity()
        return self.cache.encoderValue
    
    def hasGamePiece(self):
        # gamePieceStatus = not self.noteSensor.get() #assuming the sensor reutrns false when the note is present
        gamePieceStatus = self.cache.sensorValue
        # print(f"IntakeSubsystem.hasGamePiece() - {gamePieceStatus}")
        return gamePieceStatus
    
    def updateHardware(self):
        self.intake.set(self.cache.setpoint)

    def cacheSensors(self):
        # print(f"IntakeSubsystem.cacheSensors() self.sensorValue = {self.cache.sensorValue}")
        self.cache.currentAmps = self.intake.getOutputCurrent()
        self.cache.encoderValue = self.intakeEncoder.getVelocity()
        self.cache.currentSpeed = self.intake.get()
        self.cache.sensorValue = not self.noteSensor.get() #assuming the sensor reutrns false when the note is present

    def __str__(self):
        return f"IntakeSubsystem: Speed = {self.getIntakeSpeed()} | Encoder = {self.getIntakeEncoder()}"