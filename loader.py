# This was for the basket ball robot, and I'm still
# not really sure if we actually want it in here or 
# not.... If we are trying to make a comprehensive 
# code base, then I guess it could stay, but right 
# now its just kind-of in the way
import common


__all__ = ['Loader']


class Loader(common.ComponentBase):

    def __init__(self, config):
        self.load_button = config.load_button
        self.feeder_servo = config.feeder_servo

        self.elapsed = 0
        self.end_time = .4
        self.pTime = 0

        self.loading = False


    def op_tick(self, time):
        self.elapsed += time - pTime
        self.pTime = time
        if self.load_button.get():
            self.load()
        if self.loading:
            if self.elapsed >= self.end_time:
                self.feeder_servo.Set(1)
                self.loading = False


    def load(self):
        if not(self.loading):
            self.feeder_servo.Set(0)
            self.elapsed = 0
            self.loading = True
