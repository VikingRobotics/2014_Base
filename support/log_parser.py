import sys

if len(sys.argv) < 2:
	print("Usage: python shooter_log_parsers.py <input_filename>")
	sys.exit()

input_filename = sys.argv[1]
file = open(input_filename)

print("logger,battery_voltage,shooting_preset,shoot_seconds,shooting_speed")
for line in file:
	if "SHOOTER_LOGGER" in line:
		print(line[0:-1])

