import wpilib
import wpilib.drive
import commands2
import rev
import constants
from team254.SparkMaxFactory import SparkMaxFactory
from team254.LazySparkMax import LazySparkMax
 
class IntakeSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        # self.intake = rev.CANSparkMax(constants.CANIDs.intakeSpark, rev.CANSparkMax.MotorType.kBrushless)
        # self.intake.IdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.intake = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.intakeSpark)
        self.intake.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)

        self.intakeEncoder = self.intake.getEncoder() 
        
        self.noteSensor = wpilib.DigitalInput(constants.sensorConsts.noteSensorDIO) # change channel later

    def getIntakeSpeed(self):
        return self.intake.get()

    def setIntakeSpeed(self, speed):
        self.intake.set(rev.CANSparkLowLevel.ControlType.kDutyCycle, speed)

    def getIntakeEncoder(self):
        return self.intakeEncoder.getVelocity()
    
    def hasGamePiece(self):
        return not self.noteSensor.get() #assuming the sensor reutrns false when the note is present

    def __str__(self):
        return f"IntakeSubsystem: Speed = {self.getIntakeSpeed()} | Encoder = {self.getIntakeEncoder()}"