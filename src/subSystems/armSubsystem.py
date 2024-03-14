import time
import wpilib
import wpilib.drive
import commands2
import rev
import constants
import numpy as Derek

from team254.SparkMaxFactory import SparkMaxFactory
from team254.LazySparkMax import LazySparkMax

from team4646.PID import PID

from team1329.SimplePIDController import SimplePIDController


class ArmSubsystem(commands2.Subsystem):
    class Cache:
        def __init__(self):
            self.setpoint = 0.0
            self.rightCurrentAmp = 0.0
            self.leftCurrentAmp = 0.0
            self.rightEncoderValue = 0.0
            self.leftEncoderValue = 0.0
            self.leftPositionOffset = 0.0
            self.rightPositionOffset = 0.0
            # self.rightRelativeEncoderValue = 0.0
            # self.leftRelativeEncoderValue = 0.0
            self.bottomSensorValue = None
            self.topSensorValue = None
            self.maxEncoderValue = 0.0
            self.minEncoderValue = 0.0
            self.controlLoopTime = 0.0

    def __init__(self):
        super().__init__()
        self.cache = self.Cache()
        self.lastUpdateTime = time.time()

        self.holdingAtTop = False  # Add a flag to indicate when holding position at top

        # self.armRight = rev.CANSparkMax(constants.CANIDs.rightArmSpark, rev.CANSparkMax.MotorType.kBrushless)
        # self.armLeft = rev.CANSparkMax(constants.CANIDs.leftArmSpark, rev.CANSparkMax.MotorType.kBrushless)
        self.armRight = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.rightArmSpark, True)
        self.armLeft = SparkMaxFactory.createDefaultSparkMax(constants.CANIDs.leftArmSpark, False)
        self.arm = wpilib.MotorControllerGroup(self.armRight, self.armLeft)
        self.armRight.setInverted(True) # this can be specified by passing in a boolean to the createDefaultSparkMax method
        
        # Can only use built-in PID controller if we are using: a) the encoder built into the 
        # NEO motor _or_ an external encoder attached to the data port on the Spark Max
        # Currently we do not have it hooked to the Spark Max

        # self.armRightPIDController = self.armRight.getPIDController()
        # self.armLeftPIDController = self.armLeft.getPIDController()
        # self.armRightPIDController = self.armRight._pid_controller
        # self.armLeftPIDController = self.armLeft._pid_controller

        # self.armRightPIDController.setP(constants.armConsts.armControlP)
        # self.armRightPIDController.setI(constants.armConsts.armControlI)
        # self.armRightPIDController.setD(constants.armConsts.armControlD)
        # self.armLeftPIDController.setP(constants.armConsts.armControlP)
        # self.armLeftPIDController.setI(constants.armConsts.armControlI)
        # self.armLeftPIDController.setD(constants.armConsts.armControlD)

        # Set the acceleration strategy for both PID controllers
        # self.armRightPIDController.setSmartMotionAccelStrategy(rev.SparkMaxPIDController.AccelStrategy.kSCurve, 0)
        # self.armLeftPIDController.setSmartMotionAccelStrategy(rev.SparkMaxPIDController.AccelStrategy.kSCurve, 0)
        # self.armRightPIDController.setSmartMotionMaxVelocity(constants.armConsts.maxVelocity, constants.armConsts.slotID)
        # self.armLeftPIDController.setSmartMotionMaxVelocity(constants.armConsts.maxVelocity, constants.armConsts.slotID)
        # self.armRightPIDController.setSmartMotionMaxAccel(constants.armConsts.maxAcc, constants.armConsts.slotID)
        # self.armLeftPIDController.setSmartMotionMaxAccel(constants.armConsts.maxAcc, constants.armConsts.slotID)

        self.armLeftSPIDController = SimplePIDController(constants.armConsts.armPIDValues)
        self.armRightSPIDController = SimplePIDController(constants.armConsts.armPIDValues)


        self.armRight.IdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.armLeft.IdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.motorArmRightEncoder = self.armRight.getEncoder()
        self.motorArmLeftEncoder = self.armLeft.getEncoder()

        self.armRightEncoder = wpilib.DutyCycleEncoder(constants.armConsts.rightEncoder)
        self.armLeftEncoder = wpilib.DutyCycleEncoder(constants.armConsts.leftEncoder)

        # adding relative encoders:
        # self.armRightEncoderRelative = wpilib.Encoder(
        #     constants.armConsts.rightRelativeEncoderA,
        #     constants.armConsts.rightRelativeEncoderB
        # )
        # self.armLeftEncoderRelative = wpilib.Encoder(
        #     constants.armConsts.leftRelativeEncoderA,
        #     constants.armConsts.leftRelativeEncoderB
        # )
        # self.armLeftEncoderRelative.setReverseDirection(True)

        # !!!!!!!!!!!!!!!!!!!!
        # THIS APPARENTLY DOESN'T WORK
        # self.armRightEncoder.setPositionOffset(constants.armConsts.rightEncoderOffset)
        # self.armLeftEncoder.setPositionOffset(constants.armConsts.leftEncoderOffset)
        # !!!!!!!!!!!!!!!!!!!!

        # self.zeroEncoders()

        # bottom limit switch to detect if the arm is all the way down
        self.bottomLimit = wpilib.DigitalInput(constants.sensorConsts.armBottomLimit) # change channel later
        self.topLimit = wpilib.DigitalInput(constants.sensorConsts.armTopLimit)

        self.armTargetAngle = 0.0
        self.controlVoltage = 0.0

        self.isActive = False

    def clipValue(self, value, upperBound, lowerBound):
        assert upperBound > lowerBound
        if value > upperBound:
            return upperBound
        elif value < lowerBound:
            return lowerBound
        else:
            return value

    def goto(self, angle):
        self.isActive = True
        # self.armTargetAngle = angle
        self.cache.setpoint = constants.convert.rad2rev(angle)
        self.armLeftSPIDController.reset()
        self.armRightSPIDController.reset()
        print(f"ArmSubsystem.goto({angle}) -- self.cache.setpoint = {self.cache.setpoint}")
        

    def stop(self):
        """
        Stops the arm movement by setting the motor output to zero.
        This method can be called for immediate stop actions, ignoring PID control.
        """
        # Additionally, for PID control, you might want to ensure that the system
        # is not trying to move the arm by setting the setpoint to the current position.
        # This effectively tells the PID controller to "hold" rather than to "move".
        currentPos = self.getArmPosition()
        self.cache.setpoint = currentPos

        # Reset any flags or states as necessary
        self.holdingAtTop = False  # If using a flag to indicate holding at the top

        # Optionally, if you're using PID control to manage arm position and you want
        # to maintain that control framework, you could set the reference to the current
        # position with zero feedforward to hold position without additional input.
        # This is more of a "soft stop" that leverages the PID controller.
        gravity_compensation = self.calcGravityComp(self.getArmPosition())
        # self.armRightPIDController.setReference(currentPos, rev.CANSparkMaxLowLevel.ControlType.kPosition, 0, gravity_compensation, rev.SparkPIDController.ArbFFUnits.kVoltage)
        # self.armLeftPIDController.setReference(currentPos, rev.CANSparkMaxLowLevel.ControlType.kPosition, 0, gravity_compensation, rev.SparkPIDController.ArbFFUnits.kVoltage)
        # self.armRightPIDController.setReference(currentPos, rev.CANSparkMaxLowLevel.ControlType.kPosition, 0, gravity_compensation)
        # self.armLeftPIDController.setReference(currentPos, rev.CANSparkMaxLowLevel.ControlType.kPosition, 0, gravity_compensation)

    def calcGravityComp(self, armPos):

        return constants.armConsts.gravityGain * Derek.cos(armPos)

    def updateHardware(self):
        # print("armSubsystem.updateHardware()")
        if self.isActive:
            # print("armSubsystem.updateHardware() - self.isActive = True")
            print(f"armSubsystem.updateHardware() - getArmPosition()={self.getArmPosition()}")
            now = time.time()
            dt = now - self.lastUpdateTime
            self.lastUpdateTime = now

            currentPosRight = self.getArmRightPosition()
            currentPosLeft = self.getArmLeftPosition()
            currentPosAverage = (currentPosRight + currentPosLeft) / 2  # Average position of both sides

            # Calculate the arbitrary feedforward term based on the current position
            feedforward = self.calcGravityComp(currentPosAverage)

            # Safety checks for limit switches
            # if self.bottomLimit.get() and self.cache.setpoint < currentPosAverage:
            #     print("... Bottom limit safety check")
            #     self.stop()
            #     return

            # if self.cache.topSensorValue:
            #     print("...  Top limit safety check...")
            #     if not self.holdingAtTop:
            #         print("... not holding at the top")
            #         self.holdingAtTop = True
            #         self.stop()
            #         return
            # else:
            #     self.holdingAtTop = False

            # Update the setpoint for both PID controllers with feedforward
            self.armRightSPIDController.set_setpoint(self.cache.setpoint, feedforward)
            self.armLeftSPIDController.set_setpoint(self.cache.setpoint, feedforward)

            # Calculate the control effort
            controlEffortRight = self.armRightSPIDController.update(currentPosRight, dt, feedforward)
            controlEffortLeft = self.armLeftSPIDController.update(currentPosLeft, dt, feedforward)

            # Apply the control effort to the motors
            self.armRight.set(self.clipValue(controlEffortRight, 2.0, -2.0))
            self.armLeft.set(self.clipValue(controlEffortLeft, 2.0, -2.0))

            print(f"armSubsystem().updateHardware() - controlEffortRight/Left={controlEffortRight}, {controlEffortLeft}")

        '''
        print(f"armSubsystem.updateHardware() - getArmPosition()={self.getArmPosition()}")
        if self.isActive:
            # currentPos = self.getArmPosition()  # Your method to calculate the current arm position
            targetPos = self.cache.setpoint  # Target position set by `goto` method
            gravity_feedforward_voltage = self.calcGravityComp()
            # error = targetPos - currentPos # Calculate error   # Not needed since it's calculated in the PID Controller

            if self.cache.topSensorValue and not self.holdingAtTop:
                # If at top and not already holding, update target to current position and set flag
                targetPos = currentPos
                self.cache.setpoint = currentPos
                self.holdingAtTop = True
            elif not self.cache.topSensorValue:
                # If not at top, clear the holding flag
                self.holdingAtTop = False

            # if self.isPositionSafe(targetPos) == False:
            #     # We are at an unsafe position, something is wrong
            #     print("!!!!!!!!! UNSAFE POSITION DETECTED !!!!!!!!!!!!!!")
            #     return
            
            # PID Controller already set up with P, I, D values
            # Use setReference to move arm to target position
            # Ensure setReference is using correct units matching your encoders
            print(f"armSubsystem.updateHardware() - currentPos={currentPos}, targetPos={targetPos}, ctrl={rev.CANSparkMaxLowLevel.ControlType.kPosition}, pidSlot={constants.armConsts.slotID}, arbFeedforward={gravity_feedforward_voltage}")
            # self.armRightPIDController.setReference(targetPos, rev.CANSparkMaxLowLevel.ControlType.kSmartMotion, pidSlot=0, arbFeedforward=gravity_feedforward_voltage, arbFFUnits=rev.SparkPIDController.ArbFFUnits.kVoltage)
            # self.armLeftPIDController.setReference(targetPos, rev.CANSparkMaxLowLevel.ControlType.kSmartMotion, pidSlot=0, arbFeedforward=gravity_feedforward_voltage, arbFFUnits=rev.SparkPIDController.ArbFFUnits.kVoltage)
            # self.armRightPIDController.setReference(targetPos, rev.CANSparkMaxLowLevel.ControlType.kPosition, pidSlot=constants.armConsts.slotID, arbFeedforward=gravity_feedforward_voltage)
            # self.armLeftPIDController.setReference(targetPos, rev.CANSparkMaxLowLevel.ControlType.kPosition, pidSlot=constants.armConsts.slotID, arbFeedforward=gravity_feedforward_voltage)
            
            self.armLeftSPIDController.set_setpoint(self.cache.setpoint)
            self.armRightSPIDController.set_setpoint(self.cache.setpoint)   
            
            controlEffortLeft = self.armLeftSPIDController.update(currentPos)
           

            # Logic for bottom limit switch as before
            if self.cache.bottomSensorValue and error < 0:
                self.stop()

            # Additional logic for moving down from the top
            # If the arm is holding at the top and a command is issued to move down (setpoint < current position), allow it
            if self.holdingAtTop and self.cache.setpoint < currentPos:
                self.holdingAtTop = False  # Clear the holding flag to allow movement
    '''


    # def updateHardware(self):
    #     # print("ArmSubsystem.updateHardware()")
    #     if self.isActive:
    #         print("ArmSubsystem.updateHardware() -- self.isActive == True")
    #         delta = self.armTargetAngle - self.getArmPosition() # self.getArmPosition()
    #         """If we want the arm to move smoothly and precicesly, we need this:
    #         https://robotpy.readthedocs.io/projects/rev/en/stable/rev/SparkMaxPIDController.html
    #         starting with the P gain being our "rotationSpeedScalar" and feedforward gain being 
    #         gravityGain * cos(angle) should be similar behavior to what we have now.
    #         Then we can play with the accel profile & D gain to slow down the initial speed,
    #         and we can play with the I gain to increase the precision of the final angle.
            
    #         """
    #         P_voltage = delta * constants.armConsts.rotationSpeedScaler
    #         gravity_feedforward_voltage = constants.armConsts.gravityGain * Derek.cos(self.getArmPosition())
    #         self.armLeftPIDController.setP(constants.armConsts.rotationSpeedScalerP)
    #         self.armLeftPIDController.setI(0)
    #         self.armLeftPIDController.setD(0)
    #         self.armRightPIDController.setP(constants.armConsts.rotationSpeedScalerP)
    #         self.armRightPIDController.setI(0)
    #         self.armRightPIDController.setD(0)
    #         self.controlVoltage = P_voltage + gravity_feedforward_voltage
            
    #         #limit voltage if it's at the limit switch
    #         if self.bottomLimit.get() and self.controlVoltage < 0.0:
    #             self.controlVoltage = 0.0
    #         elif self.topLimit.get() and self.controlVoltage > 0.0:
    #             self.controlVoltage = 0.0
                    
    #         self.controlVoltage = ArmSubsystem.clipValue(self.controlVoltage, 2.0, -2.0)
    #         # print(self.controlVoltage)
    #         self.arm.setVoltage(self.controlVoltage)

    def cacheSensors(self):
        self.cache.leftCurrentAmp = self.armLeft.getOutputCurrent()
        self.cache.rightCurrentAmp = self.armRight.getOutputCurrent()
        # Negate left encoder value because it goes in the opposite direction
        self.cache.leftEncoderValue = -1.0 * (self.armLeftEncoder.getAbsolutePosition() - constants.armConsts.leftEncoderOffset)
        self.cache.rightEncoderValue = self.armRightEncoder.getAbsolutePosition() - constants.armConsts.rightEncoderOffset
        self.cache.leftPositionOffset = self.armLeftEncoder.getPositionOffset()
        self.cache.rightPositionOffset = self.armRightEncoder.getPositionOffset()
        # self.cache.leftRelativeEncoderValue = self.armLeftEncoderRelative.get()
        # self.cache.rightRelativeEncoderValue = self.armRightEncoderRelative.get()
        self.cache.bottomSensorValue = self.bottomLimit.get()
        self.cache.topSensorValue = self.topLimit.get()
        print(f"lEV: {self.cache.leftEncoderValue}, rEV: {self.cache.rightEncoderValue}")
        print(f"getArmPosition(): {self.getArmPosition()}")

    def getArmRightPosition(self):
        # return self.armRightEncoder.getAbsolutePosition() - self.armRightEncoder.getPositionOffset()
        return self.cache.rightEncoderValue # - self.cache.rightPositionOffset

    def getArmLeftPosition(self):
        # return self.armLeftEncoder.getAbsolutePosition() - self.armLeftEncoder.getPositionOffset()
        return self.cache.leftEncoderValue # - self.cache.leftPositionOffset
    
    # def zeroEncoders(self):
    #     rightOffset = self.armRightEncoder.getAbsolutePosition()
    #     leftOffset = self.armLeftEncoder.getAbsolutePosition()
    #     self.armRightEncoder.setPositionOffset(rightOffset)
    #     self.armLeftEncoder.setPositionOffset(leftOffset)
    #     print(f"right encoder offset: {self.armRightEncoder.getPositionOffset()} | left encoder offset: {self.armLeftEncoder.getPositionOffset()}")
    
    def getArmPosition(self):
        # return constants.convert.rev2rad((self.getArmRightPosition() - self.getArmLeftPosition()) / 2)
        # Average the encoder values, considering any necessary conversion from encoder units to radians.
        # This example assumes the encoder values are already in a useful form and just averages them.
        average_encoder_value = (self.getArmRightPosition() + self.getArmLeftPosition()) / 2
        
        # Convert the average encoder value to radians or the unit of measure you're using for the arm position.
        # This might involve converting from encoder fractions to radians, taking into account the total range of motion.

        # arm_position_radians = convertEncoderValueToRadians(average_encoder_value)
        arm_position_radians = constants.convert.rev2rad(average_encoder_value)

        return arm_position_radians
    
    def isPositionSafe(self, position):
        # Example safe bounds, adjust based on your system's specifics
        safeMin = constants.armConsts.minEncoderValue
        safeMax = constants.armConsts.maxEncoderValue
        isSafe = safeMin <= position <= safeMax
        print(f"armSubsystem.isPositionSafe() - safeMin={safeMin}, safeMax={safeMax}, isSafe={isSafe}")
        return isSafe
    
    


    '''
    def __str__(self):
        """To string for robot's arm"""
        # return f"angle: {self.getArmPositionRelative()}rad | target: {self.armTargetAngle}rad | voltage: {self.controlVoltage} | topLimit: {self.topLimit.get()} | bottomLimit: {self.bottomLimit.get()}"
        return f"armSubsystem : angle: {self.getArmPosition()} rad"
    '''

 
