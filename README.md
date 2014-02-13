# Getting Started

We use python (Yay!)

Python is not officially supported by FRC, so we use [RobotPy](http://firstforge.wpi.edu/sf/projects/robotpy). 
RobotPy runs a python interpreter on the cRio and provides python bindings to *most* of the wpilib.

## Learn Python

* Finish the [Python Codecademy course](http://www.codecademy.com/tracks/python). *Almost* everything covered 
  there is used in our Python code. You should finish the course before coding the robot.
* If you want to get better, try solving the [beginners problems on CodeAbbey](http://codeabbey.com/index/task_list/beginners-problems). 
  This is not necessary to program the robot.

## Learn how to program an FRC Robot with Python

* You should have a thorough understanding of the [WPILib Documentation](http://wpilib.screenstepslive.com/s/3120/m/7912)
  . This will give you an understanding of what's possible with the Robot. There are also step-by-step 
  guides for coding some things, such as mecanum drive.
* There is [example Python code in the RobotPy code base](https://github.com/robotpy/robotpy/tree/2014/samples).
* RobotPy wraps the C++ implementation of WPILib, therefore we have to use the C++ documentation. For detailed 
  C++ documentation, see [Virtual Roadside](http://www.virtualroadside.com/WPILib/annotated.html).

## Install PyFRC on Your Computer

* Download the [latest PyFRC package](https://github.com/VikingRobotics/pyfrc)
* Unzip the contents
* cd into the directory
* Run `python setup.py install`

## Setting up a cRio for this codebase

If the cRio has been used to run different code, follow these steps:

* [Image the cRio with the C++ image](http://wpilib.screenstepslive.com/s/3120/m/8559/l/89727-imaging-your-crio)
* Download the [latest RobotPy](http://firstforge.wpi.edu/sf/frs/do/listReleases/projects.robotpy/frs.robotpy)
* Unzip the robot archive
* Run the `install.py` inside the unzipped folder while the cRio is connected to the computer.

## change/build/test workflow

THIS NEEDS TO BE FILLED OUT

## IP Addresses

10.29.28.1     - Router
10.29.28.2     - cRio
10.29.28.5/6   - Computer
10.29.28.11    - Axis

# Planning

## Shooting strategies

* Jam robot against corner goal, shoot low goal
* Jam robot against corner goal, shoot high goal
  - If not possible to make high goal (need to test), back up by specific amount before shooting
* Square against wall, shoot from variable distance (use sonars to square and detect speed needed)
* Square up with zone line, fire at fixed speed to high goal (can use line sensors square)
* Square up on goal line, fire at fixed speed at high goal (can use line sensors to square)
* Shoot whenever you want at whatever speed you want

## Autonomous Mode Plan

* With humans, square up robot to wall at consistent distance from wall
* Wait until Axis camera detects goal is hot
* Shoot ball 
* Drive forward with dead reckoning into zone area

## Functions we want the robot to do

shoot(shootingSpeed)
  - extend picker upper
  - set speed of motor for x seconds to shootingSpeed
  - reset() (Q: auto or manual reset for shooting?)

reset()
  - arm moves in reverse at fixed speed
  - stop arm moving once hall effect detected
  - retract picker upper

pickupExtend()
  - extend picker upper

enableRollers(speed)
  - turn on rollers to given speed

pickupRetract()
  - retract picker upper

spitOut(speed)
  - reverse rollers to given speed

alignOnLine() 
  - robot starts behind line
  - orient robot perpendicular to line using light sensors

alignOnWall()
  - square robot against wall using sonars 

# TODO

* Go over pyfrc
* Go over changes that fixed errors in the code
* Fix the code (try `python3 robot.py sim` and teleop it. It crashes)
* Move declarations in config.py to all be in one spot at the top, then use named arguments in component constructors instead of config objects
* rename variables to be more descriptive
* Make sure Paul's code works

* Get vision processing working to detect when goal is hot
* Comment the code
* Write shooter code
* Write picker upper code
* Write autonomous code
* Add [motor safety feature to shooter](http://wpilib.screenstepslive.com/s/3120/m/7912/l/79730-using-the-motor-safety-feature)
* Add SmartDashboard stuff

* Use [pyfrc](https://github.com/robotpy/pyfrc)
* Check out the Robot.py netconsole in utilities/netconsole/netconsole.py
