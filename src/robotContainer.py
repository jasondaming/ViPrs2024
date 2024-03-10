
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
from commands.shooter.shooterStartCmd import Shooter
from commands.drive.arcadeDriveCmd import ArcadeDriveCommand
from constants import States, intakeConsts, inputConsts
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

        # Command inits

        # Intake commands
        self.collectCmd = IntakeCollectNoteCmd(self.intake, intakeConsts.captureSpeed)
        self.retractCmd = IntakeRetractNoteCmd(self.intake, intakeConsts.releaseSpeed, intakeConsts.retractTime)  # Example values for retract speed and time
        self.intakeAndRetractCommand = IntakeAndRetractCommand(self.intake, intakeConsts.releaseSpeed, intakeConsts.retractTime)
        self.intakeStartCmd = IntakeStartCmd(self.intake, intakeConsts.captureSpeed)
        self.stopIntakeCmd = StopIntakeCmd(self.intake)
        self.detectNoteCmd = DetectNoteCmd(self.intake)
        self.expelNoteCmd = IntakeExpelNoteCmd(self.intake, intakeConsts.expelSpeed, intakeConsts.expelTime)

        # Shooter commands
        self.

        # Drive commands
        self.arcadeDriveCmd = ArcadeDriveCommand(self.robotDrive, self.driverController)

        # Command groups
        #self.collectAndRetractCmd = SequentialCommandGroup(self.collectCmd, self.retractCmd)
        self.intakeCommandGroup = SequentialCommandGroup(self.intakeStartCmd, self.detectNoteCmd, self.retractCmd)
        # self.intakeCommandGroup = SequentialCommandGroup(self.intakeStartCmd, self.detectNoteCmd, self.stopIntakeCmd)
        se

        # Configure buttons
        self.configureButtonBindings()
        
        # Set up default commands for subsystems
        self.robotDrive.setDefaultCommand(self.arcadeDriveCmd)
        # self.arm.setDefaultCommand(???)
        # self.intake.setDefaultCommand(???)
        # self.shooter.setDefaultCommand(???)


    def configureButtonBindings(self):
        # Bind the collectAndRetractCmd object to the B button press
        # self.driverController.b().toggleOnTrue(self.collectAndRetractCmd)
        # self.driverController.b().toggleOnTrue(self.collectCmd)  # Test simple intake
        # self.driverController.b().onTrue(IntakeAndRetractCommand(self.intake, -0.5, 2.0))
        self.driverController.b().onTrue(self.intakeCommandGroup)

        self.driverController.x().onTrue(self.expelNoteCmd)


        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!! TESTING CODE --- TEMPORARY
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # print(f"self.arm -> {self.arm}")
        self.driverController.a().whileTrue( 
            commands2.cmd.run(
                #lambda: print("A button pressed, going to 0.4"), self.arm.goto(0.4)
                lambda: self.arm.goto(0.4)
            )
        ).whileFalse(
            commands2.cmd.run(
                #lambda: print("A button not pressed, going to 0.0"), self.arm.goto(0.0)
                lambda: self.arm.goto(0.0)
            )
        )
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!! TESTING CODE --- TEMPORARY
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
