try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

import drive
import pickup
import shooter
import utilComponent
import reporter
import auto_drive
import auto_config

from utils import Button
from utils import Axis
from utils import HallEffect
from utils import DistanceEncoder
from utils import RateEncoder

from driveBase import DriveBase

def components():
    leftJoy = wpilib.Joystick(1)
    rightJoy = wpilib.Joystick(2)
    components = {}

    # lw = wpilib.LiveWindow.GetInstance()

    class DriveConfig(object):
        right_motors = wpilib.Talon(1)
        # lw.AddActuator('Drive', 'right motors', right_motors)
        left_motors = wpilib.Talon(2)
        # lw.AddActuator("Drive", "left motors", left_motors)

        robot_drive = wpilib.RobotDrive(left_motors, right_motors)

        left_shifter = wpilib.DoubleSolenoid(1, 2)
        # lw.AddActuator("Drive", "left shifter", left_shifter)

        right_shifter = wpilib.DoubleSolenoid(3, 4)
        # lw.AddActuator("Drive", "right shifter", right_shifter)


        # TODO: figure out which one is which. Is forward high gear or low gear? Once we know
        #       let's change the variable names to high_gear and low_gear instead of forward/reverse
        forward = wpilib.DoubleSolenoid.kForward
        reverse = wpilib.DoubleSolenoid.kReverse
        
        drive_joy = leftJoy

        # Buttons
        # align_button = Button(leftJoy, 6) # UNUSED!!!!!!
        shift_button = Button(leftJoy, 9)

    components['drive'] = drive.Drive(DriveConfig)

    class AutoDriveConfig(object):
        right_motors = DriveConfig.right_motors
        left_motors = DriveConfig.left_motors

        left_encoder = wpilib.Encoder(2, 3)
        right_encoder = wpilib.Encoder(4, 5)

        left_encoder.SetDistancePerPulse(1/128)
        right_encoder.SetDistancePerPulse(1/128)


    # components['auto_drive'] = auto_drive.AutoDrive(AutoDriveConfig)

    class PickupConfig(object):
        pickup_motor = wpilib.Talon(4)
        # self.lw.AddActuator("Pickup", "pickup motor", pickup_motor)

        solenoid = wpilib.DoubleSolenoid(5, 6)
        # lw.AddActuator("Pickup", "pickup solenoid", solenoid)

        # TODO: figure out if forward is pickup-up or pickup-down. 
        # Rename these variables once we know
        forward = wpilib.DoubleSolenoid.kForward
        reverse = wpilib.DoubleSolenoid.kReverse

        pickup_switch = Button(rightJoy, 3)
        motor_button = Button(rightJoy, 2)
        
        pickup_fast_preset = Button(rightJoy, 10)
        pass_slow_preset = Button(rightJoy, 11)
        pickup_slow_preset = Button(rightJoy, 12)


    components['pickup'] = pickup.Pickup(PickupConfig)


    class ShooterConfig(object):
        motors = wpilib.Jaguar(3)
        # lw.AddActuator("Shooter", "shooter motors", motors)
        shoot_button = Button(rightJoy, 1)

        low_shot_preset_button = Button(rightJoy, 8)
        high_shot_preset_button = Button(rightJoy, 7)
        catch_preset_button = Button(rightJoy, 5)
        manual_reset_button = Button(rightJoy, 4)

        reset_hall_effect_counter = wpilib.Counter()
        reset_hall_effect_counter.SetUpSource(8)
        reset_hall_effect_counter.SetUpSourceEdge(False, True)
        reset_hall_effect_counter.Start() 
        # lw.AddSensor("Shooter", "reset hall effect", reset_hall_effect_counter)

        low_shot_hall_effect_counter = wpilib.Counter()
        low_shot_hall_effect_counter.SetUpSource(6)
        low_shot_hall_effect_counter.SetUpSourceEdge(False, True)
        low_shot_hall_effect_counter.Start()
        # lw.AddSensor("Shooter", "low shot hall effect", low_shot_hall_effect_counter)        

        high_shot_hall_effect_counter = wpilib.Counter()
        high_shot_hall_effect_counter.SetUpSource(7)
        high_shot_hall_effect_counter.SetUpSourceEdge(False, True)
        high_shot_hall_effect_counter.Start()
        # lw.AddSensor("Shooter" "high shot hall effect", high_shot_hall_effect_counter)

        catch_hall_effect_counter = wpilib.Counter()
        catch_hall_effect_counter.SetUpSource(9)
        catch_hall_effect_counter.SetUpSourceEdge(False, True)
        catch_hall_effect_counter.Start()

        pickup = components['pickup']

    components['shooter'] = shooter.Shooter(ShooterConfig)

    class UtilConfig(object):
        reload_code_button = Button(leftJoy, 8)
        compressor = wpilib.Compressor(1, 1)

    components['auto_config'] = auto_config.AutoConfig()

    components['util'] = utilComponent.UtilComponent(UtilConfig)
    components['reporter'] = reporter.Reporter(DriveConfig,
                                               AutoDriveConfig, 
                                               PickupConfig, 
                                               ShooterConfig, 
                                               UtilConfig,
                                               components['auto_config'])

    return components
