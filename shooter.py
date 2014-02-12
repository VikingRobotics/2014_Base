import common


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    def __init__(self, config):
        self.motors = config.motors
        self.shoot_button = config.shoot_button
        self.stop_input = config.stop_input
        self.reset_input = config.reset_input

        self.is_reseting = False
        self.is_shooting = False

    def op_tick(self, time):
        if self.is_reseting:
            if self.reset_input.Get():
                self.set_motors(0)
                self.reset_input = False

        elif self.is_shooting:
            if self.stop_input.Get():
                self.set_motors(-1.0)
                self.is_reseting = True
                self.is_shooting = False

        else:
               
            if self.shoot_button.get():
                self.is_shooting = True
                self.set_motors(1.0)
            
    def set_motors(self, speed):
        for motor in self.motors:
            motor.Set(speed)
