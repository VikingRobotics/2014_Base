import common


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    def __init__(self, config):
        self.motors = config.motors
        self.shoot_button = config.shoot_button
        self.stop_buttons = config.stop_buttons
        self.stop_inputs = config.stop_inputs
        self.reset_stop = config.reset_stop

        self.current_stop = 0

        self.pressed = False

    def op_init(self):
        self.motors.Set(0)

    def op_tick(self, time):
        prev = self.pressed
        self.pressed = self.shoot_button.get()
        if not prev and self.pressed:
            reseting = False

        speed = 0
        self.current_stop = self.get_current_stop()
        if not self.should_stop(self.current_stop) and not self.reseting:
            speed = 1
        else:
            self.reseting = True

        if self.reseting and not self.reset_stop.Get():
            speed = -.1

        print(speed)

        """
        When we are all in agreement that this code won't blow things up 
        uncomment the line below to enable actual movement of the Shooter
        arm.
        I would suggest pretty thuroughly testing this by manually moving
        the arm along the sensors and editing until the desired behavior 
        is acheived.
        """
        #self.motors.Set(speed)
        


    def get_current_stop(self):
        for i in range(len(self.stop_buttons)):
            if self.stop_buttons[i].get():
                return i

    def should_stop(self, current_stop):
        for stop_num in range(len(self.stop_inputs)):
            if stop_num >= current_stop and stop_inputs[stop_num].Get():
                return True

        return False
