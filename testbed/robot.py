# TODO: insert robot code here
#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import rev

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        super().__init__()

        # self.timer = wpilib.Timer()
        self.motor_31 = rev.CANSparkMax(31, rev.CANSparkMax.MotorType.kBrushless)
        # self.motor_32 = rev.CANSparkMax(32, rev.CANSparkMax.MotorType.kBrushless)
        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.controller = wpilib.XboxController(0)
        self.encoder_31 = self.motor_31.getEncoder()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        # self.timer.restart()
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self): 
        """This function is called once each time the robot enters teleoperated mode."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        # self.motor_31.set(self.controller.getLeftY())
        self.motor_31.set(self.controller.getRightY())
        print(self.encoder_31.getPosition())
        # self.spark1.set(0.15)

    def testInit(self): 
        """This function is called once each time the robot enters test mode."""
        pass

    def testPeriodic(self): 
        """This function is called periodically during test mode."""
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)