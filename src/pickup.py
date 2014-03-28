try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import common


__all__ = ['Pickup']


class Pickup(common.ComponentBase):
    
    def __init__(self, config):
        self.motor = config.pickup_motor
        
        self.solenoid = config.solenoid
        self.OUT = config.reverse
        self.IN = config.forward

        self.pickup_switch = config.pickup_switch
        self.motor_button = config.motor_button

        self.pass_slow_preset = config.pass_slow_preset
        self.pickup_slow_preset = config.pickup_slow_preset
        self.pickup_fast_preset = config.pickup_fast_preset

        self.pickup_state = -1
        self.start_time = 0
        self.is_extending = False

        self.extend_spin_time = .3
        self.extend_spin_speed = -.8

        self.pickup_fast_speed = -1
        self.drag_ball_speed = -.25
        self.slow_pass_speed = .5
        self.pickup_drag_fast_speed = -.5

        self.auto_pickup_speed = .5

    def robot_init(self):
        wpilib.SmartDashboard.PutNumber("extend_spin_time", self.extend_spin_time)
        wpilib.SmartDashboard.PutNumber("extend_spin_speed", self.extend_spin_speed)
        wpilib.SmartDashboard.PutNumber("pickup_fast_speed", self.pickup_fast_speed)
        wpilib.SmartDashboard.PutNumber("drag_ball_speed", self.drag_ball_speed)
        wpilib.SmartDashboard.PutNumber("slow_pass_speed", self.slow_pass_speed)
        wpilib.SmartDashboard.PutNumber("pickup_reverse_speed", 1)
        wpilib.SmartDashboard.PutNumber("auto pickup speed", self.auto_pickup_speed)

    def update_smartdashboard_vars(self):
        self.extend_spin_time = wpilib.SmartDashboard.GetNumber("extend_spin_time")
        self.extend_spin_speed = wpilib.SmartDashboard.GetNumber("extend_spin_speed")
        self.pickup_fast_speed = wpilib.SmartDashboard.GetNumber("pickup_fast_speed")
        self.drag_ball_speed = wpilib.SmartDashboard.GetNumber("drag_ball_speed")
        self.slow_pass_speed = wpilib.SmartDashboard.GetNumber("slow_pass_speed")
        self.auto_pickup_speed = wpilib.SmartDashboard.GetNumber("auto pickup speed")
        self.pickup_reverse_speed = wpilib.SmartDashboard.GetNumber("pickup_reverse_speed")   
    def op_init(self):
        pass

    def op_tick(self, time):
        speed = 0

        prev_state = self.pickup_state
        self.pickup_state = self.solenoid.Get()
        
        # If the pickup is extending
        if prev_state == self.IN and self.pickup_state == self.OUT:
            self.is_extending = True
            self.start_time = time

        elapsed_time = time - self.start_time
        if self.is_extending:
            if elapsed_time < self.extend_spin_time:
                speed = self.extend_spin_speed
            else: 
                # we're done extending
                self.is_extending = False

        if self.motor_button.get():
            if self.pass_slow_preset.get():
                speed = self.slow_pass_speed
            elif self.pickup_slow_preset.get():
                speed = self.drag_ball_speed
            elif self.pickup_fast_preset.get():
                speed = self.pickup_fast_speed

        self.motor.Set(speed)

        if self.pickup_switch.get():
            self.extend()
        else:
            self.retract()

    def extend(self):
        self.solenoid.Set(self.OUT)

    def retract(self):
        self.solenoid.Set(self.IN)

    def is_extended(self):
        return self.solenoid.Get() == self.OUT 

    def pickup_slow(self):
        self.motor.Set(self.drag_ball_speed)

    def pickup_fast(self):
        self.motor.Set(self.pickup_fast_speed)

    def pickup_stop(self):
        self.motor.Set(0)

    def pickup_drag_fast(self):
        self.motor.Set(self.pickup_drag_fast_speed)

    def pickup_reverse(self):
        self.motor.Set(self.pickup_reverse_speed)

    def pickup_auto_fast(self):
        self.motor.Set(self.auto_pickup_speed)

