"""
File for base classes used by other modules.
"""

class ComponentBase(object):

    def robot_init(self):
        pass

    def auto_init(self):
        pass

    def auto_tick(self, time):
        pass

    def disabled_init(self):
        pass

    def disabled_tick(self, time):
        pass

    def op_init(self):
        pass

    def op_tick(self, time):
        pass

