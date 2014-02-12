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
        self.stop_input = mock.DigitalInput()
        self.reset_input = mock.DigitalInput()

        class MockShooterConfig(object):
            motors = self.motors
            shoot_button = self.shoot_button
            stop_input = self.stop_input
            reset_input = self.reset_input

        self.shooter = shooter.Shooter(MockShooterConfig)

    def tearDown(self):
         pass

    def test_Stop_input(self):
        self.shoot_button.pressed = True
        self.shooter.op_tick(1)

        self.check_motors(1.0)
        self.stop_input.state = True

        self.shooter.op_tick(2)
        self.check_motors(-1.0)

        self.stop_input.state = False
        self.shooter.op_tick(3)
        self.check_motors(-1.0)

        self.reset_input.state = True
        self.shooter.op_tick(4)
        self.check_motors(0)

    def test_shooter(self):

        self.check_motors(0)

        self.shooter.op_tick(1)

        self.check_motors(0)

        self.shoot_button.pressed = True
        self.shooter.op_tick(2)

        self.check_motors(1.0)

        self.shoot_button.pressed = False

        self.shooter.op_tick(2)

        self.check_motors(1.0)

    def check_motors(self,speed):
        for motor in self.motors:
            self.assertEquals(motor.speed, speed)

class TestArcadeDrive(unittest.TestCase):

    def setUp(self):
        self.robot_drive = mock.RobotDrive()

        self.left_joy = mock.Joystick()
        self.right_joy = mock.Joystick()

        self.photo_sensors = [ mock.DigitalInput() for x in range(5)]
        self.sqrd_button = mock.Button()
        self.tank_button = mock.Button()


        class MockDriveConfig(object):
            # Motors & Drive System
            robot_drive = self.robot_drive
            left_joy = self.right_joy
            right_joy = self.left_joy

            sqrd_button = self.sqrd_button
            tank_button = self.tank_button


        self.drive = drive.Drive(MockDriveConfig)

        self.tank_button.pressed = True
        self.drive.op_tick(1)

        self.tank_button.pressed = False

    def tearDown(self):
        pass

    def test_throttle(self):
        self.left_joy.x = 0.0

        # Sweep forward
        for y in seq(-1.0, 1.0, 0.1):
            self.left_joy.y = y

            self.drive.op_tick(100)

            self.assertEquals(self.robot_drive.speed, self.left_joy.y)
            self.assertEquals(self.robot_drive.rotation, self.left_joy.x)

        # Sweep back
        for y in seq(1.0, -1.0, -0.1):
            self.left_joy.y = y

            self.drive.op_tick(200)

            self.assertEquals(self.robot_drive.speed, self.left_joy.y)
            self.assertEquals(self.robot_drive.rotation, self.left_joy.x)

    def test_steering(self):
        self.left_joy.y = 0.0

        # Sweep forward
        for x in seq(-1.0, 1.0, 0.1):
            self.left_joy.x = x

            self.drive.op_tick(100)

            self.assertEquals(self.robot_drive.speed, self.left_joy.y)
            self.assertEquals(self.robot_drive.rotation, self.left_joy.x)

        # Sweep back
        for x in seq(1.0, -1.0, -0.1):
            self.left_joy.x = x

            self.drive.op_tick(200)

            self.assertEquals(self.robot_drive.speed, self.left_joy.y)
            self.assertEquals(self.robot_drive.rotation, self.left_joy.x)

#    def test_half_speed_throttle(self):
#        self.hs_button.pressed = True
#
#        self.left_joy.x = 0.0
#
#        # Sweep forward
#        for y in seq(-1.0, 1.0, 0.1):
#            self.left_joy.y = y
#
#            self.drive.op_tick(100)
#
#            self.assertEquals(self.robot_drive.speed, self.left_joy.y/2)
#            self.assertEquals(self.robot_drive.rotation, self.left_joy.x)
#
#       # Sweep back
#       for y in seq(1.0, -1.0, -0.1):
#           self.left_joy.y = y
#
#           self.drive.op_tick(200)
#
#           self.assertEquals(self.robot_drive.speed, self.left_joy.y/2)
#           self.assertEquals(self.robot_drive.rotation, self.left_joy.x)

#   def test_half_speed_steering(self):
#       self.hs_button.pressed = True
#
#       self.left_joy.y = 0.0
#
#       # Sweep forward
#       for x in seq(-1.0, 1.0, 0.1):
#           self.left_joy.x = x
#
#           self.drive.op_tick(1)
#
#           self.assertEquals(self.robot_drive.speed, self.left_joy.y)
#           self.assertEquals(self.robot_drive.rotation, self.left_joy.x/2)
#
#       # Sweep back
#       for x in seq(1.0, -1.0, -0.1):
#           self.left_joy.x = x
#
#           self.drive.op_tick(10)
#
#           self.assertEquals(self.robot_drive.speed, self.left_joy.y)
#           self.assertEquals(self.robot_drive.rotation, self.left_joy.x/2)


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
