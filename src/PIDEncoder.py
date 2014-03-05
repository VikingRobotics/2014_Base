import common

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class DistanceEncoder(wpilib.PIDSource):

    def __init__(self, encoder):
        super(DistanceEncoder, self).__init__()
        self.encoder = encoder

    def PIDGet(self):
        return self.encoder.GetDistance()


class RateEncoder(wpilib.PIDSource):
    
    def __init__(self, encoder):
        super.__init__(self)
        self.encoder = encoder

    def PIDGet(self):
        return self.encoder.GetRate()
