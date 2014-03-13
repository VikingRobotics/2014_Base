import common

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

__all__ = ['AutoDrive']


class AutoDrive(common.ComponentBase):

    def __init__(self, config):

        self.left_motors = config.left_motors
        self.right_motors = config.right_motors

        self.p = 0
        self.i = 0
        self.d = 0

        self.auto_drive_distance = 1
        self.encoder_distance_per_pulse = 1/100

        self.left_encoder = config.left_encoder
        self.left_encoder.SetPIDSourceParameter(wpilib.PIDSourceParameter.kDistance)
        self.left_pid_controller = wpilib.PIDController(self.p, self.i, self.d, self.left_encoder, self.left_motors)

        self.right_encoder = config.right_encoder
        self.right_encoder.SetPIDSourceParameter(wpilib.PIDSourceParameter.kDistance)
        self.right_pid_controller = wpilib.PIDController(self.p, self.i, self.d, self.right_encoder, self.right_motors)

    def robot_init(self):
        wpilib.SmartDashboard.PutNumber("p", self.p)
        wpilib.SmartDashboard.PutNumber("i", self.i)
        wpilib.SmartDashboard.PutNumber("d", self.d)

        wpilib.SmartDashboard.PutNumber("auto_drive_distance", self.auto_drive_distance)
        wpilib.SmartDashboard.PutNumber("encoder_distance_per_pulse", self.encoder_distance_per_pulse)

    def update_smartdashboard_vars(self):
        self.p = wpilib.SmartDashboard.GetNumber("p")
        self.i = wpilib.SmartDashboard.GetNumber("i")
        self.d = wpilib.SmartDashboard.GetNumber("d")

        self.auto_drive_distance = wpilib.SmartDashboard.GetNumber("auto_drive_distance")
        self.encoder_distance_per_pulse = wpilib.SmartDashboard.GetNumber("encoder_distance_per_pulse")

    def op_init(self):
        self.left_pid_controller.Disable()
        self.right_pid_controller.Disable()

    def auto_init(self, auto_config):
        self.left_encoder.SetDistancePerPulse(self.encoder_distance_per_pulse)
        self.right_encoder.SetDistancePerPulse(self.encoder_distance_per_pulse)

        self.left_pid_controller.SetPID(self.p, self.i, self.d)
        self.right_pid_controller.SetPID(self.p, self.i, self.d)

        self.left_pid_controller.SetSetpoint(self.auto_drive_distance)
        self.right_pid_controller.SetSetpoint(self.auto_drive_distance)

    def auto_drive_forward_tick(self, time):
        self.left_pid_controller.Enable()
        self.right_pid_controller.Enable()

        wpilib.SmartDashboard.PutNumber("left PID output", self.left_pid_controller.Get())
        wpilib.SmartDashboard.PutNumber("right PID output", self.right_pid_controller.Get())

        if self.is_auto_drive_done():
            self.left_pid_controller.Disable()
            self.right_pid_controller.Enable()

    def is_auto_drive_done(self):
        return self.left_pid_controller.OnTarget() and self.right_pid_controller.OnTarget()

