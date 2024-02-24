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
        self.bottomShooter.setInverted(True)
        self.intake = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)

        self.armRight.IdleMode(rev.CANSparkBase.IdleMode.kCoast)
        self.armLeft.IdleMode(rev.CANSparkBase.IdleMode.kCoast)
        self.topShooter.IdleMode(rev.CANSparkBase.IdleMode.kCoast)
        self.bottomShooter.IdleMode(rev.CANSparkBase.IdleMode.kCoast)
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

        # Photo Sensor to detect if a note is loaded
        self.noteSensor = wpilib.DigitalInput(1) # change channel later

        # bottom limit switch to detect if the arm is all the way down
        self.bottomLimit = wpilib.DigitalInput(2) # change channel later

        self.armTargetAngle = 0

    def goto(self, angle):
        self.armTargetAngle = angle

    def updateArmPosition(self):
        delta = self.armTargetAngle - self.getArmPosition()
        self.arm.set(delta * constants.armConsts.rotationSpeedScaler)

    def shootHigh(self):
        pass
        """
        self.topShooter.set(1)
        self.bottomShooter.set(1)
        while topSpeed < 2500 or bottomSpeed < 2500{
            
        }
        self.intake.set(1)
        while isNoteLoaded(){
            
        }
        self.topShooter.set(0)
        self.bottomShooter.set(0)
        self.intake.set(0)
        """

    def pickup(self):
        pass
        """
        if not isNoteLoaded(){
            self.intake.set(0.5)
        }else{
            self.intake.set(0)
        }
        """

    def lowerArmForPickup():
        pass
        """
        
        """

    def isNoteLoaded(self):
        return self.noteSensor.get()
    
    def zeroEncoders(self):
        self.armRightEncoder.setPositionOffset(self.armRightEncoder.getAbsolutePosition())

    def getArmPosition(self):
        return self.armRightEncoder.getAbsolutePosition() - self.armRightEncoder.getPositionOffset()
    # todo make zeroEncoders method