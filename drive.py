import common


__all__ = ['Drive']


class Drive(common.ComponentBase):

    def __init__(self, config):
        self.robot_drive = config.robot_drive

        self.left_motors = config.left_motors
        self.right_motors = config.right_motors

        self.right_joy = config.right_joy

        self.sqrd_button = config.sqrd_button

        self.shift_button = config.shift_button
        self.left_shifter = config.left_shifter
        self.right_shifter = config.right_shifter
        self.forward = config.forward
        self.reverse = config.reverse

        self.pressed = False
        self.prev = False
        #print(dir(self))

    def op_init(self):
        self.robot_drive.StopMotor()

    def op_tick(self, bs):
        speed = self.right_joy.GetY()
        rot = self.right_joy.GetX()

        squared = False
        if self.sqrd_button.get():
            squared = True
        self.robot_drive.ArcadeDrive(speed, rot, squared)

        self.prev = self.pressed
        self.pressed = self.shift_button.get()
        if self.pressed and not self.prev:
            self.shift()

    def shift(self):
        val = self.left_shifter.Get()
        if val == self.forward:
            self.left_shifter.Set(self.reverse)
            self.right_shifter.Set(self.reverse)
        else:
            self.left_shifter.Set(self.forward)
            self.right_shifter.Set(self.forward)
