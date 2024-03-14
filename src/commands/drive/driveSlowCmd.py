import commands2
from commands2 import Command
from subSystems.REVDriveSubsystem import DriveSubsystem

class ToggleSlowModeCmd(Command):
    def __init__(self, drive: DriveSubsystem):
        super().__init__()
        self.drive = drive
        self.getRequirements(self.drive)

    def initialize(self):
        """Called once when the command is initiated."""
        self.drive.toggleSlowMode()

    def isFinished(self):
        """This command runs quickly to toggle the state, so it's done immediately."""
        return True
