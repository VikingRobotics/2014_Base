import common


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    def __init__(self, config):
        self.motors = config.motors
        self.shoot_button = config.shoot_button
        self.stop_input = config.stop_input

    def op_tick(self, time):
        if self.stop_input.Get():
            for motor in self.motors:
                motor.Set(0)
        else:
               
            if self.shoot_button.get():
                for motor in self.motors:
                    motor.Set(1.0)
            else:
                for motor in self.motors:
                    motor.Set(0)
