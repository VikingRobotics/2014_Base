import common

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

__all__ = ['Drive']


class Drive(common.ComponentBase):

    START = 'start'
    DRIVE_FORWARD = 'drive_forward'
    STOP = 'stop'

    def __init__(self, config):
        self.robot_drive = config.robot_drive

        self.left_motors = config.left_motors
        self.right_motors = config.right_motors

        self.joy = config.drive_joy

        self.shift_switch = config.shift_button
        self.left_shifter = config.left_shifter
        self.right_shifter = config.right_shifter

        self.low = config.reverse
        self.high = config.forward
        self.gear = None

        self.auto_state = self.START
        self.auto_drive_start_time = 0

    def op_init(self):
        self.robot_drive.StopMotor()

    def op_tick(self, bs):
        speed = self.joy.GetY()
        rot = self.joy.GetX()

        self.robot_drive.ArcadeDrive(speed, rot)

        if self.shift_switch.get():
            self.shift(self.low)
        else:
            self.shift(self.high)

    def auto_init(self, auto_config):
        self.auto_state = self.START
        self.auto_config = auto_config

    def auto_drive_forward_tick(self, time):
        speed = 0

        if self.auto_state == self.START:
            self.auto_drive_start_time = time
            self.auto_state = self.DRIVE_FORWARD

        elif self.auto_state == self.DRIVE_FORWARD:
            speed = 1
            elapsed_time = time - self.auto_drive_start_time
            if elapsed_time > self.auto_config.drive_seconds:
                speed = 0
                self.auto_state = self.STOP

        elif self.auto_state == self.STOP:
            speed = 0
        
        self.left_motors.Set(speed)
        self.right_motors.Set(-speed)

        wpilib.SmartDashboard.PutString('auto drive state', self.auto_state)
        
    def reset(self):
        self.auto_state = self.START

    def is_auto_drive_done(self):
        return self.auto_state == self.STOP

    def shift(self, gear):
        self.left_shifter.Set(gear)
        self.right_shifter.Set(gear)

    def downshift(self):
        self.shift(self.low)   

    def upshift(self):
        self.shift(self.high)
