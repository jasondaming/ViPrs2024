from team4646.PID import PID
from team254.LazySparkMax import LazySparkMax

from rev import CANSparkMax, CANSparkLowLevel, SparkMaxPIDController, REVLibError
from wpilib import Timer, DriverStation

class SparkMaxFactory:
    class Configuration:
        def __init__(self):
            print(f"SparkMaxFactory Configuration Subclass constructor{self}")
            self.BURN_FACTORY_DEFAULT_FLASH = True
            self.NEUTRAL_MODE = CANSparkMax.IdleMode.kCoast
            self.INVERTED = False
            # Note: Status frame rates might not be directly configurable via RobotPy,
            # or the method to do so could differ.
            self.STATUS_FRAME_0_RATE_MS = 10
            self.STATUS_FRAME_1_RATE_MS = 1000
            self.STATUS_FRAME_2_RATE_MS = 1000
            self.OPEN_LOOP_RAMP_RATE = 0.0
            self.CLOSED_LOOP_RAMP_RATE = 0.0
            self.ENABLE_VOLTAGE_COMPENSATION = False
            self.NOMINAL_VOLTAGE = 12.0

    kDefaultConfiguration = Configuration()
    kSlaveConfiguration = Configuration()

    @staticmethod
    def setPID(controller, PID):
        # Assuming 'PID' is an object with attributes P, I, D, and F
        controller.setP(PID.P)
        controller.setI(PID.I)
        controller.setD(PID.D)
        controller.setFF(PID.F)

    @staticmethod
    def createDefaultSparkMax(id, inverted=False):
        print(f"createDefaultSparkMax({id}, {inverted})")
        return SparkMaxFactory.createSparkMax(id, SparkMaxFactory.kDefaultConfiguration, inverted)

    @staticmethod
    def createPermanentSlaveSparkMax(id, master, inverted):
        print("createPermanentSlaveSparkMax called")
        # Method to configure a SparkMax as a follower of another SparkMax
        sparkMax = SparkMaxFactory.createSparkMax(id, SparkMaxFactory.kSlaveConfiguration)
        SparkMaxFactory.handleCANError(id, sparkMax.follow(master, invert=inverted), "setting follower")
        return sparkMax

    @staticmethod
    def createSparkMax(id, config, inverted=False):
        print(f"createSparkMax({id}, {config}, {inverted}) called")
        # Timer.delay(0.25)  # Delay for CAN bus bandwidth
        # sparkMax = CANSparkMax(id, CANSparkMax.MotorType.kBrushless)
        sparkMax = LazySparkMax(id)
        
        sparkMax.restoreFactoryDefaults()

        SparkMaxFactory.handleCANError(id, sparkMax.setCANTimeout(200), "set timeout")
        sparkMax.set(CANSparkLowLevel.ControlType.kDutyCycle, 0.0)

        SparkMaxFactory.handleCANError(id, sparkMax.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus0, config.STATUS_FRAME_0_RATE_MS), "set status0 rate")
        SparkMaxFactory.handleCANError(id, sparkMax.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus1, config.STATUS_FRAME_1_RATE_MS), "set status1 rate")
        SparkMaxFactory.handleCANError(id, sparkMax.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus2, config.STATUS_FRAME_2_RATE_MS), "set status2 rate")
        
        sparkMax.clearFaults()

        SparkMaxFactory.handleCANError(id, sparkMax.setIdleMode(config.NEUTRAL_MODE), "set neutrual")
        SparkMaxFactory.handleCANError(id, sparkMax.setOpenLoopRampRate(config.OPEN_LOOP_RAMP_RATE), "set open loop ramp")
        SparkMaxFactory.handleCANError(id, sparkMax.setClosedLoopRampRate(config.CLOSED_LOOP_RAMP_RATE), "set closed loop ramp")


        if config.ENABLE_VOLTAGE_COMPENSATION:
            SparkMaxFactory.handleCANError(id, sparkMax.enableVoltageCompensation(config.NOMINAL_VOLTAGE), "voltage compensation");
        else:
            SparkMaxFactory.handleCANError(id, sparkMax.disableVoltageCompensation(), "voltage compensation");

        return sparkMax

    @staticmethod
    def handleCANError(id, error, message):
        if error is not None:  # Assuming 'error' indicates an issue if not None
            print(f"Could not configure spark id: {id} error: {error} {message}")
            #DriverStation.reportError(f"Could not configure spark id: {id} error: {error} {message}", False)
