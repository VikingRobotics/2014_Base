
class PIDController(object):
	def __init__(self, p, i, d, in_var, setpoint):
		self.kp = p
		self.ki = i
        self.kd = d

        self.in_var = in_var
        self.p_input = 0
        
        set_setpoint(setpoint)

        self.i_term = 0

        self.max_out = 1
        self.min_out = -1

        self.enabled = True

    def compute(self):
        if not self.enabled:
            reutrn

        _input = self.in_var()
        
        self.error = self.setpoint - _input

        self.i_term += self.ki * self.error
        if self.i_term > self.max_out:
            self.i_term = self.max_out
        elif self.i_term < self.min_out:
            self.i_term = self.min_out

        d_input = _input - self.p_input

        self.output = self.kp*self.error + self.i_term + self.kd*d_input

        if output > self.max_out:
            output = self.max_out
        elif output < self.min_out:
            output = self.min_out

        self.p_input = _input

        return self.output

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

    def enable(self):
        self.enabled = True
        reinitialize()

    def disable(self):
        self.enabled = False

    def reinitialize(self):
        self.p_input = self.in_var()
        self.i_term = self.output
