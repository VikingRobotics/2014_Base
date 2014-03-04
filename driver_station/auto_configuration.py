# Very basic command line interface to let us configure
# the robots autonomous values without changing

import sys
import time
from pynetworktables import *

if len(sys.argv) != 2:
    print("Usage: python auto_configuration.py <ip>")
    exit(0)

ip = sys.argv[1]
tablename = "AutoConfig"

NetworkTable.SetIPAddress(ip)
NetworkTable.SetClientMode()
NetworkTable.Initialize()

def clearscreen(numlines=100):
    """Clear the console.
    numlines is an optional argument used only as a fall-back.
    """
    import os
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')
    else:
        # Fallback for other operating systems.
        print('\n' * numlines)

# Listen to new table values and add em to our dict
class Listener(ITableListener):
    listening = False
    def __init__(self):
        ITableListener.__init__(self)
        
    def ValueChanged(self, table, key, value, isNew):
        self.listening = True
        table_dict[key] = table.GetValue(key)


listener = Listener()
        
table = NetworkTable.GetTable(tablename)
table.AddTableListener(listener)
table_dict = {}

# wait until we're connected to the tables
while not listener.listening:
  time.sleep(1)

# input loop
while True:
    clearscreen()

    # print current table
    print("Current auto config:")
    print()
    for k, v in sorted(table_dict.items()):
      print("%s\t%s" % (k,v))
    print()

    # User input
    key = input("key: ")
    val = input("val: ")

    try:
      val = int(val)
      table.PutNumber(key, val)
    except:
      print("error")
