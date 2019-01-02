# SniffingRobot
This work is my master's thesis and we presented an autonomous differential-drive robot whose task is to map the presence of IEEE 802.11 radio sources and their signal strength.
In this work, we scan the whole area in which the robot is deployed and create a 2D map of the surrounding environment, by using a LiDAR sensor. Then, after having reconstructed the environment, the robot will begin the exploration phase whose task will be to identify and map radio sources. To perform this analysis we used Cinnamon, a module which I developed during my bachelor thesis work, that monitors a WiFi network and analyzes 802.11 frames. After the exploration phase, we have that the robot has managed to reconstruct the position of each Access Point. Mapped data can be graphically visualized through a specifically developed tool, written in Python.

## Running
First of all, and needed to all the phases, we must launch the master node and to do this we launch in console the command `roscore`. Then, we must connect the LiDAR laser, mounted on the robot. First, we assure that the laser is connected phisically, then, in another console, we enter on the folder in which there is the launch file wrote to launch the laser's node (in this case, `cd catkin_ws/`) and launch `roslaunch src/hokuyo_start.launch`. In this way, we can use the laser needed in this work.

This work is based on three phases: *Reconstruct Map*, *Navigate and Collect Wireless Data*, and, finally, *Analyse the collected data*.

### Reconstruct Map
In the first phase, we must scan the area to reconstruct a 2D map of the environment, to do this we must launch some node. We launch `roslaunch mybot_description mybot_rviz_gmapping.launch` to have a graphical view of the robot's sensors. Indeed, this file launch RViz that takes the content of the existing topics. Then, we must launch the **Hector Slam** node needed to recostruct the map, so, we launch `roslaunch corobot_state_tf hectorSlam_robot.launch`. By launching this file, we see that we have some error that we resolve by launching `rosrun movement c8_odom`. This last creates the link between the *map* topic and the *odometry* topic and we can start to see on RViz what the robot sees. 
Now, we must move the robot. In this phase we move the robot by using a joystick and we need to launch a joystick node. Initially we assure that the joystick is connected to the robot via usb cable. Then, enter on *script* folder (`cd catkin_ws/src/script`) and we launch `./launchJoistick.sh`. In this way, we create the nodes needed to use the joystick.
Finally, we must launch the file needed to move the motor of the robot. For this, we can launch `roslaunch phidget_motor PhidgetMotor.launch`.
Now, we can move the robot via Joystick and we can see the updated map on RViz.
When we finish to reconstruct, we must save it and, so, we launch `rosrun map_server map_saver -f NAME_OF_MAP` and this saves two file of the reconstructed map. One is the image of the map and the other contains some property of the map.

### Navigate and Collect Wireless Data
