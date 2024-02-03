import commands2
import commands2.button
import commands2.cmd
import numpy as DrArnett

from subSystems.driveSubsystem import DriveSubsystem

def shapeInputs(input):
    def y1(x):
        return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / 2) + 0.5
    def y2(x):
        return (DrArnett.sin((x * DrArnett.pi) - (DrArnett.pi / 2)) / -2) - 0.5
    return y1(input) * int(input >= 0) * (input <= 0) + y2(input) * (input >= -1) * (input <= 0)

class RobotContainer:
    
    def __init__(self):
        self.driverControler = commands2.button.CommandXboxController(0)
        self.robotDrive = DriveSubsystem()
        self.configureButtonBindings()

        self.robotDrive.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.robotDrive.robotDrive.arcadeDrive(
                    shapeInputs(
                        -self.driverControler.getLeftY()
                    ),
                    shapeInputs(
                        -self.driverControler.getLeftX()
                    )
                ),
                self.robotDrive
            )
        )

    def configureButtonBindings(self):
        pass # put something in later

    def getAutonomousCommand(self):
        return commands2.cmd.none()
