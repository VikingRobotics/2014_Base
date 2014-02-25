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
    components = {}

    class DriveConfig(object):
        right_motors = wpilib.Talon(1)
        left_motors = wpilib.Talon(2)

        robot_drive = wpilib.RobotDrive(left_motors, right_motors)

        left_shifter = wpilib.DoubleSolenoid(1, 2)
        right_shifter = wpilib.DoubleSolenoid(3, 4)
        
        # TODO: figure out which one is which. Is forward high gear or low gear? Once we know
        #       let's change the variable names to high_gear and low_gear instead of forward/reverse
        forward = wpilib.DoubleSolenoid.kForward
        reverse = wpilib.DoubleSolenoid.kReverse
        
        drive_joy = leftJoy
        
        # Buttons
        squared_drive_stick = Button(leftJoy, 1)
        shift_button = Button(leftJoy, 9)

    components['drive'] = drive.Drive(DriveConfig)


    class PickupConfig(object):
        pickup_motor = wpilib.Talon(4)

        solenoid = wpilib.DoubleSolenoid(5, 6)

        # TODO: figure out if forward is pickup-up or pickup-down. 
        # Rename these variables once we know
        forward = wpilib.DoubleSolenoid.kForward
        reverse = wpilib.DoubleSolenoid.kReverse

        pickup_switch = Button(rightJoy, 3)
        motor_button = Button(rightJoy, 2)
        
        pass_slow_preset = Button(rightJoy, 10)
        pass_fast_preset = Button(rightJoy, 11)
        pickup_slow_preset = Button(rightJoy, 12)
        pickup_fast_preset = Button(rightJoy, 13)


    components['pickup'] = pickup.Pickup(PickupConfig)


    class ShooterConfig(object):
        motors = wpilib.Talon(3)
        
        shoot_button = Button(rightJoy, 1)

        low_shot_preset_button = Button(rightJoy, 5)
        high_shot_preset_button = Button(rightJoy, 6)

        reset_hall_effect = HallEffect(wpilib.DigitalInput(6))

        preset_hall_effect_counters = []

        low_shot_hall_effect_counter = wpilib.Counter()
        low_shot_hall_effect_counter.SetUpSource(7)
        low_shot_hall_effect_counter.SetUpSourceEdge(False, True)
        low_shot_hall_effect_counter.Start()        

        high_shot_hall_effect_counter = wpilib.Counter()
        high_shot_hall_effect_counter.SetUpSource(8)
        high_shot_hall_effect_counter.SetUpSourceEdge(False, True)
        high_shot_hall_effect_counter.Start()


    components['shooter'] = shooter.Shooter(ShooterConfig)

    class UtilConfig(object):
        reload_code_button = Button(leftJoy, 8)
        compressor = wpilib.Compressor(1, 1)

    components['util'] = utilComponent.UtilComponent(UtilConfig)
    components['reporter'] = reporter.Reporter(DriveConfig, PickupConfig, ShooterConfig, UtilConfig)

    return components
