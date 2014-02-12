import common


__all__ = ["UtilComponent"]


class UtilComponent(common.ComponentBase):

	def __init__(self, config):
		self.reset_button = config.reset_button
		self.compressor = config.compressor
		self.compressor.Start()

	def disabled_tick(self, timestamp):
		if self.reset_button.get():
			raise SystemExit
