import unittest

import utils
import mock

import drive
import shooter

def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])

class TestShooter(unittest.TestCase):

    def setUp(self):
        self.motors = [mock.Motor(), mock.Motor(), mock.Motor(), mock.Motor()]
        self.shoot_button = mock.Button()
       
        class MockShooterConfig(object):
            motors = self.motors
            shoot_button = self.shoot_button

        self.shooter = shooter.Shooter(MockShooterConfig)

    def tearDown(self):
         pass

    def test_shooter(self): 

        for motor in self.motors:
           self.assertEquals(motor.speed, 0)

        self.shooter.op_tick(1)

        for motor in self.motors:
            self.assertEquals(motor.speed, 0) 
        
        self.shoot_button.pressed = True
        self.shooter.op_tick(2)
        
        for motor in self.motors:
            self.assertEquals(motor.speed, 1)

        self.shoot_button.pressed = False
        
        self.shooter.op_tick(2)

        for motor in self.motors:
            self.assertEquals(motor.speed, 0)

class TestDrive(unittest.TestCase):

    def setUp(self):
        self.robot_drive = mock.RobotDrive()

        self.joystick = mock.Joystick()
        self.photo_sensors = [ mock.DigitalInput() for x in range(5)]
        self.hs_button = mock.Button()
        self.align_button = mock.Button()


        class MockDriveConfig(object):
            # Motors & Drive System
            robot_drive = self.robot_drive
            drive_joy = self.joystick

            photo_sensors = self.photo_sensors

            align_button = self.align_button
            hs_button = self.hs_button

        self.drive = drive.Drive(MockDriveConfig)

    def tearDown(self):
        pass

    def test_throttle(self):
        self.joystick.x = 0.0

        # Sweep forward
        for y in seq(-1.0, 1.0, 0.1):
            self.joystick.y = y

            self.drive.op_tick(100)

            self.assertEquals(self.robot_drive.speed, self.joystick.y)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x)

        # Sweep back
        for y in seq(1.0, -1.0, -0.1):
            self.joystick.y = y

            self.drive.op_tick(200)

            self.assertEquals(self.robot_drive.speed, self.joystick.y)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x)

    def test_steering(self):
        self.joystick.y = 0.0

        # Sweep forward
        for x in seq(-1.0, 1.0, 0.1):
            self.joystick.x = x

            self.drive.op_tick(100)

            self.assertEquals(self.robot_drive.speed, self.joystick.y)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x)

        # Sweep back
        for x in seq(1.0, -1.0, -0.1):
            self.joystick.x = x

            self.drive.op_tick(200)

            self.assertEquals(self.robot_drive.speed, self.joystick.y)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x)

    def test_half_speed_throttle(self):
        self.hs_button.pressed = True

        self.joystick.x = 0.0

        # Sweep forward
        for y in seq(-1.0, 1.0, 0.1):
            self.joystick.y = y

            self.drive.op_tick(100)

            self.assertEquals(self.robot_drive.speed, self.joystick.y/2)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x)

        # Sweep back
        for y in seq(1.0, -1.0, -0.1):
            self.joystick.y = y

            self.drive.op_tick(200)

            self.assertEquals(self.robot_drive.speed, self.joystick.y/2)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x)

    def test_half_speed_steering(self):
        self.hs_button.pressed = True

        self.joystick.y = 0.0

        # Sweep forward
        for x in seq(-1.0, 1.0, 0.1):
            self.joystick.x = x

            self.drive.op_tick(1)

            self.assertEquals(self.robot_drive.speed, self.joystick.y)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x/2)

        # Sweep back
        for x in seq(1.0, -1.0, -0.1):
            self.joystick.x = x

            self.drive.op_tick(10)

            self.assertEquals(self.robot_drive.speed, self.joystick.y)
            self.assertEquals(self.robot_drive.rotation, self.joystick.x/2)


class TestButtonControlledMotor(unittest.TestCase):

    def setUp(self):
        self.up_button = mock.Button()
        self.down_button = mock.Button()
        self.motor = mock.Motor()

        class MockButtonControlledMotor(object):
            motor = self.motor

            up_button = self.up_button
            down_button = self.down_button

        self.button_motor = utils.ButtonControlledMotor(
                                                 MockButtonControlledMotor)

    def test_op_init(self):
        self.motor.Set(1)
        self.button_motor.op_init()
        self.assertEqual(self.motor.speed, 0)

    def test_up(self):
        self.up_button.pressed = True

        self.button_motor.op_tick(1)

        self.assertEqual(self.motor.speed, -1)

    def test_down(self):
        self.down_button.pressed = True

        self.button_motor.op_tick(1)

        self.assertEqual(self.motor.speed, 1)


if __name__ == '__main__':
        unittest.main()
