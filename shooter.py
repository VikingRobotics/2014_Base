import common

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    SHOOTING = 0
    RESET = 1 
    RESETTING = 2

    def __init__(self, config):
        self.motors = config.motors

        self.shoot_button = config.shoot_button

        self.stop_buttons = config.stop_buttons
        
        self.stop_counters = config.stop_counters


        self.reset_stop = config.reset_stop
    
        self.state = self.RESETTING

        self.stop_pos = -1


    def op_init(self):
        for counter in self.stop_counters:
            counter.Reset()

        self.state = self.RESETTING 

    def op_tick(self, time):

        wpilib.SmartDashboard.PutNumber("shooter state", self.state)
        wpilib.SmartDashboard.PutNumber("current preset", self.get_current_stop())
        for idx, counter in enumerate(self.stop_counters):
            wpilib.SmartDashboard.PutBoolean("hall effect counter %d" % idx , counter.Get())

        if self.state == self.RESET:
            speed = 0
            if self.shoot_button.get():
                self.state = self.SHOOTING
                self.stop_pos = self.get_current_stop()
                for counter in self.stop_counters:
                    counter.Reset()

        if self.state == self.SHOOTING:
            speed = 1
            if self.should_stop(self.stop_pos):
                speed = 0
                self.state = self.RESETTING
                self.stop_pos = -1

        if self.state == self.RESETTING:
            speed = -.1
            if self.should_stop(self.stop_pos):
                speed = 0
                self.state = self.RESET

    def get_current_stop(self):
        for idx, button in enumerate(self.stop_buttons):
            if button.get():
                return idx

        # If we don't detect any buttons go for the most restrictive.
        # That way if the switch malfunctions or we don't read it, we just
        # stop.
        return 0


    def should_stop(self, stop_pos):
        if stop_pos == -1 and self.reset_stop.Get():
            return True

        for idx, counter in enumerate(self.stop_counters):
            # 0 is False and positve is True
            if idx >= stop_pos and counter.Get(): 
                return True

        return False
