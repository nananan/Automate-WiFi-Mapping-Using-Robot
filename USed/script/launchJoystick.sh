#!/bin/sh

pkill joy_node
pkill teleop_node
pkill joystick_control

rosrun joy joy_node &
echo "Starting joy_node"

#check teleop
rosrun teleop_twist_joy teleop_node &
echo "Starting teleop_node"

rosrun corobot_joystick joystick_control &
echo "Starting joystick_control"
