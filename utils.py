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




##    self.attributes = []
##    self.input_stack = []

##    def __init__(self, real_config):
##        self.config = real_config()
##        _attributes = dir(config)
##        self.mocks = {}
##        self.inputs = []
##        for attribute in _attributes:
##            _type = type(attribute)
##            if attribute[0] != '_' and _type in input_dict:
##                self.mocks[attribute] = input_dict[_type]()
##                self.config.attribute = self.mocks[attribute]
##                self.inputs.append(attribute)
