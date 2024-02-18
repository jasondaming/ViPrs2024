import wpilib
import wpilib.drive
import commands2
import rev
import constants

class ArmSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()
        self.armRight = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.armLeft = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
        self.arm = wpilib.MotorControllerGroup(self.armRight, self.armLeft)
        self.armRight.setInverted(True)

        self.topShooter = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)
        self.bottomShooter = rev.CANSparkMax(8, rev.CANSparkMax.MotorType.kBrushless)
        self.intake = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)

        self.armRight.IdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.armLeft.IdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.topShooter.IdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.bottomShooter.IdleMode(rev.CANSparkBase.IdleMode.kBrake)
        self.intake.IdleMode(rev.CANSparkBase.IdleMode.kBrake)

        self.motorArmRightEncoder = self.armRight.getEncoder()
        self.motorArmLeftEncoder = self.armLeft.getEncoder()
        self.topShooterEncoder = self.topShooter.getEncoder()
        self.bottomShooterEncoder = self.bottomShooter.getEncoder()
        self.intakeEncoder = self.intake.getEncoder()

        self.armRightEncoder = wpilib.DutyCycleEncoder(5)
        self.armLeftEncoder = wpilib.DutyCycleEncoder(6)

        self.armRightEncoder.setPositionOffset(0.85)
        self.armLeftEncoder.setPositionOffset(self.armLeftEncoder.getAbsolutePosition())

    def shoot():
        pass

    def getArmPosition(self):
        return self.armRightEncoder.getAbsolutePosition() - self.armRightEncoder.getPositionOffset()
    # todo make zeroEncoders method