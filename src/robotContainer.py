
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
from commands.arcadeDriveCmd import ArcadeDriveCommand
from constants import States, intakeConsts, inputConsts
from subSystems.robotState import RobotState

class RobotContainer:
    
    def __init__(self):
        self.robotState = RobotState()

        self.driverController = commands2.button.CommandXboxController(0)

        # Subsystem inits
        self.robotDrive = DriveSubsystem()
        self.arm = ArmSubsystem()
        self.intake = IntakeSubsystem()
        self.shooter = ShooterSubsystem()

        # Command inits
        self.collectCmd = IntakeCollectNoteCmd(self.intake, intakeConsts.captureSpeed)
        self.retractCmd = IntakeRetractNoteCmd(self.intake, -0.5, 0.5)  # Example values for retract speed and time
        self.collectAndRetractCmd = SequentialCommandGroup(self.collectCmd, self.retractCmd)
        self.arcadeDriveCmd = ArcadeDriveCommand(self.robotDrive, self.driverController)

        # Configure buttons
        self.configureButtonBindings()
        
        self.robotDrive.setDefaultCommand(self.arcadeDriveCmd)


    def toggleIntakeCommand(self):
        # Check the current state of the intake and toggle accordingly
        if self.robotState.get('intake') != States.INTAKE_COLLECTING:
            # If not currently collecting, start collecting
            self.robotState.setSubsystemState('intake', States.INTAKE_COLLECTING)
            self.collectAndRetractCmd.schedule()
        else:
            # If already collecting, cancel and set to idle
            self.robotState.setSubsystemState('intake', States.INTAKE_IDLE)
            self.collectAndRetractCmd.cancel()

    def configureButtonBindings(self):
        # Bind the command group to the A button
        # self.driverController.a.whenPressed(collectAndRetractCmd)
        #self.driverController.a().onTrue(self.collectAndRetractCmd)

        # Bind the toggleIntakeCommand method to the A button press
        self.driverController.a().toggleOnTrue(self.toggleIntakeCommand)

    def getAutonomousCommand(self):
        return commands2.cmd.none()
