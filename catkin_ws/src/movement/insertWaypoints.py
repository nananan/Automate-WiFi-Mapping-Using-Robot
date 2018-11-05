#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

import imp
db_man = imp.load_source('DB_Manager', '/home/wallf/git/Cinnamon/db.py')


class WaypointsController:
	def __init__(self):
		self.db_manager = db_man.DB_Manager()

		rospy.init_node('waypoint_controller', anonymous=False)
		rospy.loginfo("Started ")

		self.goal_subscriber = rospy.Subscriber('move_base_simple/goal', PoseStamped, self.goal_callback)

	def goal_callback(self, goal_pose):
		print(goal_pose)
		pose = goal_pose.pose
		orientation = goal_pose.orientation

		record = OrderedDict([("position_x",pose.x),("position_y",pose.y),("position_z",pose.z),
				("orientation_x": orientation.x), ("orientation_y": orientation.y), ("orientation_z": orientation.z), 
				("orientation_w": orientation.w)])
		self.db_manager.insert_Waypoint(record)

if __name__ == '__main__':
	try:
		waypoint_controller = WaypointsController()
		waypoint_controller.spin() #In this application all user callbacks will be called from within the ros::spin() call. ros::spin()
									#will not return until the node has been shutdown, either through a call to ros::shutdown() or a Ctrl-C. 
		# Sleep to give the last log messages time to be sent
		rospy.sleep(10)

	except rospy.ROSInterruptException:
		rospy.loginfo("Ctrl-C caught. Quitting")
