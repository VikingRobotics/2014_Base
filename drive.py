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

        self.pid_button = config.squared_drive_stick

        self.shift_switch = config.shift_button
        self.left_shifter = config.left_shifter
        self.right_shifter = config.right_shifter
        self.high = config.reverse
        self.low = config.forward
        self.gear = None

        self.align_button = config.align_button
        self.front_left_photo_switch = config.front_left_photo_switch
        self.front_right_photo_switch = config.front_right_photo_switch
        self.back_left_photo_switch = config.back_left_photo_switch
        self.back_right_photo_switch = config.back_right_photo_switch


        self.prev_shift_button_val = False
        #print(dir(self))

        self.auto_state = self.START
        self.auto_drive_start_time = 0

        self.AUTO_DRIVE_FORWARD_TIME = 1

    def op_init(self):
        self.robot_drive.StopMotor()

    def op_tick(self, bs):
        speed = self.joy.GetY()
        rot = self.joy.GetX()

        self.robot_drive.dissable_pid()
        if self.pid_button.get():
            self.robot_drive.enable_pid()

        self.robot_drive.ArcadeDrive(speed, rot)

        if self.shift_switch.get():
            self.shift(self.high)
        elif not self.shift_switch.get():
            self.shift(self.low)

        if self.align_button.get():
            self.align()

    def auto_drive_forward_tick(self, time):
        speed = 0

        if self.auto_state == self.START:
            self.auto_drive_start_time = time
            self.auto_state = self.DRIVE_FORWARD

        elif self.auto_state == self.DRIVE_FORWARD:
            speed = 1
            elapsed_time = time - self.auto_drive_start_time
            if elapsed_time > self.AUTO_DRIVE_FORWARD_TIME:
                self.auto_state = self.STOP

        elif self.auto_state == self.STOP:
            speed = 0
        
        self.left_motors.Set(speed)
        self.right_motors.Set(speed)

        wpilib.SmartDashboard.PutString('auto drive state', self.auto_state)

    def is_auto_drive_done(self):
        return self.auto_state == self.STOP

    def shift(self, gear):
        if gear == self.high:
            self.left_shifter.Set(self.high)
            self.right_shifter.Set(self.high)
            self.gear = self.high
        else:
            self.left_shifter.Set(self.low)
            self.right_shifter.Set(self.low)
            self.gear = self.low

    def align(self):
        motor_speed = .25
        left = 0
        right = 0

        if self.front_left_photo_switch.Get() and self.back_left_photo_switch.Get():
            left = 0
        elif not self.front_left_photo_switch.Get() and self.back_left_photo_switch.Get():
            left = -motor_speed
        else:
            left = motor_speed


        if self.front_right_photo_switch.Get() and self.back_right_photo_switch.Get():
            right = 0
        elif not self.front_right_photo_switch.Get() and self.back_right_photo_switch.Get():
            right = -motor_speed
        else:
            right = motor_speed 
        
        # DANGER! Right and left are inverted here. This is because Morgan flipped
        # forward and back
        self.robot_drive.SetLeftRightMotorOutputs(right, left)
