from constants import States
from enum import Enum, auto

class RobotState:
    def __init__(self):
        # Initialize the states of various subsystems
        self.subsystemStates = {
            "robot": States.IDLE,
            "intake": States.IDLE,
            "shooter": States.IDLE,
            "arm": States.IDLE,
            "drive": States.IDLE,
            # Add more subsystems as necessary
        }

    def setSubsystemState(self, subsystem: str, state: States):
        """Set the state of a specific subsystem."""
        if subsystem in self.subsystemStates:
            self.subsystemStates[subsystem] = state
            print(f"{subsystem} state changed to: {state}")
        else:
            print(f"Subsystem {subsystem} does not exist.")

    def getSubsystemState(self, subsystem):
        """Get the current state of a specific subsystem."""
        return self.subsystemStates.get(subsystem, States.IDLE)

    # Intake subsystem methods
    def startIntakeCollecting(self):
        """Transition the intake subsystem to collecting state."""
        self.setSubsystemState("intake", States.INTAKE_COLLECTING)

    def setIntakeIdle(self):
        """Transition the intake subsystem to idle state."""
        self.setSubsystemState("intake", States.INTAKE_IDLE)

    def startIntakeRetracting(self):
        """Transition the intake subsystem to retracting state."""
        self.setSubsystemState("intake", States.INTAKE_RETRACTING)

    def startIntakeUnjam(self):
        """Transition the intake subsystem to unjamming state."""
        self.setSubsystemState("intake", States.INTAKE_UNJAM)

    def startIntakeEjecting(self):
        """Transition the intake subsystem to ejecting state."""
        self.setSubsystemState("intake", States.INTAKE_EJECTING)

    # Shooter subsystem methods
    def startShooterPrepping(self):
        """Transition the shooter subsystem to prepping state."""
        self.setSubsystemState("shooter", States.SHOOTER_PREPPING)

    def startShooterFiring(self):
        """Transition the shooter subsystem to firing state."""
        self.setSubsystemState("shooter", States.SHOOTER_FIRING)

    def setShooterIdle(self):
        """Transition the shooter subsystem to idle state."""
        self.setSubsystemState("shooter", States.SHOOTER_IDLE)

    # Arm subsystem methods
    def startArmCollecting(self):
        """Transition the arm subsystem to collecting state."""
        self.setSubsystemState("arm", States.ARM_COLLECTING)

    def startArmScoringLow(self):
        """Transition the arm subsystem to scoring low state."""
        self.setSubsystemState("arm", States.ARM_SCORING_LOW)

    def startArmScoringHigh(self):
        """Transition the arm subsystem to scoring high state."""
        self.setSubsystemState("arm", States.ARM_SCORING_HIGH)

    def setArmIdle(self):
        """Transition the arm subsystem to idle state."""
        self.setSubsystemState("arm", States.ARM_IDLE)

    # Add more methods for other subsystems and states as needed

    # Optionally, you could also have a method to check if all subsystems are in a specific state
    def allSubsystemsIdle(self):
        return all(state == States.IDLE for state in self.subsystemStates.values())
