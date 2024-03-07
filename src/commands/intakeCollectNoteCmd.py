import wpilib
import commands2
import commands2.cmd

from subSystems.intakeSubsystem import IntakeSubsystem

import constants

class IntakeCollectNoteCmd(CommandBase):
    def __init__(self, intake: IntakeSubsystem, targetSpeed: float):
        super().__init__()
        self.intake = intake
        self.targetSpeed = targetSpeed
        self.addRequirements([self.intake])

    def execute(self):
        self.intake.setIntakeSpeed(self.targetSpeed)

    def isFinished(self):
        # Assume hasGamePiece() returns True when the note is detected
        return self.intake.hasGamePiece()

    def end(self, interrupted):
        # Optionally, stop the intake here or leave it for the retract command
        self.intake.setIntakeSpeed(0)


"""
### IntakeCollectNoteCmd
**Parameters:**
targetSpeed: (float) Target speed to spin the intake system at. Defaults to the constant captureSpeed
intake: (IntakeSubsystem)  Reference to the IntakeSubsystem

**Description:**
This command runs the intake until it detects a captured note.
"""
"""
class IntakeCollectNoteCmd(commands2.CommandBase):
    #A command that will be used when collecting notes from the ground

    def __init__(self, targetSpeed = constants.intakeConsts.captureSpeed: float, intake: IntakeSubsystem) -> None:
        #Turns the intake to the specified speed
        
        #:param: targetSpeed the speed to set the intake to
        #:param: intake The intake subsystem
        
    
        super().__init__()

        self.subsystem = IntakeSubsystem
        self.setpoint = targetSpeed 
    
"""