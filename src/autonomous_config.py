try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


import config


class MyRobot(wpilib.SimpleRobot):

    ONE_BALL_AUTO = "one ball auto"
    TWO_BALL_AUTO = "two ball auto"

    def __init__(self):
        super().__init__()
        
        self.dog = self.GetWatchdog()
        self.dog.SetExpiration(0.25)
        self.components = config.components()

