import common


__all__ = ['Drive']


class Drive(common.ComponentBase):

    def __init__(self, config):
        self.robot_drive = config.robot_drive
        self.left_joy = config.left_joy
        self.right_joy = config.right_joy
        self.sqrd_button = config.sqrd_button
        self.tank_button = config.tank_button

        self.isTank = True
        self.pressed = False
        self.prev = False

    def op_init(self):
        self.robot_drive.StopMotor()

    def op_tick(self, timestamp):
        squared = False
        speed = self.right_joy.GetY()
        rot = self.right_joy.GetX()

        if self.sqrd_button.get():
            squared = True

        if self.check_tank():
            self.robot_drive.TankDrive(self.right_joy.GetY(), -1*self.left_joy.GetY(), squared)
        else:
            self.robot_drive.ArcadeDrive(speed, rot, squared)

    def check_tank(self):
        self.prev = self.pressed
        self.pressed = self.tank_button.get()

        if self.pressed and not self.prev:
            self.isTank = not self.isTank
            self.robot_drive.SetInvertedMotor(1, self.isTank)
            self.robot_drive.SetInvertedMotor(2, self.isTank)

        return self.isTank
