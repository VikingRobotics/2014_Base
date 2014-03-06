try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import common


class Button(object):

    def __init__(self, joystick, buttonNumber):
        self.joy = joystick
        self.button = buttonNumber

    def get(self):
        return self.joy.GetRawButton(self.button)


class Axis(object):

    def __init__(self, joystick, axisNumber):
        self.joy = joystick
        self.axis = axisNumber

    def get(self):
        return self.joy.GetRawAxis(self.axis)


class HallEffect(object):

    def __init__(self, hallEffect):
        self.hallEffect = hallEffect

    def Get(self):
        return not self.hallEffect.Get()

class DistanceEncoder(wpilib.PIDSource):

    def __init__(self, encoder):
        super(DistanceEncoder, self).__init__()
        self.encoder = encoder

    def PIDGet(self):
        return self.encoder.GetDistance()


class RateEncoder(wpilib.PIDSource):
    
    def __init__(self, encoder):
        super.__init__(self)
        self.encoder = encoder

    def PIDGet(self):
        return self.encoder.GetRate()



class ButtonControlledMotor(common.ComponentBase):

    def __init__(self, config):
        self.motor = config.motor
        self.up_button = config.up_button
        self.down_button = config.down_button

    def op_init(self):
        self.motor.Set(0)

    def op_tick(self, time):
        if self.up_button.get():
            if self.down_button.get():
                self.motor.Set(0)
            else:
                self.motor.Set(-1)
        elif self.down_button.get():
            self.motor.Set(1)
        else:
            self.motor.Set(0)
