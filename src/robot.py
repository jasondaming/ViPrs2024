# TODO: insert robot code here
#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import phoenix5
import rev
import numpy as np

PI = 3.1415926535
INPUTSCALEFACTOR = 0.5

def filterInput(x):
    return INPUTSCALEFACTOR * x

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
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
        self.controller = wpilib.XboxController(0)
        self.timer = wpilib.Timer()

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightDrive.setInverted(True)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            # Drive forwards half speed, make sure to turn input squaring off
            self.robotDrive.arcadeDrive(0.5, 0, squareInputs=True)
        else:
            self.robotDrive.stopMotor()  # Stop robot

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        self.robotDrive.arcadeDrive(
            filterInput(-self.controller.getLeftY()), filterInput(-self.controller.getRightX())
        )
        # self.spark1.set(0.15)

    def testInit(self):
        """This function is called once each time the robot enters test mode."""

    def testPeriodic(self):
        """This function is called periodically during test mode."""


if __name__ == "__main__":
    wpilib.run(MyRobot)