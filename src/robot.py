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

            wpilib.Wait(0.01)

        self.dog.SetEnabled(False)

    # Called once when the robot enters autonomous state
    def Autonomous(self):
        # THE FOLLOWING LINE MAKES NETSIM HAPPY! DONT REMOVE IT, BUT
        # DONT USE IT ON THE ACTUAL ROBOT!!!!!!!!!
        # self.auto_config = AutoConfig()

        self.dog.SetEnabled(True)

        for type, component in self.components.items():
            component.auto_init(self.auto_config)

        if self.auto_config.get_autonomous_mode() == AutoConfig.ONE_BALL_AUTO:
            self.one_ball_autonomous()
        else:
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
        self.components['drive'].downshift()

        while wpilib.IsAutonomous() and wpilib.IsEnabled():
            self.dog.Feed()

            wpilib.SmartDashboard.PutString('auto robot state', current_state)

            current_time = wpilib.Timer.GetFPGATimestamp()
            elapsed_seconds = current_time - start_time

            if current_state == START:
                self.wait(.5)
                current_state = DRIVE_FORWARD
            
            elif current_state == DRIVE_FORWARD:
                self.components['drive'].auto_drive_forward_tick(current_time)

                # TODO: this isn't optimal. We should have an "extending" state and stick the goal_is_hot and
                # elapsed_seconds check in the state transition for that
                if self.components['drive'].is_auto_drive_done():
                    self.components['pickup'].extend()
                    self.wait(self.auto_config.after_drive_pause_seconds)
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
        EXTENDING = 'extending'
        SHOOTING = 'shooting'
        DRIVE_FORWARD = 'drive_forward'
        PICKUP = 'pickup'
        WAIT_FOR_HOT_GOAL = 'wait_for_hot_goal'
        SECOND_SHOT = 'second_shot'
        STOP = 'stop'
        
        # Initialization
        current_state = EXTENDING
        start_time = wpilib.Timer.GetFPGATimestamp()
        self.components['drive'].downshift()

        while wpilib.IsAutonomous() and wpilib.IsEnabled():
            self.dog.Feed()

            wpilib.SmartDashboard.PutString('auto robot state', current_state)

            current_time = wpilib.Timer.GetFPGATimestamp()
            elapsed_seconds = current_time - start_time

            if current_state == EXTENDING:
                self.components['pickup'].extend()
                self.components['pickup'].pickup_slow()
                self.wait(self.auto_config.extending_seconds)
                current_state = DRIVE_FORWARD

            elif current_state == DRIVE_FORWARD:
                self.components['drive'].auto_drive_forward_tick(current_time)
                self.components['pickup'].pickup_slow()

                if self.components['drive'].is_auto_drive_done():
                    self.wait(self.auto_config.after_drive_pause_seconds)
                    current_state = WAIT_FOR_HOT_GOAL

            elif current_state == WAIT_FOR_HOT_GOAL:
                if self.auto_config.is_goal_hot() or elapsed_seconds > 5:
                    current_state = SHOOTING

            elif current_state == SHOOTING:
                self.components['shooter'].auto_shoot_tick(current_time)
               
                if self.components['shooter'].is_auto_shoot_done():
                    self.wait(self.auto_config.after_shoot_seconds)
                    current_state = PICKUP
           
            elif current_state == PICKUP:
                self.components['pickup'].pickup_fast()
                self.wait(self.auto_config.pickup_seconds)
                self.components['pickup'].pickup_stop()
                # call shooter.reset() to knock it out of AUTO_SHOOT_DONE state
                self.components['shooter'].reset()
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
