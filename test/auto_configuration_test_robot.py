#!/usr/bin/env python3
#
#   This program pretends to be a robot so we can test our 
#   autonomous configuration values
#

import time
from pynetworktables import *

NetworkTable.SetServerMode()
NetworkTable.Initialize()

class Listener(ITableListener):
    def __init__(self):
        ITableListener.__init__(self)
        
    def ValueChanged(self, table, key, value, isNew):
        print('%s: %s' % (key, table.GetValue(key)))

listener = Listener()
        
table = NetworkTable.GetTable("AutoConfig")
table.AddTableListener(listener)

table.PutNumber("a", 1)
table.PutNumber("b", 2)
table.PutNumber("c", 3)

while True:
    time.sleep(1)
