import wpilib
import wpilib.drive
import commands2
import rev
import constants
 
class IntakeSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.intake = rev.CANSparkMax(constants.CANIDs.intakeSpark, rev.CANSparkMax.MotorType.kBrushless)
        self.intake.IdleMode(rev.CANSparkBase.IdleMode.kBrake)

        self.intakeEncoder = self.intake.getEncoder() 
        
        self.noteSensor = wpilib.DigitalInput(constants.sensorConsts.noteSensorDIO) # change channel later

    def getIntakeSpeed(self):
        return self.intake.get()

    def setIntakeSpeed(self, speed):
        self.intake.set(speed)

    def getIntakeEncoder(self):
        return self.intakeEncoder.getVelocity()

    def __str__(self):
        return f"IntakeSubsystem: Speed = {self.getIntakeSpeed()} | Encoder = {self.getIntakeEncoder()}"