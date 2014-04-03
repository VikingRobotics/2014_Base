
class PIDController(object):
	def __init__(self, p, i, d, in_var, setpoint):
		self.kp = p
		self.ki = i
        self.kd = d

        self.in_var = in_var
        self.setpoint = setpoint

        self.p_error = setpoint - in_var
        self.error_sum = self.p_error

    def compute(self, delta_time, in_var):
        self.error = self.setpoint - in_var()
        self.error_sum += self.error * delta_time

        d_error = (self.error - self.p_error) / delta_time

        output = self.kp*self.error + self.ki*self.error_sum + self.kd*d_error

        return output

    def set_vars(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
