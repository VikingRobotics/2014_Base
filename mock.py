

class Button(object):

    def __init__(self):
        self.pressed = False

    def get(self):
        return self.pressed


class Joystick(object):

    def __init__(self):
        self.x = 0
        self.y = 0

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y


class DigitalInput(object): # Changed from PhotoSensor for limit switches

    def __init__(self):
        self.state = False

    def Get(self):
        return self.state


class Motor(object):

    def __init__(self):
        self.speed = 0

    def Set(self, speed):
        self.speed = speed

    def Get(self):
        return self.speed


class RobotDrive(object):

    def __init__(self):
        self.speed = 0
        self.rotation = 0

        self.left_speed = 0
        self.right_speed = 0
        self.squared = False

    def ArcadeDrive(self, speed, rotation, squared=None):
        self.speed = speed
        self.rotation = rotation
        self.squared = squared

    def StopMotor(self):
        self.speed = 0
        self.rotation = 0

    def SetLeftRightMotorOutputs(self, leftOutput,  rightOutput):
        return
        # Not really sure what we want to do with this, but it'll have to be something

    def SetInvertedMotor(self, idx, invert_state):
        pass

    def TankDrive(self, left_speed, right_speed, squared):
        self.left_speed = left_speed
        self.right_speed = right_speed
        self.squared = squared


class Servo(object):

    def __init__(self):
        self.angle = 0

    def Set(self, angle):
        self.angle = angle

    def Get(self):
        return self.angle
