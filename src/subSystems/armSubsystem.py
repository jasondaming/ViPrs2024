import wpilib
import wpilib.drive
import commands2
import rev
import constants
import numpy as Derek

from team254.SparkMaxFactory import SparkMaxFactory
from team254.LazySparkMax import LazySparkMax


class ArmSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()
        # self.armRight = rev.CANSparkMax(constants.CANIDs.rightArmSpark, rev.CANSparkMax.MotorType.kBrushless)
        # self.armLeft = rev.CANSparkMax(constants.CANIDs.leftArmSpark, rev.CANSparkMax.MotorType.kBrushless)
        self.armRight = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.rightArmSpark)
        self.armLeft = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.leftArmSpark)
        self.arm = wpilib.MotorControllerGroup(self.armRight, self.armLeft)
        self.armRight.setInverted(True)

        self.armRight.IdleMode(rev.CANSparkBase.IdleMode.kCoast)
        self.armLeft.IdleMode(rev.CANSparkBase.IdleMode.kCoast)

        self.motorArmRightEncoder = self.armRight.getEncoder()
        self.motorArmLeftEncoder = self.armLeft.getEncoder()

        self.armRightEncoder = wpilib.DutyCycleEncoder(constants.armConsts.rightEncoder)
        self.armLeftEncoder = wpilib.DutyCycleEncoder(constants.armConsts.leftEncoder)

        # adding relative encoders:
        self.armRightEncoderRelative = wpilib.Encoder(
            constants.armConsts.rightRelativeEncoderA,
            constants.armConsts.rightRelativeEncoderB
        )
        self.armLeftEncoderRelative = wpilib.Encoder(
            constants.armConsts.leftRelativeEncoderA,
            constants.armConsts.leftRelativeEncoderB
        )
        self.armLeftEncoderRelative.setReverseDirection(True)

        self.armRightEncoder.setPositionOffset(0.45699721142493027)
        self.armLeftEncoder.setPositionOffset(0.39403500985087525)

        # bottom limit switch to detect if the arm is all the way down
        self.bottomLimit = wpilib.DigitalInput(constants.sensorConsts.armBottomLimit) # change channel later
        self.topLimit = wpilib.DigitalInput(constants.sensorConsts.armTopLimit)

        self.armTargetAngle = 0.0
        self.controlVoltage = 0.0

        self.isActive = False

    def clipValue(value, upperBound, lowerBound):
        assert upperBound > lowerBound
        if value > upperBound:
            return upperBound
        elif value < lowerBound:
            return lowerBound
        else:
            return value

    def goto(self, angle):
        print(f"ArmSubsystem.goto({angle})")
        self.isActive = True
        self.armTargetAngle = angle

    def updateHardware(self):
        pass

    def updateArmPosition(self):
        print("ArmSubsystem.updateArmPosition()")
        if self.isActive:
            print("ArmSubsystem.updateArmPosition() -- self.isActive == True")
            delta = self.armTargetAngle - self.getArmPosition() # self.getArmPosition()
            """If we want the arm to move smoothly and precicesly, we need this:
            https://robotpy.readthedocs.io/projects/rev/en/stable/rev/SparkMaxPIDController.html
            starting with the P gain being our "rotationSpeedScalar" and feedforward gain being 
            gravityGain * cos(angle) should be similar behavior to what we have now.
            Then we can play with the accel profile & D gain to slow down the initial speed,
            and we can play with the I gain to increase the precision of the final angle.
            
            """
            P_voltage = delta * constants.armConsts.rotationSpeedScaler
            gravity_feedforward_voltage = constants.armConsts.gravityGain * Derek.cos(self.getArmPosition())
            self.controlVoltage = P_voltage + gravity_feedforward_voltage
            
            #limit voltage if it's at the limit switch
            if self.bottomLimit.get() and self.controlVoltage < 0.0:
                self.controlVoltage = 0.0
            elif self.topLimit.get() and self.controlVoltage > 0.0:
                self.controlVoltage = 0.0
                    
            self.controlVoltage = ArmSubsystem.clipValue(self.controlVoltage, 2.0, -2.0)
            # print(self.controlVoltage)
            self.arm.setVoltage(self.controlVoltage)


    '''
    In the documentation it states this:

    GetAbsolutePosition() - GetPositionOffset() will give an encoder absolute position 
    relative to the last reset. This could potentially be negative, which needs to be 
    accounted for.

    Should we return the absolute value of the result?
    '''
    def getArmRightPosition(self):
        return self.armRightEncoder.getAbsolutePosition() - self.armRightEncoder.getPositionOffset()

    def getArmLeftPosition(self):
        return self.armLeftEncoder.getAbsolutePosition() - self.armLeftEncoder.getPositionOffset()
    
    def zeroEncoders(self):
        rightOffset = self.armRightEncoder.getAbsolutePosition()
        leftOffset = self.armLeftEncoder.getAbsolutePosition()
        self.armRightEncoder.setPositionOffset(rightOffset)
        self.armLeftEncoder.setPositionOffset(leftOffset)
        print(f"right encoder offset: {self.armRightEncoder.getPositionOffset()} | left encoder offset: {self.armLeftEncoder.getPositionOffset()}")
    
    def getArmPosition(self):
        return constants.convert.rev2rad((self.getArmRightPosition() - self.getArmLeftPosition()) / 2)
    

    '''
    def shootHigh(self):
        pass
        """
        pseudo code to raise the arm to shoot at the high goal

        // start the shooter motors running them at full speed
        self.topShooter.set(1)
        self.bottomShooter.set(1)

        // wait until both motors are up to full speed as determined by some minimal RPM(?) value for each
        while topSpeed < 2500 or bottomSpeed < 2500{
            
        }

        // once both shooting motors are at full speed, push the note into the shooter wheels by starting the intake motor
        self.intake.set(1)

        // once the photo sensor no longer sees the note then stop the shooter. 
        // NOTE: Might be better to stop the shooter and intake motors when the driver releases the "shoot" button
        while isNoteLoaded(){
            
        }

        // stop the shooter and intake motors
        self.topShooter.set(0)
        self.bottomShooter.set(0)
        self.intake.set(0)
        
        """
    '''

    '''
    def pickup(self):
        pass
        """
        
        if not isNoteLoaded(){
            // if the photo sensor does not detect a note being loaded then start the intake motors
            self.intake.set(0.5)

        } else {
            // else the photo sensor detected a note so stop the intake motors.  NOTE: May need an override button
            self.intake.set(0)
        }

        """
    '''

    '''
    def lowerArmForPickup():
        pass
        """
        (1) detect the current arm position
        (2) start the motors to move the arm down into the "pickup" position - 
            there will be a limit switch to detect when the arm contacts the lower cross brace
        (3) when the limit switch is tripped (value is true) stop the arm motors
        NOTE: one idea was to scale the arm speed by the delta angle (angle between starting position and current position)
            so that as the arm gets closer to its final position the arm speed slows down
        """
    '''
        
    '''
    def isNoteLoaded(self):
        return self.noteSensor.get()
    '''


    
    '''
    def zeroEncodersRelative(self):
        self.armRightEncoderRelative.reset()
        self.armLeftEncoderRelative.reset()
        self.motorArmLeftEncoder.setPosition(0.0)
        self.motorArmRightEncoder.setPosition(0.0)
    '''

    '''
    def getArmPositionRelative(self):
        """returns the arm's position in rad, averaged between the two encoders"""
        # posRight = constants.convert.rev2rad(constants.convert.count2rev(self.armRightEncoderRelative.get()))
        # posLeft = constants.convert.rev2rad(constants.convert.count2rev(self.armLeftEncoderRelative.get()))
        posRight = constants.convert.rev2rad(self.motorArmRightEncoder.getPosition()/constants.armConsts.motorToArmGearRatio)
        # posLeft = self.motorArmLeftEncoder.getPosition()
        
        return posRight
    '''




        
    ''' 
    def shooterIdle(self):
        self.intake.set(0.0)
        self.topShooter.set(0.0)
        self.bottomShooter.set(0.0)
    # todo make zeroEncoders method
    '''

    '''
    def intakeNote(self):
        self.intake.set(0.75)
    '''

    ''' 
    def OuttakeNote(self):
        self.intake.set(-0.75)
    '''
        
    '''
    def pewpew(self):
        self.shooters.set(-0.75)   
    '''
        
    '''
    def __str__(self):
        """To string for robot's arm"""
        # return f"angle: {self.getArmPositionRelative()}rad | target: {self.armTargetAngle}rad | voltage: {self.controlVoltage} | topLimit: {self.topLimit.get()} | bottomLimit: {self.bottomLimit.get()}"
        return f"armSubsystem : angle: {self.getArmPosition()} rad"
    '''

 
