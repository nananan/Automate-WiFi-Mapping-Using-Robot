# Automate-WiFi-Mapping-Using-Robot
We presented an autonomous differential-drive robot whose task is to map the presence of IEEE 802.11 radio sources and their signal strength.
In this work, we scan the whole area in which the robot is deployed and create a 2D map of the surrounding environment, by using a LiDAR sensor. Then, after having reconstructed the environment, the robot will begin the exploration phase whose task will be to identify and map radio sources. To perform this analysis we used Cinnamon, a module which I developed during my bachelor thesis work, that monitors a WiFi network and analyzes 802.11 frames. After the exploration phase, we have that the robot has managed to reconstruct the position of each Access Point. Mapped data can be graphically visualized through a specifically developed tool, written in Python.

## Preparation of System
To use this work, we need a version of ROS. We used the Kinetic version. Then, we need to install and configure a MySQL/MariaDB database. For Linux we use the following guide to install and configure the DB:
- https://thishosting.rocks/install-mysql-mariadb-ubuntu/
- https://www.kaffeetalk.de/how-to-setup-and-configure-mysql-with-unixodbc-under-ubuntu-14-04/

Then, we use the file **create_table.sql** in the *cinnamon* folder to create all the tables needed to save the data.
In the execution of this work we used the root user on the DB.

## Running
First of all, we must launch the master node and to do this we launch in the console the command `roscore`. Then, we must connect the LiDAR laser, mounted on the robot. First, we assure that the laser is connected physically, then, in another console, we enter on the folder in which there is the launch file wrote to launch the laser's node (in this case, `cd catkin_ws/`) and launch `roslaunch src/hokuyo_start.launch`. In this way, we can use the laser needed in this work.

This work is based on three phases: *Reconstruct Map*, *Navigate and Collect Wireless Data*, and, finally, *Analyse the collected data*.

### Reconstruct Map
In the first phase, we must scan the area to reconstruct a 2D map of the environment, to do this we must launch some node. We launch, in different console Linux:
- `roslaunch mybot_description mybot_rviz_gmapping.launch` to have a graphical view of the robot's sensors. Indeed, this file launch RViz that takes the content of the existing topics.
- `rosrun movement c8_odom`, that creates the link between the *map* topic and the *odometry* topic.
- `roslaunch corobot_state_tf hectorSlam_robot.launch` that launch the **Hector Slam** node needed to reconstruct the map and we can start to see on RViz what the robot sees. 

Now, we must allow the robot to move. In this phase, we move the robot by using a joystick and we need to launch a joystick node. Initially, we assure us that the joystick is connected to the robot via USB cable. Then, we enter on *script* folder (`cd catkin_ws/src/script`) and we launch `./launchJoistick.sh`. In this way, we create the nodes needed to use the joystick.
Finally, we must launch the file needed to move the motors of the robot. For this, we launch `roslaunch phidget_motor PhidgetMotor.launch`.
Now, we can move the robot via joystick and we can see the updated map on RViz.
When we finish the reconstruct, we must save it and, so, we launch `rosrun map_server map_saver -f NAME_OF_MAP` and this saves two files of the reconstructed map. One is the image of the map (*NAME_OF_MAP.pgm*) and the other contains some property of the map (*NAME_OF_MAP.yaml*).

### Navigate and Collect Wireless Data
In this phase, the robot moves autonomously. So, we can disconnect the joystick. Furthermore, to prepare the ROS network needed to the navigation, we must launch:
- `roslaunch mybot_description mybot_rviz_gmapping.launch`, like in the first phase.
- `rosrun movement c8_odom`, like in the first phase.
- `roslaunch mybot_navigation amcl_demo.launch`, needed to launch the **AMCL** node that communicates with the robot and gives it the commands to reach the goal and, so, to navigate the mapped environment. If we have a different map in a different folder we can give the path by launching `roslaunch mybot_navigation amcl_demo.launch map_path:="PATH_FOLDER" map_file:="NAME_OF_MAP.yaml"`.
- `roslaunch corobot_launch motors.launch`, to launch the node needed to start the motors of the robot.
In this way, we create the network ROS needed to allow the robot to move. 

Since we had created the DB from the root user, the next nodes need the privileges and, so, we must launch them from root user. After we are root, we launch the path needed to configure the ROS configuration, that is:
- `source /opt/ros/kinetic/setup.bash`.
- `source /home/USERNAME/git/Automate-WiFi-Mapping-Using-Robot/catkin_ws/devel/setup.bash`.

First, to give the goals to the robot, since we want to save them to use afterwards, we launch `rosrun location insertWaypoints.py`. This saves the goal position in a DB. Now, we can give a goal's position to the robot by pressing the RViz's button *"Pose Estimate"* and, then, by pressing in a point in the map.

When we finish giving the goals to the robot we can stop the *insertWaypoints.py* script and we can reposition the robot to the starting point. Now, we are ready to allow the robot to move and to sniff the network to map the wireless sources. To do this we must launch two files:
- `roslaunch cinnamon cinnamon_controller.launch interface:="NAME_OF_WIRELESS_INTERFACE"`, this launches the cinnamon tool, my work of the bachelor's thesis that we modify as a python module, that sniff the 802.11 frames and save the Beacons in the DB. **N.B.** the wireless interface must be set to **monitor mode**.
- `rosrun movement sendGoals.py`, needed to give the saved goals to the robot to allow it to move autonomously.

In this way, the robot moves by following the goals' position and in the meantime it associate the frame that it receives in a moment with the position where it is located in the same moment. Every time that the robot receives a frame, the *cinnamon_controller* node creates a new data with the information about the position and save it in the DB. 

### Analyse the collected data
In this phase, finally, we can see the mapped data. This is done with a tool implemented in Python 2.7.13 that take the data from the DB and visualize them in the map created in the first phase. To view the data we must launch:
- `sudo python location.py`, this get the map image from the *navigation/mybot_navigation/map_cubo/* folder.
If we would use other images in a different folder, we can launch:
- `sudo python location.py --map_image=PATH_OF_MAP_PGM --map_yaml=PATH_OF_MAP_YAML`.

## Dependencies
- OpenCV for python
- Tkinter
- Ttkthemes
- Matplotlib

## Other Informations
This is a work of my thesis for the Master's degree, you can read it at the following link:
- https://mega.nz/#!ERshUYbS!mVrkZPPjx7VZInyIej3Mmy1xZBZ_4igxY07eHUoFwfA

The Cinnamon tool is located at the following repository:
- https://github.com/nananan/Cinnamon

The Corobot nodes are located at the following repository:
- https://github.com/morgancormier/corobot

The original nodes needed to the autonomous navigation are located at the following repository:
- https://github.com/richardw05/mybot_ws
