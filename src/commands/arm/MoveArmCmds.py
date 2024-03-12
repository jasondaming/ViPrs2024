import commands2
from subSystems.armSubsystem import ArmSubsystem
from constants import armConsts

class MoveArmToAngle(commands2.Command):
    def __init__(self, arm: ArmSubsystem, angle: float):
        super().__init__()
        self.arm = arm
        self.angle = angle
        self.addRequirements(self.arm)

    def initialize(self):
        self.arm.goto(self.angle)

    def isFinished(self):
        # You might want to check if the arm has reached the target angle.
        # This could be done by checking the current position vs the target
        # and seeing if it's within an acceptable range.
        # For now, we'll just let it run without a specific end condition here.
        return False

class MoveArmToStartingPosition(MoveArmToAngle):
    def __init__(self, arm: ArmSubsystem):
        super().__init__(arm, armConsts.startingAngle) # Define this angle in your ArmSubsystem

class MoveArmToScoreHigh(MoveArmToAngle):
    def __init__(self, arm: ArmSubsystem):
        super().__init__(arm, armConsts.speakerAngle) # Define this angle in your ArmSubsystem

class MoveArmToScoreLow(MoveArmToAngle):
    def __init__(self, arm: ArmSubsystem):
        super().__init__(arm, armConsts.ampAngle) # Define this angle in your ArmSubsystem

class MoveArmToIntakePosition(MoveArmToAngle):
    def __init__(self, arm: ArmSubsystem):
        super().__init__(arm, armConsts.intakeAngle) # Define this angle in your ArmSubsystem
