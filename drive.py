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

        self.squared_drive_stick = config.squared_drive_stick

        self.shift_button = config.shift_button
        self.left_shifter = config.left_shifter
        self.right_shifter = config.right_shifter
        self.forward = config.forward
        self.reverse = config.reverse

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

        squared = False
        if self.squared_drive_stick.get():
            squared = True
        self.robot_drive.ArcadeDrive(speed, rot, squared)

        if self.shift_button.get() != self.prev_shift_button_val:
            self.prev_shift_button_val = self.shift_button.get()
            self.shift()

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

    def shift(self):
        val = self.left_shifter.Get()
        if val == self.forward:
            self.left_shifter.Set(self.reverse)
            self.right_shifter.Set(self.reverse)
        else:
            self.left_shifter.Set(self.forward)
            self.right_shifter.Set(self.forward)


    def align(self):

        motorSpeed = .25

        if self.frontLeft and self.backLeft:
            self.left = 0
        elif not self.frontLeft and self.backLeft:
            self.left = -motorSpeed
        else:
            self.left = motorSpeed


        if self.frontRight and self.backRight:
            self.right = 0
        elif not self.frontRight and self.backRight:
            self.right = -motorSpeed
        else:
            self.right = motorSpeed 
            
            
        self.robot_drive.SetLeftRightMotorOutputs(self.left, self.right)



            


            
