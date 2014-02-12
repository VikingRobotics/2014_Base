import wpilib
import mock
import drive
import utilComponent

from utils import Button

# Joysticks
leftJoy = wpilib.Joystick(2)
rightJoy = wpilib.Joystick(1)

componets = []


class DriveConfig(object):
    left_motors = wpilib.Talon(1)
    right_motors = wpilib.Talon(2)

    robot_drive = wpilib.RobotDrive(left_motors, right_motors)

    left_shifter = wpilib.DoubleSolenoid(1, 2)
    right_shifter = wpilib.DoubleSolenoid(3, 4)
    #print(dir(right_shifter))
    forward = wpilib.DoubleSolenoid.kForward
    reverse = wpilib.DoubleSolenoid.kReverse
    
    right_joy = leftJoy
    

    # Buttons
    sqrd_button = Button(leftJoy, 1)
    shift_button = Button(leftJoy, 11)


componets.append(drive.Drive(DriveConfig))

class UtilConfig(object):
    reset_button = Button(leftJoy, 8)
    compressor = wpilib.Compressor(1, 1)

componets.append(utilComponent.UtilComponent(UtilConfig))


# Core Functions
def CheckRestart():
    return
    # We need to do something about this at some point.....
