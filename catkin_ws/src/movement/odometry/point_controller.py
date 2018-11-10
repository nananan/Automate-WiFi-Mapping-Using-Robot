#!/usr/bin/env python

import roslib; #roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

from mapping import Mapping

class PointController:
    def __init__(self):
        self.map_manager = Mapping()
        self.AP = self.map_manager.getAPs()

        self.list_color = [["red","violet"],["blue","green"],["orange","black"]]
        self.norm = matplotlib.colors.Normalize(vmin=-90, vmax=-20)
        #NODE FOR ROS
        rospy.init_node("point_controller")
        self.publisher = rospy.Publisher('/visualization_marker_array', MarkerArray)
        self.markerArray = MarkerArray()

        self.rate = rospy.Rate(10)

    def publish_marker(self):
        col = 0
        id_marker = 0
        for ap in self.AP:
            print(ap[0])
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", self.list_color[col])

            for key, value in self.map_manager.createMappingAP(ap[0]).items():
                print(key, value, cmap(self.norm(value))[:3])
                color = cmap(self.norm(value))[:3]
                # print(self.norm(value))
                # print("COLOR: ",color[0],color[1],color[2])
                # print("POSITION: ",key[0],key[1],key[2])
                marker = Marker()
                marker.id = id_marker
                id_marker = id_marker+1
                marker.header.frame_id = "/map"
                marker.type = marker.SPHERE
                marker.action = marker.ADD
                marker.scale.x = 0.2
                marker.scale.y = 0.2
                marker.scale.z = 0.2
                marker.color.a = 1.0
                marker.color.r = color[0]
                marker.color.g = color[1]
                marker.color.b = color[2]
                #marker.pose.orientation.w = 1.0
                marker.pose.position.x = key[0]
                marker.pose.position.y = key[1] 
                marker.pose.position.z = key[2]
                # marker.lifetime = rospy.Duration(0)
                
                self.markerArray.markers.append(marker)

            col = col+1
            if col >= len(self.list_color):
                col = 0

    #     marker = Marker()
    #     marker.header.frame_id = "/map"
    #     marker.type = marker.SPHERE
    #     marker.action = marker.ADD
    #     marker.scale.x = 0.2
    #     marker.scale.y = 0.2
    #     marker.scale.z = 0.2
    #     marker.color.a = 1.0
    #     marker.color.r = 1.0
    #     marker.color.g = 1.0
    #     marker.color.b = 0.0
    #     marker.pose.orientation.w = 1.0
    #     marker.pose.position.x = 2.0
    #     marker.pose.position.y = 2.0 
    #     marker.pose.position.z = 1.0
	#     marker.lifetime = rospy.Duration(0)
        
    #     self.markerArray.markers.append(marker)

    #     # Renumber the marker IDs
	#     #marker.id = 0
        # id = 0
        # for m in self.markerArray.markers:
        #     m.id = id
        #     id += 1
        while not rospy.is_shutdown():
            # Publish the MarkerArray
            self.publisher.publish(self.markerArray)
            #print "sending marker", marker.pose.position
            self.rate.sleep()

    # def spin(self):
	# 	while not rospy.is_shutdown():
	# 		self.rate.sleep()

if __name__ == '__main__':
    point_controller = PointController()
    point_controller.publish_marker()

