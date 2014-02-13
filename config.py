try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import mock
import drive
import pickup
import shooter
import utilComponent

from utils import Button
from utils import Axis

# Joysticks
leftJoy = wpilib.Joystick(2)
rightJoy = wpilib.Joystick(1)

components = []


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

components.append(drive.Drive(DriveConfig))


class PickupConfig(object):
    pickup_motor = wpilib.Talon(4)

    solenoid = wpilib.DoubleSolenoid(5, 6)
    forward = wpilib.DoubleSolenoid.kForward
    reverse = wpilib.DoubleSolenoid.kReverse
    
    out_button = Button(rightJoy, 3)
    in_button = Button(rightJoy, 2)
    motor_button = Button(rightJoy, 4)
    
    speed_axis = Axis(rightJoy, 1)

components.append(pickup.Pickup(PickupConfig))

class ShooterConfig(object):
    # TODO: what channel is this guy actually on?
    motors = wpilib.Talon(3)
    
    shoot_button = Button(rightJoy, 1)
    stop_buttons = [Button(rightJoy, x+5) for x in range(2)]
    
    stop_inputs = [wpilib.DigitalInput(x) for x in range(6, 10)]
    reset_input = wpilib.DigitalInput(10)

    # TODO: Matt through these in there to make the Shooter
    # component work. What should these be mapped to?
    reset_stop = Button(rightJoy, 5)
    max_throw_time = Axis(rightJoy, 2)

components.append(shooter.Shooter(ShooterConfig))


class UtilConfig(object):
    reset_button = Button(leftJoy, 8)
    compressor = wpilib.Compressor(1, 1)

components.append(utilComponent.UtilComponent(UtilConfig))
