'''
    This test module imports tests that come with pyfrc, and can be used
    to test basic functionality of just about any robot.
'''

#from pyfrc.tests import test_autonomous
#from pyfrc.tests import test_disabled
from pyfrc.tests import test_operator_control
#from pyfrc.tests import test_practice

'''
import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from commands2 import CommandScheduler
from subSystems.intakeSubsystem import IntakeSubsystem
from commands.intakeCollectNoteCmd import IntakeCollectNoteCmd

@pytest.fixture
def intake_subsystem():
    subsystem = IntakeSubsystem()
    subsystem.setIntakeSpeed = MagicMock()
    subsystem.hasGamePiece = MagicMock(return_value=False)  # Initially, no game piece
    return subsystem

@pytest.fixture
def intake_command(intake_subsystem):
    return IntakeCollectNoteCmd(intake_subsystem, targetSpeed=0.5)

def test_intake_collect_note(intake_subsystem, intake_command):
    CommandScheduler.getInstance().schedule(intake_command)
    # Run the scheduler enough times for execute to be called
    for _ in range(5):
        CommandScheduler.getInstance().run()

    # Verify setIntakeSpeed was called with the target speed
    intake_subsystem.setIntakeSpeed.assert_called_with(0.5)

    # Now simulate game piece acquisition
    intake_subsystem.hasGamePiece.return_value = True

    # Reset mock to check for subsequent calls
    intake_subsystem.setIntakeSpeed.reset_mock()

    # Run the scheduler to process the command completion
    for _ in range(5):
        CommandScheduler.getInstance().run()

    # Verify that the intake stops after detecting the game piece
    intake_subsystem.setIntakeSpeed.assert_called_with(0)
'''

