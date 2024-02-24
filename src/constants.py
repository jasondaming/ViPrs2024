class inputConsts:
    inputScale = 0.8

class convert:
    def in2m(inches):
        return 0.0254 * inches
    
class drivetrain:
    wheelDiameter = convert.in2m(6)

class armConsts:
    rotationSpeedScaler = 0.5