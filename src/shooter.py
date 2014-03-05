import common

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


__all__ = ['Shooter']


class Shooter(common.ComponentBase):

    SHOOTING = 'shooting'
    RESET = 'reset'
    RESETTING = 'resetting'
    AUTO_SHOOT_DONE = 'auto_shoot_done'

    def __init__(self, config):
        self.motors = config.motors

        self.shoot_button = config.shoot_button
        self.manual_reset_button = config.manual_reset_button

        self.low_shot_preset_button = config.low_shot_preset_button
        self.high_shot_preset_button = config.high_shot_preset_button
        
        self.low_shot_hall_effect_counter = config.low_shot_hall_effect_counter
        self.high_shot_hall_effect_counter = config.high_shot_hall_effect_counter

        self.reset_hall_effect_counter = config.reset_hall_effect_counter
    
        self.op_state = self.RESETTING

        self.auto_state = self.RESET

        self.RESETTING_SPEED = -.25

        self.SHOOTING_SPEED = 1

    def op_init(self):
        self.low_shot_hall_effect_counter.Reset()
        self.high_shot_hall_effect_counter.Reset()
        self.reset_hall_effect_counter.Reset()

        self.op_state = self.RESET

    def op_tick(self, time):

        if self.op_state == self.RESET:
            speed = 0
            if self.shoot_button.get():
                self.op_state = self.SHOOTING
                self.low_shot_hall_effect_counter.Reset()
                self.high_shot_hall_effect_counter.Reset()
                self.reset_hall_effect_counter.Reset()

        if self.op_state == self.SHOOTING:
            components.pickup.is_extended()
            speed = self.SHOOTING_SPEED
            if self.should_stop():
                speed = 0
                self.reset_hall_effect_counter.Reset()
                self.op_state = self.RESETTING

        if self.op_state == self.RESETTING:
            speed = self.RESETTING_SPEED
            if self.reset_hall_effect_counter.Get():
                speed = 0
                self.reset_hall_effect_counter.Reset()
                self.op_state = self.RESET
        
        #This is not part of the normal state machine,
        #this is for manual reset.
        if self.op_state != self.RESET and self.manual_reset_button.get() and self.shoot_button.get():
            self.op_state = self.RESETTING


        wpilib.SmartDashboard.PutString("Shooter Op State", self.op_state)

        self.motors.Set(speed)

    def auto_init(self):
        self.auto_state = self.RESET
        self.low_shot_hall_effect_counter.Reset()
        self.high_shot_hall_effect_counter.Reset()
        self.reset_hall_effect_counter.Reset()
        wpilib.SmartDashboard.PutString('auto shooter state', self.auto_state)

    def auto_shoot_tick(self, time):

        speed = 0
        if self.auto_state == self.RESET:
            self.auto_state = self.SHOOTING

        elif self.auto_state == self.SHOOTING:
            speed = self.SHOOTING_SPEED
            if self.high_shot_hall_effect_counter.Get():
                self.reset_hall_effect_counter.Reset()
                self.auto_state = self.RESETTING
                # wpilib.Wait(3)

        elif self.auto_state == self.RESETTING:
            speed = self.RESETTING_SPEED
            if self.reset_hall_effect_counter.Get():
                speed = 0
                self.auto_state = self.AUTO_SHOOT_DONE
                # wpilib.Wait(3)

        elif self.auto_state == self.AUTO_SHOOT_DONE:
            speed = 0

        self.motors.Set(speed)
        
        wpilib.SmartDashboard.PutString('auto shooter state', self.auto_state)

    def is_auto_shoot_done(self):
        return self.auto_state == self.AUTO_SHOOT_DONE


    def should_stop(self):
        # This could be compacted down, but it's understandable as is
        if self.low_shot_preset_button.get() and self.low_shot_hall_effect_counter.Get():
            return True
        # Always stop if the high shot hall effect is triggered
        elif self.high_shot_hall_effect_counter.Get(): 
            return True

        return False
