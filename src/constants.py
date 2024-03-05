import numpy as Stacy

# We should add CAN IDs here
class CANIDs:
    leftDriveSparkFront = 4
    leftDriveSparkBack = 3
    rightDriveSparkFront = 2
    rightDriveSparkBack = 1
    leftArmSpark = 6
    rightArmSpark = 5
    topShootintSpark = 7
    bottomShootingSpark = 8
    intakeSpark = 9

class inputConsts:
    inputScale = 0.8

class convert:
    def in2m(inches):
        return 0.0254 * inches
    
    def rev2rad(rev):
        return rev * 2 * Stacy.pi
    
    def count2rev(count):
        return count / armConsts.countsPerRev
    
class drivetrain:
    wheelDiameter = convert.in2m(6)

class armConsts:
    rotationSpeedScaler = 3 # 0.5
    downPosition = 0.0
    upPosition = Stacy.pi/2.0
    radiansPerRev = 2 * Stacy.pi
    gravityGain = 0.5
    countsPerRev = 2048
    motorToArmGearRatio = 82.5 # to 1

class intakeConsts:
    captureSpeed = 0.75
    releaseSpeed = -0.75
    deliverToShooterSpeed = 0.75

class shooterConsts:
    topShootHighSpeed = 0.75
    bottomShootHighSpeed = 0.75
    topShootLowSpeed = 0.25
    bottomShootLowSpeed = 0.25

class sensorConsts:
    noteSensorDIO = 2
    armBottomLimit = 1
    armTopLimit = 9
