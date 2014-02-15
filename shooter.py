import common


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    def __init__(self, config):
        self.motors = config.motors

        self.shoot_button = config.shoot_button

        self.stop_buttons = config.stop_buttons
        
        self.stop_inputs = config.stop_inputs
        self.reset_stop = config.reset_stop

        self.state = 'reseting'

        self.stop_pos = -1

    def op_tick(self, time):
        wpilib.SmartDashboard.PutString("shooter state", self.state)
        wpilib.SmartDashboard.PutNumber("current preset", self.get_current_stop())
         for idx, hall in enumerate(self.stop_inputs):
            wpilib.SmartDashboard.PutBoolean("hall effect %d" % idx , hall.Get())
                return True

        if self.state == 'reset':
            speed = 0
            if shoot_button.get():
                self.state = 'shooting'
                self.stop_pos = self.get_current_stop()

        if self.state == 'shooting':
            speed = 1
            if self.should_stop(self.stop_pos):
                speed = 0
                self.state = 'reseting'
                self.stop_pos = -1

        if self.state == 'reseting':
            speed = -.1
            if self.should_stop(self.stop_pos):
                speed = 0
                self.state = 'reset'


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

        for idx, hall in enumerate(self.stop_inputs):
            if idx >= stop_pos and hall.Get():
                return True

        return False
