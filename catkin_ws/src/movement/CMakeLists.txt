cmake_minimum_required(VERSION 2.8.3)
project(chapter8_tutorials)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  dynamixel_msgs
  geometry_msgs
  joy
  nav_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  tf
  pcl_conversions
  pcl_ros
  corobot_msgs
  move_base_msgs
)

## System dependencies are found with CMake's conventions
 find_package(PCL REQUIRED)
 include_directories(
  ${PCL_INCLUDE_DIRS}
)
link_directories(
  ${PCL_LIBRARY_DIRS}
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(

)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)

include_directories(include ${catkin_INCLUDE_DIRS})

add_dependencies(joystick_control corobot_msgs_gencpp)
add_dependencies(sendGoals ${catkin_EXPORTED_TARGETS})

## Declare a C++ executable
add_executable(c8_odom odometry/c8_odom.cpp)
add_executable(sendGoals src/sendGoals.cpp)

## Specify libraries to link a library or executable target against

target_link_libraries(c8_odom ${catkin_LIBRARIES})
target_link_libraries(sendGoals ${catkin_LIBRARIES})