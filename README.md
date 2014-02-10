# TODO

* Use [pyfrc](https://github.com/robotpy/pyfrc)
* Get vision processing working to detect when goal is hot
* Write autonomous code
* Write shooter code
* Write picker upper code
* Move line-aligning code to 2014 bot

# Getting Started

We use python (Yay!)

Python is not officially supported by FRC, so we use [RobotPy](http://firstforge.wpi.edu/sf/projects/robotpy). RobotPy runs a python interpreter on the cRio and provides
python bindings to *most* of the wpilib.

## Setting up a cRio for this codebase

If the cRio has been used to run different code, follow these steps:

* [Image the cRio with the C++ image](http://wpilib.screenstepslive.com/s/3120/m/8559/l/89727-imaging-your-crio)
* Download the [latest RobotPy](http://firstforge.wpi.edu/sf/frs/do/listReleases/projects.robotpy/frs.robotpy)
* Unzip the robot archive
* Run the `install.py` inside the unzipped folder while the cRio is connected to the computer.

## change/build/test workflow

THIS NEEDS TO BE FILLED OUT

## IP Addresses

10.29.28.1   - FMS
10.29.28.2   - cRio
10.29.28.5   - Computer
10.29.28.11 - Axis

# Shooting strategies

* Jam robot against corner goal, shoot low goal
* Jam robot against corner goal, shoot high goal
  - If not possible to make high goal (need to test), back up by specific amount before shooting
* Square against wall, shoot from variable distance (use sonars to square and detect speed needed)
* Square up with zone line, fire at fixed speed to high goal (can use line sensors square)
* Square up on goal line, fire at fixed speed at high goal (can use line sensors to square)
* Shoot whenever you want at whatever speed you want

# Planning

## Autonomous Mode Plan

* With humans, square up robot to wall at consistent distance from wall
* Wait until Axis camera detects goal is hot
* Shoot ball 
* Drive forward with dead reckoning into zone area

## Robot Commands

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


