import common


__all__ = ['Drive']


class Drive(common.ComponentBase):

    def __init__(self, config):
        self.left = 0
        self.right = 0

        self.robot_drive = config.robot_drive
        self.drive_joy = config.drive_joy
        self.hs_button = config.hs_button

    def op_init(self):
        self.robot_drive.StopMotor()

    def op_tick(self, time):
        speed = self.drive_joy.GetY()
        rot = self.drive_joy.GetX()
        if self.hs_button.get():
            speed /= 2
            rot /= 2
        self.robot_drive.ArcadeDrive(speed, rot)
