#include <ros/ros.h>
 #include <tf/transform_broadcaster.h>
 #include "math.h"
 #include "corobot_msgs/PosMsg.h"
 #include "nav_msgs/Odometry.h"
 #include <dynamic_reconfigure/server.h>
 #include <corobot_state_tf/corobot_state_tfConfig.h>
 
 long _PreviousLeftEncoderCounts = 0;
 long _PreviousRightEncoderCounts = 0;
 ros::Time current_time_encoder, last_time_encoder;
 double DistancePerCount; //to calculate - distance in meter for one count of the encoders.The Phidget C API gives the number of encoder ticks *4.
 double lengthBetweenTwoWheels; //distance in meters between the left and right wheels, taken in the middle. 
 /*Measures for Corobot:
  *Diameter of wheel = 10.5 cm
  *Distance between wheels = 21cm
  *ticks per revolution 12*52
 
   Measures forExplorer:
  *Diameter of wheel = 20.32 cm
  *Distance between wheels = 48.895cm
  *ticks per revolution ??
  */
 double x;
 double y;
 double th;
 
 double vx;
 double vy;
 double vth;
 double dt;
 
 int firstTime;
 bool isExplorer, isCorobot4WD, publish_odom_tf;
 bool odometry_activated = true;
 
 void WheelCallback(const corobot_msgs::PosMsg::ConstPtr& pos)
 {
   current_time_encoder = pos->header.stamp;
   long deltaLeft;
   long deltaRight;
   //current_time_encoder = ros::Time::now();
   dt = (current_time_encoder - last_time_encoder).toSec();
   if (dt>0.01){
           if(firstTime != 0)
           {
                 deltaLeft = (pos->px - _PreviousLeftEncoderCounts);
 
                 deltaRight = (pos->py - _PreviousRightEncoderCounts);
             
             double vl = 0.0,vr = 0.0;
             vl = ((double)deltaLeft * DistancePerCount); //distance made by the left wheel
             vr = ((double)deltaRight * DistancePerCount); //distance made by the right wheel
             
             vx = (vl+vr)/2.0;
             vth = (vr-vl)/lengthBetweenTwoWheels; //rotation made by the robot
             double delta_x = 0.0, delta_y = 0.0, delta_th = 0.0;
             delta_x = (vx * cos(th) - vy * sin(th));
             delta_y = (vx * sin(th) + vy * cos(th));
             delta_th = vth;
             x += delta_x;
             y += delta_y;
             int mod = (int) ((th+delta_th)/(2*M_PI));
             th = (th+ delta_th) -(mod*2*M_PI);
           }
           else
             firstTime = 1;
           _PreviousLeftEncoderCounts = pos->px;
           _PreviousRightEncoderCounts = pos->py;
           last_time_encoder = current_time_encoder;
     }
 }
 
 void dynamic_reconfigureCallback(corobot_state_tf::corobot_state_tfConfig &config, uint32_t level) {
                 odometry_activated = config.camera_state_tf;
 }
 
 int main(int argc, char** argv){
   ros::init(argc, argv, "corobot_state_tf");
   ros::NodeHandle n;
   ros::NodeHandle nh("~");
   nh.param("Explorer", isExplorer, false);
   nh.param("Corobot4WD", isCorobot4WD, true);
   nh.param("publish_odom_tf", publish_odom_tf, true);
 
     dynamic_reconfigure::Server<corobot_state_tf::corobot_state_tfConfig> server;
     dynamic_reconfigure::Server<corobot_state_tf::corobot_state_tfConfig>::CallbackType f;
 
     f = boost::bind(&dynamic_reconfigureCallback, _1, _2);
     server.setCallback(f);
   if (isExplorer)
   {
         DistancePerCount = (M_PI*0.2032)/(500.0*59.0*4.0);
         lengthBetweenTwoWheels = 0.48895;
   }
   else if (isCorobot4WD)
   {
         DistancePerCount = (M_PI*0.109)/(12.0*52.0*4.0);
         lengthBetweenTwoWheels = 0.31 + 0.03; //length between left front and rear right wheel, plus a little more to compensate for the slipping 
   }
   else
   {
         DistancePerCount = (M_PI*0.109)/(12.0*52.0*4.0);
         lengthBetweenTwoWheels = 0.282;
   }
   _PreviousLeftEncoderCounts = 0;
   _PreviousRightEncoderCounts = 0;
   vx = 0;
   vy = 0;
   vth = 0;
   firstTime = 0;
 
   ros::Subscriber sub = n.subscribe("/position_data", 1000, WheelCallback);
   ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odometry", 50);   
   tf::TransformBroadcaster odom_broadcaster;
 
   ros::Rate r(50);
   ros::Rate r_deactivated(2);
 
   tf::TransformBroadcaster broadcaster;
 
   while(n.ok()){
     ros::spinOnce();
     if (odometry_activated)
     {
             if (isExplorer)
                 broadcaster.sendTransform(tf::StampedTransform(tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.2413, 0, 0)),ros::Time::now(),"base_footprint", "hokuyo"));
             else
                 broadcaster.sendTransform(tf::StampedTransform(tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.15, 0, 0)),ros::Time::now(),"base_footprint", "hokuyo"));
 
             //since all odometry is 6DOF we'll need a quaternion created from yaw
             geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(th);
             geometry_msgs::Quaternion odom_quat2 = tf::createQuaternionMsgFromYaw(0);
 
             //first, we'll publish the transform over tf
             geometry_msgs::TransformStamped odom_trans;
             odom_trans.header.stamp = ros::Time::now();
             odom_trans.header.frame_id = "odom";
             odom_trans.child_frame_id = "base_footprint";
 
             odom_trans.transform.translation.x = x;
             odom_trans.transform.translation.y = y;
             odom_trans.transform.translation.z = 0.0;
             odom_trans.transform.rotation = odom_quat;
 
             geometry_msgs::TransformStamped odom_trans2;
             odom_trans2.header.stamp = current_time_encoder;
             odom_trans2.header.frame_id = "base_footprint";
             odom_trans2.child_frame_id = "base_link";
 
             odom_trans2.transform.translation.x = 0;
             odom_trans2.transform.translation.y = 0;
             odom_trans2.transform.translation.z = 0.0;
             odom_trans2.transform.rotation = odom_quat2;
 
 
             //send the transform
             if(publish_odom_tf)
                 odom_broadcaster.sendTransform(odom_trans);
             odom_broadcaster.sendTransform(odom_trans2);
 
             //next, we'll publish the odometry message over ROS
             nav_msgs::Odometry odom;
             odom.header.stamp = current_time_encoder;
             odom.header.frame_id = "odom";
 
             //set the position
             odom.pose.pose.position.x = x;
             odom.pose.pose.position.y = y;
             odom.pose.pose.position.z = 0.0;
             odom.pose.pose.orientation = odom_quat;
             odom.pose.covariance[0] = 0.01;
             odom.pose.covariance[7] = 0.01;
             odom.pose.covariance[14] = 10000;
             odom.pose.covariance[21] = 10000;
             odom.pose.covariance[28] = 10000;
             odom.pose.covariance[35] = 0.1;
 
 
             //set the velocity
             odom.child_frame_id = "base_link";
             if (dt!=0)
             {
                 odom.twist.twist.linear.x = vx/dt;
                 odom.twist.twist.linear.y = vy/dt;
                 odom.twist.twist.angular.z = vth/dt;
             }
             else
             {
                 odom.twist.twist.linear.x = 0;
                 odom.twist.twist.linear.y = 0;
                 odom.twist.twist.angular.z = 0;
             }
             odom.twist.covariance[0] = 0.01;
             odom.twist.covariance[7] = 0.01;
             odom.twist.covariance[14] = 10000;
             odom.twist.covariance[21] = 10000;
             odom.twist.covariance[28] = 10000;
             odom.twist.covariance[35] = 0.1;
 
             //publish the message
             odom_pub.publish(odom);
 
             r.sleep();
         }
         else
             r_deactivated.sleep();
   }
 }