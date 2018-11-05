#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <iostream>
#include <std_msgs/Int32.h>
#include <corobot_msgs/MotorCommand.h>

using namespace std;

double width_robot = 0.41;
double vl = 0.0;
double vr = 0.0;
ros::Time last_time;	
double right_enc = 0.0;
double left_enc = 0.0;
double right_enc_old = 0.0;
double left_enc_old = 0.0;
double distance_left = 0.0;
double distance_right = 0.0;
double ticks_per_meter = 9435;
double x = 0.0;
double y = 0.0;
double th = 0.0;
geometry_msgs::Quaternion odom_quat;

double speed_l = 0.0;
double speed_r = 0.0;


int speed_value = 75;

void velocityCallback(const std_msgs::Int32::ConstPtr& msg)
{
	speed_value = msg->data;
}

void cmd_velCallback(const geometry_msgs::Twist &twist_aux)
{
	geometry_msgs::Twist twist = twist_aux;	
	double vel_x = twist_aux.linear.x;
	double vel_th = twist_aux.angular.z;
	double right_vel = 0.0;
	double left_vel = 0.0;

	if(vel_x == 0){  // turning
		right_vel = vel_th * width_robot / 2.0;
		left_vel = (-1) * right_vel;
	}else if(vel_th == 0){ // fordward / backward
		left_vel = right_vel = vel_x;
	}else{ // moving doing arcs
		left_vel = vel_x - vel_th * width_robot / 2.0;
		right_vel = vel_x + vel_th * width_robot / 2.0;
	}
	vl = left_vel;
	vr = right_vel;	

	ROS_ERROR_STREAM("VALUE: "<<vl<<" "<<vr);
}


int main(int argc, char** argv){
	ros::init(argc, argv, "base_controller");
	ros::NodeHandle n;
	ros::Subscriber cmd_vel_sub = n.subscribe("cmd_vel", 10, cmd_velCallback);
	ros::Publisher driveControl_pub = n.advertise<corobot_msgs::MotorCommand>("PhidgetMotor",100);
	ros::Subscriber velocity = n.subscribe<std_msgs::Int32>("velocityValue", 1000, velocityCallback);
//avevo messo 20 prima
const double vel_const = 30;

	ros::Rate loop_rate(10);

	while(ros::ok())
	{


		speed_r = vr * vel_const;
		speed_l = vl * vel_const;
	
		if (speed_l > vel_const)
			speed_l = vel_const;
		if (speed_l < -vel_const)
			speed_l = -vel_const;
		if (speed_r > vel_const)
			speed_r = vel_const;
		if (speed_r < -vel_const)
			speed_r = -vel_const;	

		corobot_msgs::MotorCommand msg_com;
		msg_com.leftSpeed = speed_l;
		msg_com.rightSpeed = speed_r;
		msg_com.secondsDuration = 3;
		msg_com.acceleration = 15;

		driveControl_pub.publish(msg_com);
		ros::spinOnce();
		loop_rate.sleep();
	}
}
