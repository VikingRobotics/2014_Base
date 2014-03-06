import common


__all__ = ['Pickup']


class Pickup(common.ComponentBase):
    
    def __init__(self, config):
        self.motor = config.pickup_motor
        
        self.solenoid = config.solenoid
        self.OUT = config.forward
        self.IN = config.reverse

        self.pickup_switch = config.pickup_switch
        self.motor_button = config.motor_button

        self.pass_slow_preset = config.pass_slow_preset
        self.pass_fast_preset = config.pass_fast_preset
        self.pickup_slow_preset = config.pickup_slow_preset
        self.pickup_fast_preset = config.pickup_fast_preset

        self.pickup_state = -1
        self.start_time = 0
        self.is_extending = False

        self.EXTEND_SPIN_TIME = .3
        self.EXTEND_SPIN_SPEED = .5

    def op_init(self):
        pass

    def op_tick(self, time):
        speed = 0

        prev_state = self.pickup_state
        self.pickup_state = self.solenoid.Get()
        
        # If the pickup is extending
        if prev_state == self.IN and self.pickup_state == self.OUT:
            self.is_extending = True
            self.start_time = time

        elapsed_time = time - self.start_time
        if self.is_extending 
            if elapsed_time < self.EXTEND_SPIN_TIME:
                speed = self.EXTEND_SPIN_SPEED
            else: 
                # we're done extending
                self.is_extending = False

        if self.motor_button.get():
            if self.pass_fast_preset.get():
                speed = -1
            elif self.pass_slow_preset.get():
                speed = -.5
            elif self.pickup_slow_preset.get():
                speed = .25
            elif self.pickup_fast_preset.get():
                speed = .8

        self.motor.Set(speed)
        
        if self.pickup_switch.get():
            self.extend()
        else:
            self.retract()

    def extend(self):
        self.solenoid.Set(self.OUT)

    def retract(self):
        self.solenoid.Set(self.IN)

    def is_extended(self):
        return self.solenoid.Get() == self.self.OUT 

    def pickup_slow(self):
        # TODO: make this value configurable
        self.motor.Set(.25)

    def pickup_fast(self):
        # TODO: make this value configurable
        self.motor.Set(.8)
