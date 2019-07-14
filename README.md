#  OpenPose to robotics!
<p align="center">
  <img src="https://github.com/fabian57fabian/OpenPose-to-robotics/blob/master/images/OPtoROBO.png">
</p>

**OPtoROBO** is an entertainment system to drive some robotic stuff such like your own **RC car**, a **Robotic arm** and one day we'll be driving **drones**. Or maybe not.

## How?
Simply place in front of your webcam, start **OPtoROBO** and drive your car using hands gestures (moving up, down, steering).
A simple graphical interface is there to help you. [See intro video](https://youtu.be/VZsERaSSXtw).

[![Intro video](https://img.youtube.com/vi/VZsERaSSXtw/hqdefault.jpg)](https://youtu.be/VZsERaSSXtw)

## Technology
We're currently using [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to detect human body and processing that data to drive your car. We're using a cool DIY arduino car with bluetooth connection but any RC car with programmable MCU unit onboard will be allright. Check out the [arduino code](https://github.com/fabian57fabian/OpenPose-to-robotics/blob/master/Controllers/ArduinoCarSketch/ArduinoCarSketch.ino) using this [connections circuit](https://github.com/fabian57fabian/OpenPose-to-robotics/blob/master/images/CarMainSketch_image.png) for arduino car with one dc motor and a servo for steering. If you have an RC car with only 2 wheels use the other [arduino code for 2 wheels](https://github.com/fabian57fabian/OpenPose-to-robotics/blob/master/Controllers/ArduinoCarSketch_2Wheel/ArduinoCarSketch_2Wheel.ino) with [this schematics](https://github.com/fabian57fabian/OpenPose-to-robotics/blob/master/images/CarSecondarySketch_image.png).
Feel free to change global vars according to your project (like speed_balance in 2wheel sketch if you have one motor faster than the other).

# Installation
1. Before doing anything, **clone** and **install** [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) and follow the instructions (good luck there, it's quite difficult).
2. **Clone** this repo inside {OpenPoseClonedRepo}/build/examples/tutorial_api_python/ with:
```
git clone https://github.com/fabian57fabian/OpenPose-to-robotics.git .
```
If you are under Windows, you'll need first to **move avay** all files and folder inside the **tutorial_api_python** folder, then clone and move back again.
3. Install all **python needed modules** (using pip it's easyer). OpenCv would be already been installed by OpenPose.
```
pip3 install pyserial
```
4. To run **OPtoROBO** from your terminal just enter the {OpenPoseClonedRepo}/build/examples/tutorial_api_python/ folder and type:
```
python3 IVA_project.py
```

## Requirements
Well, OpenPose will need a good GPU so make sure to use a good one.
Tests show that on a **GTX 1050** works at 6 fps and on a **GTX 1660ti** works at 19 fps.

## Contributors
The entire project was made by [Lorenzo Pisaneschi](https://github.com/pisalore) and [Fabian Greavu](https://github.com/fabian57fabian)
