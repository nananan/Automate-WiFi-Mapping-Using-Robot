#!/bin/sh

pkill c8_odom

roslaunch chapter8_tutorials c8_odom &
echo "Starting C8_ODOM"