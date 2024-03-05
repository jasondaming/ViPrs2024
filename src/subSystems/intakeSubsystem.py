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
        
        self.noteSensor = wpilib.DigitalInput(2) # change channel later

    def __str__(self):
        print("IntakeSubsystem: ")