#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

import imp
db_man = imp.load_source('DB_Manager', '../cinnamon/db.py')

import actionlib
from actionlib_msgs.msg import *

from trajectory_msgs.msg import *
from visualization_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

from collections import OrderedDict


class GoToPose():
	def __init__(self):

		self.goal_sent = False

		# What to do if shut down (e.g. Ctrl-C or failure)
		rospy.on_shutdown(self.shutdown)
		
		# Tell the action client that we want to spin a thread by default
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		rospy.loginfo("Wait for the action server to come up")

		# Allow up to 5 seconds for the action server to come up
		self.move_base.wait_for_server(rospy.Duration(5))

	def goto(self, pos, quat):

		# Send a goal
		self.goal_sent = True
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = 'map'
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], pos['w']),
									 Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

		# Start moving
		self.move_base.send_goal(goal)

		# Allow TurtleBot up to 60 seconds to complete task
		success = self.move_base.wait_for_result(rospy.Duration(60)) 

		state = self.move_base.get_state()
		result = False

		if success and state == GoalStatus.SUCCEEDED:
			# We made it!
			result = True
		else:
			self.move_base.cancel_goal()

		self.goal_sent = False
		return result

	def shutdown(self):
		if self.goal_sent:
			self.move_base.cancel_goal()
		rospy.loginfo("Stop")
		rospy.sleep(1)

if __name__ == '__main__':
	try:
		rospy.init_node('nav_test', anonymous=False)
		navigator = GoToPose()
		count = 1
		DB_Man = db_man.DB_Manager()
		waypoints = DB_Man.select_Waypoints()
		for item in waypoints:
			print(item)
			position = {'x': item.position_x, 'y' : item.position_y, 'w': item.position_z}
			quaternion = {'r1' : item.orientation_x, 'r2' : item.orientation_y, 'r3' : item.orientation_z, 'r4' : item.orientation_w}

			rospy.loginfo("Go to (%s, %s, %s) pose", position['x'], position['y'], position['w'])
			success = navigator.goto(position, quaternion)

			if success:
				rospy.loginfo("I'm here now... (%s, %s) pose", position['x'], position['y'])
			else:
				rospy.loginfo("The base failed to reach the desired pose")
			count = count+1
			# Sleep to give the last log messages time to be sent
			rospy.sleep(1)

	except rospy.ROSInterruptException:
		rospy.loginfo("Ctrl-C caught. Quitting")
