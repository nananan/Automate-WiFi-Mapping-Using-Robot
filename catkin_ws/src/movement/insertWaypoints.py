#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

import imp
db_man = imp.load_source('DB_Manager', '/home/wallf/git/Cinnamon/db.py')


def goal_callback( goal_pose):
	print(goal_pose)

if __name__ == '__main__':
	try:
		rospy.init_node('waypoint_controller', anonymous=False)

	        rospy.Subscriber('move_base_simple/goal', PoseStamped, goal_callback)

		rospy.loginfo("Started ")
		# Sleep to give the last log messages time to be sent
		rospy.sleep(10)

	except rospy.ROSInterruptException:
		rospy.loginfo("Ctrl-C caught. Quitting")
