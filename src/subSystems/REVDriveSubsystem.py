import wpilib
import wpilib.drive
import commands2
import rev
import navx
import constants

from team254.SparkMaxFactory import SparkMaxFactory
from team254.LazySparkMax import LazySparkMax

 
class DriveSubsystem(commands2.Subsystem):
    class Cache:
        def __init__(self):
            self.forwardSetpoint = 0.0
            self.rotationSetpoint = 0.0
            self.gyroAngle = 0.0
            self.leftFrontCurrentAmp = 0.0
            self.leftBackCurrentAmp = 0.0
            self.rightFrontCurrentAmp = 0.0
            self.rightBackCurrentAmp = 0.0
            self.leftFrontEncoderValue = 0.0
            self.leftBackEncoderValue = 0.0
            self.rightFrontEncoderValue = 0.0
            self.rightBackEncoderValue = 0.0

    def __init__(self):
        super().__init__()

        self.cache = self.Cache()

        self.gyroAccl = navx.AHRS(wpilib.SPI.Port.kMXP)
        # TODO: initialize gyro here
        
        # self.leftFront = rev.CANSparkMax(constants.CANIDs.leftDriveSparkFront, rev.CANSparkMax.MotorType.kBrushless)
        # self.leftBack = rev.CANSparkMax(constants.CANIDs.leftDriveSparkBack, rev.CANSparkMax.MotorType.kBrushless)
        # self.rightFront = rev.CANSparkMax(constants.CANIDs.rightDriveSparkFront, rev.CANSparkMax.MotorType.kBrushless)
        # self.rightBack = rev.CANSparkMax(constants.CANIDs.rightDriveSparkBack, rev.CANSparkMax.MotorType.kBrushless)

        self.leftFront = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.leftDriveSparkFront)
        self.leftBack = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.leftDriveSparkBack)
        self.rightFront = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.rightDriveSparkFront)
        self.rightBack = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.rightDriveSparkBack)
        
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
        self.leftBackEncoder = self.leftBack.getEncoder()
        self.rightFrontEncoder = self.rightFront.getEncoder()
        self.rigthBackEncoder = self.rightBack.getEncoder()


    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the drive to drive more slowly.

        :param maxOutput: the maximum output to which the drive will be constrained
        """
        self.robotDrive.setMaxOutput = maxOutput

    def arcadeDriveSS(self, forward, rotation):
        # self.robotDrive.arcadeDrive(forward, rotation)
        self.cache.forwardSetpoint = forward
        self.cache.rotationSetpoint = rotation

    def updateHardware(self):
        self.robotDrive.arcadeDrive(self.cache.forwardSetpoint, self.cache.rotationSetpoint)

    def cacheSensors(self):
        self.gyroAngle = self.gyroAccl.getAngle()
        self.leftFrontCurrentAmp = self.leftFront.getOutputCurrent()
        self.leftBackCurrentAmp = self.leftBack.getOutputCurrent()
        self.rightFrontCurrentAmp = self.rightFront.getOutputCurrent()
        self.rightBackCurrentAmp = self.rightBack.getOutputCurrent()
        self.leftFrontEncoderValue = self.leftFrontEncoder.getVelocity()
        self.leftBackEncoderValue = self.leftBackEncoder.getVelocity()
        self.rightFrontEncoderValue = self.rightFrontEncoder.getVelocity()
        self.rightBackEncoderValue = self.rigthBackEncoder.getVelocity()