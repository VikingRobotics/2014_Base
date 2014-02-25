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

        self.speed_array = config.speed_array

    def op_init(self):
        pass

    # TODO: Make the pickup spin while dropping or upping the loader
    # How do we do this since the pneumatics can't tell if they're 
    # operating or not? Timeout!
    def op_tick(self, time):
        speed = 0
        if self.motor_button.get():
            speed = -1
            for idx, button in enumerate(self.speed_array):
                if button.get():
                    speed_num = idx
                    speed += speed_num * .5

                    # TODO: fix this guy. It's temporary
                    if idx == 2:
                        speed = 1

        self.motor.Set(speed)
    
        if self.pickup_switch.get():
            self.solenoid.Set(self.forward)
        else:
            self.solenoid.Set(self.reverse)




