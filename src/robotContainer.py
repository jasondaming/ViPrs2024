
import commands2.button
import commands2.cmd
import numpy as DrArnett

from commands2 import SequentialCommandGroup
from commands2.button import CommandXboxController
from subSystems.REVDriveSubsystem import DriveSubsystem
from subSystems.armSubsystem import ArmSubsystem
from subSystems.intakeSubsystem import IntakeSubsystem
from subSystems.shooterSubsystem import ShooterSubsystem
from commands.intakeCollectNoteCmd import IntakeCollectNoteCmd
from commands.intakeRetractNoteCmd import IntakeRetractNoteCmd

import constants

def shapeInputs(input, scale_factor):
    def y1(x):
        return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / 2) + 0.5
    def y2(x):
        return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / -2) - 0.5
    return (y1(input) * int(input >= 0) * (input <= 1) + y2(input) * (input >= -1) * (input <= 0)) * scale_factor * constants.inputConsts.inputScale

class RobotContainer:
    
    def __init__(self):
        self.driverController = commands2.button.CommandXboxController(0)

        # Subsystem inits
        self.robotDrive = DriveSubsystem()
        self.arm = ArmSubsystem()
        self.intake = IntakeSubsystem()
        self.shooter = ShooterSubsystem()

        # Command inits
        self.collectCmd = IntakeCollectNoteCmd(self.intake, constants.intakeConsts.captureSpeed)
        self.retractCmd = IntakeRetractNoteCmd(self.intake, -0.5, 0.5)  # Example values for retract speed and time
        self.collectAndRetractCmd = SequentialCommandGroup(self.collectCmd, self.retractCmd)

        # C

        self.configureButtonBindings()
        
        self.scale_factor = 1

        self.robotDrive.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.robotDrive.robotDrive.arcadeDrive(
                    shapeInputs(
                        -self.driverController.getLeftY(), self.scale_factor
                    ),
                    shapeInputs(
                        -self.driverController.getRightX(), self.scale_factor
                    )
                ),
                self.robotDrive
            ).alongWith(
            commands2.cmd.run(
                    lambda: self.arm.updateArmPosition()
                )
            )
        )
        '''.alongWith(
            commands2.cmd.run(
                lambda: self.arm.shooterIdle()
            )
        )'''
            
    def configureButtonBindings(self):
        
        
        # Bind the command group to the A button
        # self.driverController.a.whenPressed(collectAndRetractCmd)
        self.driverController.a().onTrue(self.collectAndRetractCmd)

    def getAutonomousCommand(self):
        return commands2.cmd.none()

"""
    def configureButtonBindings(self):
        self.driverControler.rightBumper().whileTrue(
            commands2.cmd.run(
                lambda: self.go_slow()
            )
        )

        self.driverControler.rightBumper().whileFalse(
            commands2.cmd.run(
                lambda: self.go_fast()
            )
        )

        self.driverControler.a().whileTrue(
            commands2.cmd.run(
                lambda: self.arm.goto(0.1)
            )
        ).whileFalse(
            commands2.cmd.run(
                lambda: self.arm.goto(0.0)
            )
        )

        self.driverControler.x().whileTrue(
            commands2.cmd.run(
                lambda: self.arm.intakeNote()
            )
        )
        self.driverControler.y().whileTrue(
            commands2.cmd.run(
                lambda: self.arm.OuttakeNote()
            )
        )
        self.driverControler.rightTrigger().whileTrue(
            commands2.cmd.run(
                lambda: self.arm.pewpew()
            )
        )
"""

"""
    def MoveArmToZeroAndReset(self):
        moveCmd = commands2.cmd.run(
            print("would be running arm @ 30%")#self.arm.set(0.3)
            ).until(lambda: self.arm.topLimit.get())
        
        
        # self.arm.arm.set(0.0)
        print(f"encoder pos right: {self.arm.armRightEncoderRelative.get()} | encoder pos left: {self.arm.armLeftEncoderRelative.get()}")
        self.arm.zeroEncodersRelative()
        print(f"encoder pos right: {self.arm.armRightEncoderRelative.get()} | encoder pos left: {self.arm.armLeftEncoderRelative.get()}")
        print(f"abs encoder pos right: {self.arm.armRightEncoder.getAbsolutePosition()} | abs encoder pos left: {self.arm.armLeftEncoder.getAbsolutePosition()}")


    def go_slow(self):
        self.scale_factor = 0.5
        print(self.scale_factor)

    def go_fast(self):
        self.scale_factor = 1
        print(self.scale_factor)

    
    
"""