try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from auto_config import *

import config



class MyRobot(wpilib.SimpleRobot):

    def __init__(self):
        super().__init__()
        
        self.dog = self.GetWatchdog()
        self.dog.SetExpiration(0.25)
        self.components = config.components()


    # Called once when the robot is initialized
    def RobotInit(self):
        self.auto_config = AutoConfig()
        wpilib.SmartDashboard.PutNumber("pickup_reverse_seconds", .3)
        # Initialize all robot components
        for type, component in self.components.items():
            component.robot_init()

    # Called once whenever the robot enters the disabled state
    def Disabled(self):
        self.dog.SetEnabled(True)

        for type, component in self.components.items():
            component.disabled_init()

        while wpilib.IsDisabled():
            self.dog.Feed()
            for type, component in self.components.items():
                component.disabled_tick(wpilib.Timer.GetFPGATimestamp())
                component.update_smartdashboard_vars()

            wpilib.Wait(0.01)

        self.dog.SetEnabled(False)

    # Called once when the robot enters autonomous state
    def Autonomous(self):
        # THE FOLLOWING LINE MAKES NETSIM HAPPY! DONT REMOVE IT, BUT
        # DONT USE IT ON THE ACTUAL ROBOT!!!!!!!!!
        # self.auto_config = AutoConfig()

        self.dog.SetEnabled(True)

        self.auto_config.update_smartdashboard_vars()

        for type, component in self.components.items():
            component.auto_init(self.auto_config)
            component.update_smartdashboard_vars()

        if self.auto_config.get_autonomous_mode() == AutoConfig.ONE_BALL_AUTO:
            self.auto_config.drive_seconds = self.auto_config.one_ball_drive_seconds
            self.one_ball_autonomous()
        else:
            self.auto_config.drive_seconds = self.auto_config.two_ball_drive_seconds
            self.two_ball_autonomous()

        self.dog.SetEnabled(False)

    def one_ball_autonomous(self):

        # autonomous states
        START = 'start'
        DRIVE_FORWARD = 'drive_forward'
        SHOOTING = 'shooting'
        STOP = 'stop'
        WAIT_FOR_HOT_GOAL = 'wait_for_hot_goal'

        # Initialization
        current_state = START
        start_time = wpilib.Timer.GetFPGATimestamp()
        

        while wpilib.IsAutonomous() and wpilib.IsEnabled():
            self.dog.Feed()

            wpilib.SmartDashboard.PutString('auto robot state', current_state)

            current_time = wpilib.Timer.GetFPGATimestamp()
            elapsed_seconds = current_time - start_time

            if current_state == START:
                self.components['drive'].downshift()
                self.wait(self.auto_config.shift_seconds)
                current_state = DRIVE_FORWARD
            
            elif current_state == DRIVE_FORWARD:
                # self.components['drive'].auto_drive_forward_tick(current_time)
                # if self.components['drive'].is_auto_drive_done(): 

                self.components['auto_drive'].auto_drive_forward_tick(current_time)
                if self.components['auto_drive'].is_auto_drive_done():
                    self.wait(self.auto_config.after_drive_pause_seconds)
                    self.components['pickup'].extend()
                    self.wait(self.auto_config.extending_seconds)
                    current_state = SHOOTING

            elif current_state == WAIT_FOR_HOT_GOAL:
                if self.auto_config.is_goal_hot() or elapsed_seconds > 5:
                    current_state = SHOOTING
                    
            elif current_state == SHOOTING:
                self.components['shooter'].auto_shoot_tick(current_time)
                if self.components['shooter'].is_auto_shoot_done():
                    self.components['drive'].reset()
                    self.wait(self.auto_config.after_shoot_seconds)
                    current_state = STOP


            # for type, component in self.components.items():
            #     component.auto_tick(wpilib.Timer.GetFPGATimestamp())

            wpilib.Wait(0.01)

        

    def two_ball_autonomous(self):

        # autonomous states
        START = 'start'
        EXTENDING = 'extending'
        SHOOTING = 'shooting'
        DRIVE_FORWARD = 'drive_forward'
        PICKUP_REVERSE = 'pickup_reverse'
        PICKUP = 'pickup'
        WAIT_FOR_HOT_GOAL = 'wait_for_hot_goal'
        SECOND_SHOT = 'second_shot'
        STOP = 'stop'
        
        # Initialization
        # TODO: add downshift
        current_state = START
        start_time = wpilib.Timer.GetFPGATimestamp()
        while wpilib.IsAutonomous() and wpilib.IsEnabled():
            self.dog.Feed()

            wpilib.SmartDashboard.PutString('auto robot state', current_state)

            current_time = wpilib.Timer.GetFPGATimestamp()
            elapsed_seconds = current_time - start_time

            if current_state == START:
                self.components['drive'].upshift()
                self.wait(self.auto_config.shift_seconds)
                current_state = EXTENDING
                
            if current_state == EXTENDING:
                self.components['pickup'].extend()
                self.components['pickup'].pickup_slow()
                self.wait(self.auto_config.extending_seconds)
                current_state = DRIVE_FORWARD

            elif current_state == DRIVE_FORWARD:
                self.components['pickup'].pickup_drag_fast()

                self.components['drive'].auto_drive_forward_tick(current_time)
                if self.components['drive'].is_auto_drive_done():                
                # self.components['auto_drive'].auto_drive_forward_tick(current_time)
                # if self.components['auto_drive'].is_auto_drive_done():
                    self.wait(self.auto_config.after_drive_pause_seconds)
                    current_state = WAIT_FOR_HOT_GOAL

            elif current_state == WAIT_FOR_HOT_GOAL:
                if self.auto_config.is_goal_hot() or elapsed_seconds > 5:
                    self.components['pickup'].pickup_slow()
                    self.wait(self.auto_config.pre_shot_pickup_stop)
                    self.pickup_reverse_start_time = current_time
                    current_state = PICKUP_REVERSE

            # This is intentionally not an elif. We have to immediately reverse the pickup
            if current_state == PICKUP_REVERSE:
                pickup_reverse_seconds = wpilib.SmartDashboard.GetNumber("pickup_reverse_seconds")
                self.components['pickup'].pickup_reverse()
                pickup_reverse_elapsed_seconds = current_time - self.pickup_reverse_start_time
                if pickup_reverse_elapsed_seconds > pickup_reverse_seconds:
                    self.components['pickup'].pickup_stop()
                    self.wait(.5) # wait for ball to settle
                    current_state = SHOOTING

            elif current_state == SHOOTING:
                self.components['shooter'].auto_shoot_tick(current_time)
               
                if self.components['shooter'].is_auto_shoot_done():
                    self.wait(self.auto_config.after_shoot_seconds)
                    current_state = PICKUP
           
            elif current_state == PICKUP:
                self.components['pickup'].pickup_fast()
                self.wait(self.auto_config.pickup_seconds)
                self.components['pickup'].retract()
                self.components['pickup'].pickup_drag_fast()
                self.wait(self.auto_config.extending_seconds)
                self.components['pickup'].extend()
                self.wait(self.auto_config.extending_seconds)
                # self.components['pickup'].pickup_stop()
                # call shooter.reset() to knock it out of AUTO_SHOOT_DONE state
                self.components['shooter'].reset()
                self.components['pickup'].pickup_stop()
                current_state = SECOND_SHOT

            elif current_state == SECOND_SHOT:
                self.components['shooter'].auto_shoot_tick(current_time)
                if self.components['shooter'].is_auto_shoot_done():
                    current_state = STOP

            wpilib.Wait(0.01)


    def OperatorControl(self):
        self.dog.SetEnabled(True)

        for type, component in self.components.items():
            component.op_init()

        while self.IsOperatorControl() and self.IsEnabled():
            self.dog.Feed()

            for type, component in self.components.items():
                component.op_tick(wpilib.Timer.GetFPGATimestamp())
                component.update_smartdashboard_vars()

            ## Debug & Tuning
            # ??
            wpilib.Wait(0.01)

        self.dog.SetEnabled(False)

    def Test(self):
        while self.IsTest() and self.IsEnabled():
            wpilib.LiveWindow.Run()
            wpilib.Wait(0.01)

    # Wait function used to pause code execution while continuing to
    # feed the dog
    def wait(self, wait_time):
        start_time = wpilib.Timer.GetFPGATimestamp()
        elapsed_time = 0
        while(elapsed_time < wait_time):
            elapsed_time = wpilib.Timer.GetFPGATimestamp() - start_time
            self.dog.Feed()
            wpilib.Wait(0.01)

def run():
    robot = MyRobot()
    robot.StartCompetition()
    return robot

if __name__ == '__main__':
    wpilib.run()
