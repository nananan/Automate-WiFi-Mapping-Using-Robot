#!/bin/sh

pkill joy_node
pkill teleop_node
pkill joystick_control

roslaunch joy joy_node &
echo "Starting joy_node"

#check teleop
roslaunch teleop_twist_joy teleop_node &
echo "Starting teleop_node"

rosrun corobot_joystick joystick_control &
echo "Starting joystick_control"
