try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class AutoConfig(object):
    ONE_BALL_AUTO = "one_ball_auto"
    TWO_BALL_AUTO = "two_ball_auto"

    # TODO: these can be constants, so we should capitalize em
    # TODO: these values are used for both one-ball and two-ball autonomous
    #       We probably want to change that.
    after_drive_pause_seconds = 1.5
    #drive_forward_seconds = 0.75 #HIGH SHOT PRESET
    drive_forward_seconds = 1.5 #LOW SHOT PRESET
    second_drive_forward_seconds = 0
    #drive_forward_seconds = 2.5 #SHORT HIGH SHOT PRESET
    extending_seconds = 1.3
    after_shoot_seconds = .1
    pickup_seconds = 1

    def __init__(self):
        super().__init__()
        self.smartdashboardNT = wpilib.NetworkTable.GetTable("SmartDashboard")
        # Smartdashboard code to choose autonomous mode
        self.auto_chooser = wpilib.SendableChooser()
        self.auto_chooser.AddDefault("One ball autonomous", self.ONE_BALL_AUTO)
        self.auto_chooser.AddObject("Two ball autonomous", self.TWO_BALL_AUTO)
        
        wpilib.SmartDashboard.PutData("Autonomous mode chooser", self.auto_chooser)

    def get_autonomous_mode(self):
        return self.auto_chooser.GetSelected()

    def is_goal_hot(self):
        return True
        # try:
        #     hot_goal = self.smartdashboardNT.GetBoolean("HOT_GOAL")
        #     return hot_goal
        # except:
        #     return False

