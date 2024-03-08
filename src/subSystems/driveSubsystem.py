import wpilib
import wpilib.drive
import commands2
import phoenix5

class DriveSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.leftFront = phoenix5.WPI_TalonSRX(4)
        self.leftBack = phoenix5.WPI_TalonSRX(3)
        self.rightFront = phoenix5.WPI_TalonSRX(1)
        self.rightBack = phoenix5.WPI_TalonSRX(2)

        self.leftFront.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.leftBack.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.rightFront.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.rightBack.setNeutralMode(phoenix5.NeutralMode.Brake)

        self.leftDrive = wpilib.MotorControllerGroup(self.leftFront, self.leftBack)
        self.rightDrive = wpilib.MotorControllerGroup(self.rightFront, self.rightBack)
        
        # self.spark1 = rev.CANSparkMax(5, rev._rev.CANSparkLowLevel.MotorType.kBrushless)
        # self.drive1 = wpilib.drive.RobotDriveBase
        self.robotDrive = wpilib.drive.DifferentialDrive(
            self.leftDrive, self.rightDrive
        )
        self.rightDrive.setInverted(True)

    def arcadeDrive(self, forward, rotation):
        self.robotDrive.arcadeDrive(forward, rotation)