try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import config


class MyRobot(wpilib.SimpleRobot):

    def __init__(self):
        super().__init__()

        self.dog = self.GetWatchdog()
        self.dog.SetExpiration(0.25)

        self.components = config.components

    def RobotInit(self):

        for component in self.components:
            component.robot_init()

    def Disabled(self):
        self.dog.SetEnabled(True)

        for componet in self.components:
            componet.disabled_init()

        while wpilib.IsDisabled():
            self.dog.Feed()

            for componet in self.components:
                componet.disabled_tick(wpilib.Timer.GetFPGATimestamp())

            wpilib.Wait(0.01)

        self.dog.SetEnabled(False)

    def Autonomous(self):
        self.dog.SetEnabled(True)

        for componet in self.components:
            componet.auto_init()

        while wpilib.IsAutonomous() and wpilib.IsEnabled():
            self.dog.Feed()

            for componet in self.components:
                componet.auto_tick(wpilib.Timer.GetFPGATimestamp())

            wpilib.Wait(0.01)

        self.dog.SetEnabled(False)

    def OperatorControl(self):
        self.dog.SetEnabled(True)

        for componet in self.components:
            componet.op_init()

        while self.IsOperatorControl() and self.IsEnabled():
            self.dog.Feed()

            for componet in self.components:
                componet.op_tick(wpilib.Timer.GetFPGATimestamp())

            ## Debug & Tuning
            # ??
            wpilib.Wait(0.01)

        self.dog.SetEnabled(False)

def run():
    robot = MyRobot()
    robot.StartCompetition()
    return robot

if __name__ == '__main__':
    wpilib.run()
