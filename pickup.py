import common


__all__ = ['Pickup']


class Pickup(common.ComponentBase):
	
	def __init__(self, config):
		self.motor = config.pickup_motor
		self.solenoid = config.solenoid

		self.forward = config.forward
		self.reverse = config.reverse

		self.out_button = config.out_button
		self.in_button = config.in_button
		self.motor_button = config.motor_button

		self.speed_axis = config.speed_axis

	def op_init(self):
		pass

	def op_tick(self, time):
		speed = 0
		if self.motor_button.get():
			speed = self.speed_axis.get()
		self.motor.Set(speed)

		if self.out_button.get():
			self.solenoid.Set(self.forward)
		if self.in_button.get():
			self.solenoid.Set(self.reverse)