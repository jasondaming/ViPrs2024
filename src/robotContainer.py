
import commands2.button
import commands2.cmd
import numpy as DrArnett


from commands2 import SequentialCommandGroup, FunctionalCommand
from commands2.button import CommandXboxController

from subSystems.REVDriveSubsystem import DriveSubsystem
from subSystems.armSubsystem import ArmSubsystem
from subSystems.intakeSubsystem import IntakeSubsystem
from subSystems.shooterSubsystem import ShooterSubsystem
from commands.intake.intakeCollectNoteCmd import IntakeCollectNoteCmd
from commands.intake.intakeRetractNoteCmd import IntakeRetractNoteCmd
from commands.intake.intakeAndRetractCmd import IntakeAndRetractCommand
from commands.intake.intakeStartCmd import IntakeStartCmd
from commands.intake.detectNoteCmd import DetectNoteCmd
from commands.intake.stopIntakeCmd import StopIntakeCmd
from commands.intake.intakeExpelNoteCmd import IntakeExpelNoteCmd
from commands.intake.intakeDeliverNoteToShooterCmd import IntakeDeliverNoteToShooterCmd
from commands.shooter.shooterStartCmd import ShooterStartCmd
from commands.shooter.shooterStopCmd import ShooterStopCmd
from commands.drive.arcadeDriveCmd import ArcadeDriveCmd
from constants import States, intakeConsts, inputConsts, driveConsts
from subSystems.robotState import RobotState

class RobotContainer:
    
    def __init__(self):
        # State mechanics
        self.robotState = RobotState()

        # Control devices
        self.driverController = commands2.button.CommandXboxController(0)
        self.rightTriggerPressed = self.driverController.rightTrigger(threshold=0.5)

        # Subsystem inits
        self.robotDrive = DriveSubsystem()
        self.arm = ArmSubsystem()
        self.intake = IntakeSubsystem()
        self.shooter = ShooterSubsystem()

        # Subsystem configs
        self.robotDrive.setMaxOutput(driveConsts.driveMaxOutput)

        # Command inits

        # Intake commands
        self.collectCmd = IntakeCollectNoteCmd(self.intake, intakeConsts.captureSpeed)
        self.retractCmd = IntakeRetractNoteCmd(self.intake, intakeConsts.releaseSpeed, intakeConsts.retractTime)  # Example values for retract speed and time
        self.intakeAndRetractCommand = IntakeAndRetractCommand(self.intake, intakeConsts.releaseSpeed, intakeConsts.retractTime)
        self.intakeStartCmd = IntakeStartCmd(self.intake, intakeConsts.captureSpeed)
        self.stopIntakeCmd = StopIntakeCmd(self.intake)
        self.detectNoteCmd = DetectNoteCmd(self.intake)
        self.expelNoteCmd = IntakeExpelNoteCmd(self.intake, intakeConsts.expelSpeed, intakeConsts.expelTime)
        self.deliverNoteCmd = IntakeDeliverNoteToShooterCmd(self.intake)

        # Shooter commands
        self.startShooterCmd = ShooterStartCmd(self.shooter)
        self.stopShooterCmd = ShooterStopCmd(self.shooter)

        # Drive commands
        self.arcadeDriveCmd = ArcadeDriveCmd(self.robotDrive, self.driverController)

        # Command groups
        #self.collectAndRetractCmd = SequentialCommandGroup(self.collectCmd, self.retractCmd)
        self.intakeCommandGroup = SequentialCommandGroup(self.intakeStartCmd, self.detectNoteCmd, self.retractCmd)
        # self.intakeCommandGroup = SequentialCommandGroup(self.intakeStartCmd, self.detectNoteCmd, self.stopIntakeCmd)

        # Configure buttons
        self.configureButtonBindings()
        
        # Set up default commands for subsystems
        self.robotDrive.setDefaultCommand(self.arcadeDriveCmd)
        # self.arm.setDefaultCommand(???)
        # self.intake.setDefaultCommand(???)
        # self.shooter.setDefaultCommand(???)


    def configureButtonBindings(self):
        # Button A binding

        # Button B binding
        # self.driverController.b().toggleOnTrue(self.collectAndRetractCmd)
        # self.driverController.b().toggleOnTrue(self.collectCmd)  # Test simple intake
        # self.driverController.b().onTrue(IntakeAndRetractCommand(self.intake, -0.5, 2.0))
        self.driverController.b().onTrue(self.intakeCommandGroup)

        # Button X binding
        self.driverController.x().onTrue(self.expelNoteCmd)

        # Button Y binding

        # Right bumper binding

        # Left bumper binding

        # Right trigger binding 
        self.rightTriggerPressed.whileTrue(self.startShooterCmd)
        self.rightTriggerPressed.negate().whileTrue(SequentialCommandGroup(
            self.deliverNoteCmd,
            self.stopShooterCmd,
            self.stopIntakeCmd
        ))

        # Left trigger binding

        # Start button binding

        # "Back" button binding. (This looksl ike the menu button)

        

    def updateHardware(self):
        self.robotDrive.updateHardware()
        self.arm.updateHardware()
        self.intake.updateHardware()
        self.shooter.updateHardware()

    def cacheSensors(self):
        self.robotDrive.cacheSensors()
        self.arm.cacheSensors()
        self.intake.cacheSensors()
        self.shooter.cacheSensors()

    def getAutonomousCommand(self):
        return commands2.cmd.none()
