import common

__all__ = ["UtilComponent"]

class UtilComponent(common.ComponentBase):

    def __init__(self, config):
        self.reload_code_button = config.reload_code_button
        self.compressor = config.compressor
        self.compressor.Start()

    def disabled_tick(self, timestamp):
        print('test')
        if self.reload_code_button.get():
            print("reloading code")
            raise SystemExit
