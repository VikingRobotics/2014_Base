
class PIDController(object):
	def __init__(self, p, i, d, in_var, setpoint):
		self.kp = p
		self.ki = i
        self.kd = d

        self.in_var = in_var
        self.setpoint = setpoint

        self.p_error = setpoint - in_var
        self.error_sum = self.p_error
        
        self.max_out = 1
        self.min_out = -1

    def compute(self, delta_time, in_var):
        self.error = self.setpoint - in_var()
        self.error_sum += self.error * delta_time

        d_error = (self.error - self.p_error) / delta_time

        output = self.kp*self.error + self.ki*self.error_sum + self.kd*d_error

        if output > self.max_out:
            output = self.max_out
        elif output < self.min_out:
            output = self.min_out

        return output

    def set_vars(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_output_limits(self, _min, _max):
        if abs(_max) > 1:
            _max = abs(_max) / _max
        if abs(_min) > 1:
            _min = abs(_min) / _min

        self.max_out = _max
        self.min_out = _min
