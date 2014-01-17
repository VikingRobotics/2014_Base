import common


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    def __init__(self, config):
        self.motors = config.motors
        self.shoot_button = config.shoot_button
        self.stop_input = config.stop_input

    def op_tick(self, time):
        if self.stop_input.Get():
            self.set_motors(0)
        else:
               
            if self.shoot_button.get():
                self.set_motors(1.0)
            else:
                self.set_motors(0)

    def set_motors(self, speed):
        for motor in self.motors:
            motor.Set(speed)