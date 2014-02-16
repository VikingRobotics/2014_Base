try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import drive
import pickup
import shooter
import utilComponent
import reporter

from utils import Button
from utils import Axis
from utils import HallEffect

def components():
    leftJoy = wpilib.Joystick(1)
    rightJoy = wpilib.Joystick(2)
    components = []

    class DriveConfig(object):
        left_motors = wpilib.Talon(1)
        right_motors = wpilib.Talon(2)

        robot_drive = wpilib.RobotDrive(left_motors, right_motors)

        left_shifter = wpilib.DoubleSolenoid(1, 2)
        right_shifter = wpilib.DoubleSolenoid(3, 4)
        
        forward = wpilib.DoubleSolenoid.kForward
        reverse = wpilib.DoubleSolenoid.kReverse
        
        drive_joy = leftJoy
        
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
        motors = wpilib.Talon(3)
        
        shoot_button = Button(rightJoy, 1)

        stop_buttons = [Button(rightJoy, x+5) for x in range(2)]

        reset_stop = HallEffect(wpilib.DigitalInput(6))

        stop_counters = []

        for digital_input in range(7, 10):
            stop_counter = wpilib.Counter()
            stop_counter.SetUpSource(digital_input)
            stop_counter.SetUpSourceEdge(False, True)
            stop_counter.Start()
            stop_counters.append(stop_counter)

    components.append(shooter.Shooter(ShooterConfig))

    class UtilConfig(object):
        reset_button = Button(leftJoy, 8)
        compressor = wpilib.Compressor(1, 1)

    components.append(utilComponent.UtilComponent(UtilConfig))
    components.append(reporter.Reporter(DriveConfig, PickupConfig, ShooterConfig, UtilConfig))

    return components
