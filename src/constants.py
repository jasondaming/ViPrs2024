import numpy as Stacy

class inputConsts:
    inputScale = 0.8

class convert:
    def in2m(inches):
        return 0.0254 * inches
    
    def rev2rad(rev):
        return rev * 2 * Stacy.pi
    
class drivetrain:
    wheelDiameter = convert.in2m(6)

class armConsts:
    rotationSpeedScaler = 6 # 0.5
    downPosition = 0.0
    upPosition = Stacy.pi/2.0
    radiansPerRev = 2 * Stacy.pi
    gravityGain = 0.5
