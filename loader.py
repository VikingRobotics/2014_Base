
__all__ = ['Loader']

class Loader:
    def __init__(self, loadButton, feederServo):
        self.load_button = loadButton
        self.feeder_servo = feederServo

        self.elapsed = 0
        self.end_time = .4
        self.pTime = 0

        self.loading = False

    def load(self):
        if not(self.loading):
            self.feeder_servo.Set(0)
            self.elapsed = 0
            self.loading = True

    def tick(self, time):
        self.elapsed += time - pTime
        self.pTime = time
        if self.load_button.get():
            self.load()
        if self.loading:
            if self.elapsed >= self.end_time:
                self.feeder_servo.Set(1)
                self.loading = False