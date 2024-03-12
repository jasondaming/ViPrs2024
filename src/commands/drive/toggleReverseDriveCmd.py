from commands2 import Command
from subSystems.REVDriveSubsystem import DriveSubsystem



class ToggleReverseDriveCmd(Command):
    def __init__(self, driveSubsystem: DriveSubsystem):
        super().__init__()
        self.driveSubsystem = driveSubsystem
        self.addRequirements(driveSubsystem)

    def initialize(self):
        # Toggle the reverse drive state
        self.driveSubsystem.toggleReverseMode()
