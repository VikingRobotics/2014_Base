try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class AutoConfig(object):
    ONE_BALL_AUTO = "one_ball_auto"
    TWO_BALL_AUTO = "two_ball_auto"

    shift_seconds = .3
    after_drive_pause_seconds = 1

    # drive_seconds is the only one that's used. It's set using
    # the one_ball_drive_seconds or two_ball_drive_seconds,
    # depending on smart dashboard choice. This happens in robot.py
    drive_seconds = 0 
    one_ball_drive_seconds = 3
    # two_ball_drive_seconds = 4 # Low gear config
    two_ball_drive_seconds = 1.8 # High gear config

    # Drive distance is unused until we get PIDControllers working
    drive_distance = 13

    pre_shot_pickup_stop = .3
    extending_seconds = 1.3
    after_shoot_seconds = .3
    pickup_seconds = .5

    def __init__(self):
        super().__init__()

        # Smartdashboard code to choose autonomous mode
        self.auto_chooser = wpilib.SendableChooser()
        self.auto_chooser.AddDefault("One ball autonomous", self.ONE_BALL_AUTO)
        self.auto_chooser.AddObject("Two ball autonomous", self.TWO_BALL_AUTO)
        
        wpilib.SmartDashboard.PutData("Autonomous mode chooser", self.auto_chooser)

        wpilib.SmartDashboard.PutNumber("auto shift_seconds", self.shift_seconds)
        wpilib.SmartDashboard.PutNumber("auto one_ball_drive_seconds", self.one_ball_drive_seconds)
        wpilib.SmartDashboard.PutNumber("auto two_ball_drive_seconds", self.two_ball_drive_seconds)
        wpilib.SmartDashboard.PutNumber("auto drive_distance", self.drive_distance)
        wpilib.SmartDashboard.PutNumber("auto after_drive_pause_seconds", self.after_drive_pause_seconds)
        wpilib.SmartDashboard.PutNumber("auto extending_seconds", self.extending_seconds)
        wpilib.SmartDashboard.PutNumber("auto after_shoot_seconds", self.after_shoot_seconds)
        wpilib.SmartDashboard.PutNumber("auto pickup_seconds", self.pickup_seconds)
        wpilib.SmartDashboard.PutNumber("auto pre_shot_pickup_stop", self.pre_shot_pickup_stop)

    def update_smartdashboard_vars(self):
        self.shift_seconds = wpilib.SmartDashboard.GetNumber("auto shift_seconds")
        self.one_ball_drive_seconds = wpilib.SmartDashboard.GetNumber("auto one_ball_drive_seconds")
        self.two_ball_drive_seconds = wpilib.SmartDashboard.GetNumber("auto two_ball_drive_seconds")
        self.after_drive_pause_seconds = wpilib.SmartDashboard.GetNumber("auto after_drive_pause_seconds")
        self.drive_distance = wpilib.SmartDashboard.GetNumber("auto drive_distance")
        self.extending_seconds = wpilib.SmartDashboard.GetNumber("auto extending_seconds")
        self.after_shoot_seconds = wpilib.SmartDashboard.GetNumber("auto after_shoot_seconds")
        self.pickup_seconds = wpilib.SmartDashboard.GetNumber("auto pickup_seconds")
        self.pre_shot_pickup_stop = wpilib.SmartDashboard.GetNumber("auto pre_shot_pickup_stop")
    
    def get_autonomous_mode(self):
        return self.auto_chooser.GetSelected()

    def is_goal_hot(self):
        return True
        # try:
        #     hot_goal = wpilib.SmartDashboard.GetBoolean("HOT_GOAL")
        #     return hot_goal
        # except:
        #     return False

