try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class AutoConfig(object):
    ONE_BALL_AUTO = "one_ball_auto"
    TWO_BALL_AUTO = "two_ball_auto"

    downshift_seconds = .5
    after_drive_pause_seconds = 1.5
    # drive_forward_seconds = 1.5 
    drive_distance = 1
    extending_seconds = 1.3
    after_shoot_seconds = .1
    pickup_seconds = 1

    def __init__(self):
        super().__init__()

        # Smartdashboard code to choose autonomous mode
        self.auto_chooser = wpilib.SendableChooser()
        self.auto_chooser.AddDefault("One ball autonomous", self.ONE_BALL_AUTO)
        self.auto_chooser.AddObject("Two ball autonomous", self.TWO_BALL_AUTO)
        
        wpilib.SmartDashboard.PutData("Autonomous mode chooser", self.auto_chooser)

        wpilib.SmartDashboard.PutNumber("auto downshift_seconds", self.downshift_seconds)
        # wpilib.SmartDashboard.PutNumber("drive_forward_seconds", self.drive_forward_seconds)
        wpilib.SmartDashboard.PutNumber("auto drive_distance", self.drive_distance)
        wpilib.SmartDashboard.PutNumber("auto after_drive_pause_seconds", self.after_drive_pause_seconds)
        wpilib.SmartDashboard.PutNumber("auto extending_seconds", self.extending_seconds)
        wpilib.SmartDashboard.PutNumber("auto after_shoot_seconds", self.after_shoot_seconds)
        wpilib.SmartDashboard.PutNumber("auto pickup_seconds", self.pickup_seconds)

    def update_smartdashboard_vars(self):
        self.downshift_seconds = wpilib.SmartDashboard.GetNumber("auto downshift_seconds")
        self.drive_forward_seconds = wpilib.SmartDashboard.GetNumber("auto drive_forward_seconds")
        # self.after_drive_pause_seconds = wpilib.SmartDashboard.GetNumber("after_drive_pause_seconds")
        self.drive_distance = wpilib.SmartDashboard.GetNumber("auto drive_distance")
        self.extending_seconds = wpilib.SmartDashboard.GetNumber("auto extending_seconds")
        self.after_shoot_seconds = wpilib.SmartDashboard.GetNumber("auto after_shoot_seconds")
        self.pickup_seconds = wpilib.SmartDashboard.GetNumber("auto pickup_seconds")
    
    def get_autonomous_mode(self):
        return self.auto_chooser.GetSelected()

    def is_goal_hot(self):
        # return True
        try:
            hot_goal = wpilib.SmartDashboard.GetBoolean("HOT_GOAL")
            return hot_goal
        except:
            return False

