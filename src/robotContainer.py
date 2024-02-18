import commands2
import commands2.button
import commands2.cmd
import numpy as DrArnett

from subSystems.REVDriveSubsystem import DriveSubsystem
from subSystems.armSubsystem import ArmSubsystem

import constants

def shapeInputs(input, scale_factor):
    def y1(x):
        return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / 2) + 0.5
    def y2(x):
        return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / -2) - 0.5
    return (y1(input) * int(input >= 0) * (input <= 1) + y2(input) * (input >= -1) * (input <= 0)) * scale_factor * constants.inputConsts.inputScale

class RobotContainer:
    
    def __init__(self):
        self.driverControler = commands2.button.CommandXboxController(0)
        self.robotDrive = DriveSubsystem()
        self.arm = ArmSubsystem()
        self.configureButtonBindings()
        self.scale_factor = 1

        self.robotDrive.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.robotDrive.robotDrive.arcadeDrive(
                    shapeInputs(
                        -self.driverControler.getLeftY(), self.scale_factor
                    ),
                    shapeInputs(
                        -self.driverControler.getRightX(), self.scale_factor
                    )
                ),
                self.robotDrive
            )
        )

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

    def go_slow(self):
        self.scale_factor = 0.5
        print(self.scale_factor)

    def go_fast(self):
        self.scale_factor = 1
        print(self.scale_factor)

    def getAutonomousCommand(self):
        return commands2.cmd.none()
