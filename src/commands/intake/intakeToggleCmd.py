from commands2 import InstantCommand, CommandScheduler
from robotContainer import RobotContainer

class ToggleIntakeCommand(InstantCommand):
    def __init__(self, robotContainer: RobotContainer):
        super().__init__()
        self.robotContainer = robotContainer

    def initialize(self):
        if self.robotContainer.intakeCommandGroup.isScheduled():
            CommandScheduler.getInstance().cancel(self.robotContainer.intakeCommandGroup)
            self.robotContainer.updateIntakeState(False)  # Assuming you have a method to update the state
        else:
            self.robotContainer.intakeCommandGroup.schedule()
            self.robotContainer.updateIntakeState(True)   # Assuming you have a method to update the state
