import wpilib
import wpilib.drive
import commands2
import rev
import navx
import constants

 
class DriveSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.gyroAccl = navx.AHRS(wpilib.SPI.Port.kMXP)
        
        self.leftFront = rev.CANSparkMax(constants.CANIDs.leftDriveSparkFront, rev.CANSparkMax.MotorType.kBrushless)
        self.leftBack = rev.CANSparkMax(constants.CANIDs.leftDriveSparkBack, rev.CANSparkMax.MotorType.kBrushless)
        self.rightFront = rev.CANSparkMax(constants.CANIDs.rightDriveSparkFront, rev.CANSparkMax.MotorType.kBrushless)
        self.rightBack = rev.CANSparkMax(constants.CANIDs.rightDriveSparkBack, rev.CANSparkMax.MotorType.kBrushless)
        
        self.leftFront.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.leftBack.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.rightFront.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.rightBack.setIdleMode(rev.CANSparkBase.IdleMode.kBrake)

        self.leftDrive = wpilib.MotorControllerGroup(self.leftFront, self.leftBack)
        self.rightDrive = wpilib.MotorControllerGroup(self.rightFront, self.rightBack)
        
        # self.spark1 = rev.CANSparkMax(5, rev._rev.CANSparkLowLevel.MotorType.kBrushless)
        # self.drive1 = wpilib.drive.RobotDriveBase
        self.robotDrive = wpilib.drive.DifferentialDrive(
            self.leftDrive, self.rightDrive
        )
        self.rightDrive.setInverted(True)

        self.leftFrontEncoder = self.leftFront.getEncoder()

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the drive to drive more slowly.

        :param maxOutput: the maximum output to which the drive will be constrained
        """
        self.robotDrive.setMaxOutput = maxOutput

    def arcadeDriveSS(self, forward, rotation):
        self.robotDrive.arcadeDrive(forward, rotation)

    def updateHardware(self):
        pass

    

    
        
    