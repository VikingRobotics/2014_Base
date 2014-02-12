import common


__all__ = ["Reboot"]


class Reboot(common.ComponentBase):

	def __init__(self, config):
		self.reset_button = config.reset_button

	def disabled_tick(self, timestamp):
		if self.reset_button.get():
			raise SystemExit