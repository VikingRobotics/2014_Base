import common

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

class DriveBase:
    FRONT = True
    BACK = False
    def __init__(self, left_motor, right_motor, front,
                 left_encoder, right_encoder, 
                 left_PID_controller, right_PID_controller):

        self.left_motor = left_motor
        self.right_motor = right_motor

        self.front = front

        self.left_encoder = left_encoder
        self.right_encoder = right_encoder

        self.left_PID_controller = left_PID_controller
        self.right_PID_controller = right_PID_controller

        self.p = 0
        self.i = 0
        self.d = 0

        self.pid_enabled = False

    def set_front(self, front):
        self.front = front

    def enable_pid(self):
        self.pid_enabled = True
        self.left_PID_controller.Enable()
        self.right_PID_controller.Enable()

    def disable_pid(self):
        self.pid_enabled = False
        self.left_PID_controller.Disable()
        self.right_PID_controller.Disable()

    def StopMotor(self):
        self.left_motor.Set(0)
        self.right_motor.Set(0)

    def drive_speed(self, l_speed, r_speed):
        self.left_PID_controller.SetSetpoint(l_speed)
        self.right_PID_controller.SetSetpoint(r_speed)

    def drive_distance(self, distance, speed):
        self.left_PID_controller.SetSetpoint(distance)
        self.right_PID_controller.SetSetpoint(distance)

    def set_pid(self, p, i = False, d = False):
        if(i == False):
            i = self.i
        if(d == False):
            d = self.d

        self.left_PID_controller.SetPID(p, i, d)
        self.right_PID_controller.SetPID(p, i, d)

    def ArcadeDrive(self, rot, speed):
        if speed > 0.0:
            if rot > 0.0:
                l_speed = speed - rot
                r_speed = max(speed, rot)
            else:
                l_speed = max(speed, -1 * rot)
                r_speed = speed + rot

        else:
            if (rot > 0.0):    
                l_speed = -1 * max(-1 * speed, rot)
                r_speed = speed + rot
            else:    
                l_speed = speed - rot
                r_speed = - max(-1 * speed, -1 * rot)

        if not self.front:
            temp = l_speed
            l_speed = r_speed
            r_speed = temp

        if self.pid_enabled:
            self.drive_speed(l_speed, r_speed)
        else:
            self.left_motor.Set(l_speed)
            self.right_motor.Set(r_speed)
