#!/bin/sh

pkill mybot_rviz_gmapping.launch

roslaunch mybot_description mybot_rviz_gmapping.launch &
echo "Starting mybot_rviz_GMAPPING"