try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import common

__all__ = ['Reporter']


class Reporter(common.ComponentBase):

    def __init__(self, drive_config, pickup_config, shooter_config, util_config):
        self.drive_config = drive_config
        self.pickup_config = pickup_config
        self.shooter_config = shooter_config
        self.util_config = util_config

    def op_tick(self, time):
        self.update()

    def auto_tick(self, time):
        self.update()

    def disabled_tick(self, time):
        self.update()

    def update(self):
        # TODO: once this code is on the robot, we can work with the drivers to change the outputs
        #       to be useful to them. For example, insted of "forward" and "reverse" for shifters,
        #       they can say "high gear", "low gear"

        # drive_config
        wpilib.SmartDashboard.PutNumber("left motor speed", self.drive_config.left_motors.Get())
        wpilib.SmartDashboard.PutNumber("right motor speed", self.drive_config.right_motors.Get())

        wpilib.SmartDashboard.PutString("left shifter", self.solenoid_value(self.drive_config.left_shifter.Get()))
        
        right_shifter_state = self.solenoid_value(self.drive_config.right_shifter.Get())
        wpilib.SmartDashboard.PutString("right shifter", right_shifter_state)

        #pickup config        
        wpilib.SmartDashboard.PutNumber("pickup motor speed", self.pickup_config.pickup_motor.Get())
        wpilib.SmartDashboard.PutString("pickup solenoid", self.solenoid_value(self.pickup_config.solenoid.Get()))

        #shooter config
        wpilib.SmartDashboard.PutNumber("shooter motor speed", self.shooter_config.motors.Get())
        wpilib.SmartDashboard.PutNumber("reset stop hall effect", self.shooter_config.reset_stop.Get())

        for idx, stop_counter in enumerate(self.shooter_config.stop_counters):
            wpilib.SmartDashboard.PutNumber("stop counter %d" % idx, stop_counter.Get())

        #util config
        wpilib.SmartDashboard.PutNumber("pressure switch val", self.util_config.compressor.GetPressureSwitchValue())


    def solenoid_value(self, val):
        if val == wpilib.DoubleSolenoid.kForward:
            return "low gear"
        elif val == wpilib.DoubleSolenoid.kReverse:
            return "high gear"
        else:
            return "not used yet"

