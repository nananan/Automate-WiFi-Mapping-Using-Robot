#!/bin/sh

pkill c8_odom

rosrun movement c8_odom &
echo "Starting C8_ODOM"