import common


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    def __init__(self, config):
        self.motors = config.motors
        self.shoot_button = config.shoot_button
        self.stop_buttons = config.stop_buttons
        self.stop_inputs = config.stop_inputs
        self.reset_stop = config.reset_stop
        self.max_throw_time = config.max_throw_time

        self.current_stop = 0
        self.throw_start_time = 0.0

        self.pressed = False

    def op_init(self):
        self.motors.Set(0)

    def op_tick(self, time):

        throw_time = time - self.throw_start_time

        speed = 0

        if not throw_time >= self.max_throw_time:
            prev = self.pressed
            self.pressed = self.shoot_button.get()

            if not prev and self.pressed:
                self.reseting = False
                self.current_stop = self.get_current_stop()
                self.throw_start_time = time

            if not self.should_stop(self.current_stop) and not self.reseting:
                speed = 1
            else:
                self.reseting = True

            if self.reseting:
                self.throw_start_time = time
                if self.reset_stop.Get():
                    speed = 0
                else:
                    speed = -.1

        print(speed)

        """
        When we are all in agreement that this code won't blow things up
        uncomment the line below to enable actual movement of the Shooter
        arm.
        I would suggest pretty thoroughly testing this by manually moving
        the arm along the sensors and editing until the desired behavior
        is achieved.
        """
        #self.motors.Set(speed)



    def get_current_stop(self):
        for idx, button in enumerate(self.stop_buttons):
            if button.get():
                return idx

        # If we don't detect any buttons go for the most restrictive.
        # That way if the switch malfunctions or we don't read it, we just
        # stop.
        return 0

    def should_stop(self, current_stop):
        for idx, stop_input in enumerate(self.stop_inputs):
            if stop_num >= idx and stop_input.Get():
                return True

        return False

