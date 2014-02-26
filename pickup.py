import common


__all__ = ['Pickup']


class Pickup(common.ComponentBase):
    
    def __init__(self, config):
        self.motor = config.pickup_motor
        
        self.solenoid = config.solenoid
        self.forward = config.forward
        self.reverse = config.reverse

        self.pickup_switch = config.pickup_switch
        self.motor_button = config.motor_button

        self.pass_slow_preset = config.pass_slow_preset
        self.pass_fast_preset = config.pass_fast_preset
        self.pickup_slow_preset = config.pickup_slow_preset
        self.pickup_fast_preset = config.pickup_fast_preset

    def op_init(self):
        pass

    # TODO: Make the pickup spin while dropping or upping the loader
    # How do we do this since the pneumatics can't tell if they're 
    # operating or not? Timeout!
    def op_tick(self, time):
        speed = 0
        if self.motor_button.get():
            if self.pass_slow_preset.get():
                speed = -.5
            elif self.pass_fast_preset.get():
                speed = -1
            elif self.pickup_slow_preset.get():
                speed = .25
            elif self.pickup_fast_preset.get():
                speed = .5

        self.motor.Set(speed)
    
        if self.pickup_switch.get():
            self.solenoid.Set(self.forward)
        else:
            self.solenoid.Set(self.reverse)




