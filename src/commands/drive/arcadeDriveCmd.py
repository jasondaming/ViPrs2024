import wpilib
import commands2
import commands2.cmd

from commands2.button import CommandXboxController
from subSystems.REVDriveSubsystem import DriveSubsystem
from util.inputShaping import InputShaping
from constants import inputConsts

import constants

class ArcadeDriveCommand(commands2.Command):
    def __init__(self, driveSubsystem: DriveSubsystem, driverController: CommandXboxController):
        super().__init__()
        print(f"ArcadeDriveCommand: DriveSubsystem = {driveSubsystem}")
        self.driveSubsystem = driveSubsystem
        self.driverController = driverController
        self.addRequirements(self.driveSubsystem)
        
    def execute(self):
        forward = -self.driverController.getLeftY()
        rotation = self.driverController.getRightX()

        # Apply input shaping if necessary
        forward = InputShaping.shapeInputs(forward, inputConsts.inputScale)  # Adjust scale factor as needed
        rotation = InputShaping.shapeInputs(rotation, inputConsts.inputScale)  # Adjust scale factor as needed
        self.driveSubsystem.arcadeDriveSS(forward, rotation)
