#!/usr/bin/env python

import roslib; roslib.load_manifest('arbotix_python')
import rospy
import sys

from arbotix_msgs.msg import *
from arbotix_msgs.srv import *

from arbotix_python.arbotix import ArbotiX
from arbotix_python.diff_controller import DiffController
from arbotix_python.follow_controller import FollowController
from arbotix_python.servo_controller import *
from arbotix_python.linear_controller import *
from arbotix_python.publishers import *
from arbotix_python.io import *

# name: [ControllerClass, pause]
controller_types = { "follow_controller" : FollowController,
                    "diff_controller"   : DiffController,
#                    "omni_controller"   : OmniController,
                    "linear_controller" : LinearControllerAbsolute,
                    "linear_controller_i" : LinearControllerIncremental }

###############################################################################
# Main ROS interface
class ArbotixROS(ArbotiX):
    
    def __init__(self):
        pause = False

        # load configurations    
        port = rospy.get_param("~port", "/dev/ttyUSB0")
        baud = int(rospy.get_param("~baud", "115200"))

        self.rate = rospy.get_param("~rate", 100.0)
        self.fake = rospy.get_param("~sim", False)

        self.use_sync_read = rospy.get_param("~sync_read",True)      # use sync read?
        self.use_sync_write = rospy.get_param("~sync_write",True)    # use sync write?

        # setup publishers
        self.diagnostics = DiagnosticsPublisher()
        self.joint_state_publisher = JointStatePublisher()

        # start an arbotix driver
        if not self.fake:
            ArbotiX.__init__(self, port, baud)        
            rospy.sleep(1.0)
            rospy.loginfo("Started ArbotiX connection on port " + port + ".")
        else:
            rospy.loginfo("ArbotiX being simulated.")

        # setup joints
        self.joints = dict()
        for name in rospy.get_param("~joints", dict()).keys():
            joint_type = rospy.get_param("~joints/"+name+"/type", "dynamixel")
            if joint_type == "dynamixel":
                self.joints[name] = DynamixelServo(self, name)
            elif joint_type == "hobby_servo":
                self.joints[name] = HobbyServo(self, name)
            elif joint_type == "calibrated_linear":
                self.joints[name] = LinearJoint(self, name)

    # TODO: <BEGIN> REMOVE THIS BEFORE 1.0
        if len(rospy.get_param("~dynamixels", dict()).keys()) > 0:
            rospy.logwarn("Warning: use of dynamixels as a dictionary is deprecated and will be removed in 0.8.0")
            for name in rospy.get_param("~dynamixels", dict()).keys():
                self.joints[name] = DynamixelServo(self, name, "~dynamixels")
        if len(rospy.get_param("~servos", dict()).keys()) > 0:
            rospy.logwarn("Warning: use of servos as a dictionary is deprecated and will be removed in 0.8.0")
            for name in rospy.get_param("~servos", dict()).keys():
                self.joints[name] = HobbyServo(self, name, "~servos")
    # TODO: <END> REMOVE THIS BEFORE 1.0

        # setup controller
        self.controllers = [ServoController(self, "servos"), ]
        controllers = rospy.get_param("~controllers", dict())
        for name, params in controllers.items():
            try:
                controller = controller_types[params["type"]](self, name)
                self.controllers.append( controller )
                pause = pause or controller.pause
            except Exception as e:
                if type(e) == KeyError:
                    rospy.logerr("Unrecognized controller: " + params["type"])
                else:  
                    rospy.logerr(str(type(e)) + str(e))

        # wait for arbotix to start up (especially after reset)
        if not self.fake:
            if rospy.has_param("~digital_servos") or rospy.has_param("~digital_sensors") or rospy.has_param("~analog_sensors"):
                pause = True
            if pause:
                while self.getDigital(1) == -1 and not rospy.is_shutdown():
                    rospy.loginfo("Waiting for response...")
                    rospy.sleep(0.25)
            rospy.loginfo("ArbotiX connected.")

        for controller in self.controllers:
            controller.startup()

        # services for io
        rospy.Service('~SetupAnalogIn',SetupChannel, self.analogInCb)
        rospy.Service('~SetupDigitalIn',SetupChannel, self.digitalInCb)
        rospy.Service('~SetupDigitalOut',SetupChannel, self.digitalOutCb)
        # initialize digital/analog IO streams
        self.io = dict()
        if not self.fake:
            for v,t in {"digital_servos":DigitalServo,"digital_sensors":DigitalSensor,"analog_sensors":AnalogSensor}.items():
                temp = rospy.get_param("~"+v,dict())
                for name in temp.keys():
                    pin = rospy.get_param('~'+v+'/'+name+'/pin',1)
                    value = rospy.get_param('~'+v+'/'+name+'/value',0)
                    rate = rospy.get_param('~'+v+'/'+name+'/rate',10)
                    self.io[name] = t(name, pin, value, rate, self)
        
        r = rospy.Rate(self.rate)

        # main loop -- do all the read/write here
        while not rospy.is_shutdown():
    
            # update controllers
            for controller in self.controllers:
                controller.update()

            # update io
            for io in self.io.values():
                io.update()

            # publish feedback
            self.joint_state_publisher.update(self.joints.values(), self.controllers)
            self.diagnostics.update(self.joints.values(), self.controllers)

            r.sleep()

        # do shutdown
        for controller in self.controllers:
            controller.shutdown()

    def analogInCb(self, req):
        # TODO: Add check, only 1 service per pin
        if not self.fake:
            self.io[req.topic_name] = AnalogSensor(req.topic_name, req.pin, req.value, req.rate, self) 
        return SetupChannelResponse()

    def digitalInCb(self, req):
        if not self.fake:
            self.io[req.topic_name] = DigitalSensor(req.topic_name, req.pin, req.value, req.rate, self) 
        return SetupChannelResponse()

    def digitalOutCb(self, req):
        if not self.fake:
            self.io[req.topic_name] = DigitalServo(req.topic_name, req.pin, req.value, req.rate, self) 
        return SetupChannelResponse()


if __name__ == "__main__":
    rospy.init_node('arbotix')
    a = ArbotixROS()
