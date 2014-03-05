try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class AutoConfig(object):
    ONE_BALL_AUTO = "one_ball_auto"
    TWO_BALL_AUTO = "two_ball_auto"

    after_drive_pause_seconds = 3
    drive_forward_time = 1.2

    def __init__(self):
        super().__init__()
        
        # Smartdashboard code to choose autonomous mode
        self.auto_chooser = wpilib.SendableChooser()
        self.auto_chooser.AddDefault("One ball autonomous", self.ONE_BALL_AUTO)
        self.auto_chooser.AddObject("Two ball autonomous", self.TWO_BALL_AUTO)
        
        wpilib.SmartDashboard.PutData("Autonomous mode chooser", self.auto_chooser)

    def get_autonomous_mode():
        return self.auto_chooser.GetSelected()
