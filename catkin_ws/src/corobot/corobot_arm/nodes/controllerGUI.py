#!/usr/bin/env python

""" 
  A simple Controller GUI to drive robots and pose heads.
  Copyright (c) 2008-2011 Michael E. Ferguson.  All right reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
      * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
      * Neither the name of Vanadium Labs LLC nor the names of its 
        contributors may be used to endorse or promote products derived 
        from this software without specific prior written permission.
  
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL VANADIUM LABS BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import roslib; roslib.load_manifest('arbotix_python')
import rospy
import wx

from math import radians

from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from arbotix_msgs.srv import Relax
from arbotix_python.servos import *

width = 325

class servoSlider():
    def __init__(self, parent, min_angle, max_angle, name, i):
        self.name = name
        if name.find("_joint") > 0: # remove _joint for display name
            name = name[0:-6]
        self.position = wx.Slider(parent, -1, 0, int(min_angle*100), int(max_angle*100), wx.DefaultPosition, (150, -1), wx.SL_HORIZONTAL)
        self.enabled = wx.CheckBox(parent, i, name+":")
        self.enabled.SetValue(False)
        self.position.Disable()
	self.synched = 0

    def setPosition(self, angle):
        self.position.SetValue(int(angle*100))

    def getPosition(self):
        return self.position.GetValue()/100.0

class controllerGUI(wx.Frame):
    TIMER_ID = 100

    def __init__(self, parent, debug = False):  
        wx.Frame.__init__(self, parent, -1, "ArbotiX Controller GUI", style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        sizer = wx.GridBagSizer(5,5)

        # Move Base
        drive = wx.StaticBox(self, -1, 'Move Base')
        drive.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        driveBox = wx.StaticBoxSizer(drive,orient=wx.VERTICAL) 
        self.movebase = wx.Panel(self,size=(width,width-20))
        self.movebase.SetBackgroundColour('WHITE')
        self.movebase.Bind(wx.EVT_MOTION, self.onMove)  
        wx.StaticLine(self.movebase, -1, (width/2, 0), (1,width), style=wx.LI_VERTICAL)
        wx.StaticLine(self.movebase, -1, (0, width/2), (width,1))
        driveBox.Add(self.movebase)        
        sizer.Add(driveBox,(0,0),wx.GBSpan(1,1),wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT,5)
        self.forward = 0
        self.turn = 0
        self.X = 0
        self.Y = 0
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist)

        # Move Servos
        servo = wx.StaticBox(self, -1, 'Move Servos')
        servo.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        servoBox = wx.StaticBoxSizer(servo,orient=wx.VERTICAL) 
        servoSizer = wx.GridBagSizer(5,5)

        joint_defaults = getServosFromURDF()
        
        i = 0
        dynamixels = rospy.get_param("/arbotix/dynamixels", dict())
	

        self.servos = list()
        self.publishers = list()
        self.relaxers = list()

	self.synched = list()

        
	# create sliders and publishers
        for name in sorted(dynamixels.keys()):
            # pull angles
            min_angle, max_angle = getServoLimits(name, joint_defaults)
            # create publisher
            self.publishers.append(rospy.Publisher(name+'/command', Float64))
            self.relaxers.append(rospy.ServiceProxy(name+'/relax', Relax))
            # create slider
            s = servoSlider(self, min_angle, max_angle, name, i)
            servoSizer.Add(s.enabled,(i,0), wx.GBSpan(1,1),wx.ALIGN_CENTER_VERTICAL)   
            servoSizer.Add(s.position,(i,1), wx.GBSpan(1,1),wx.ALIGN_CENTER_VERTICAL)

	    #check for synch
	    synch = rospy.get_param("/arbotix/dynamixels/"+name+"/synched", -1)
	    s.synched = int(synch)

            self.servos.append(s)
            i += 1
	    
        # add everything
        servoBox.Add(servoSizer) 
        sizer.Add(servoBox, (0,1), wx.GBSpan(1,1), wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT,5)
        self.Bind(wx.EVT_CHECKBOX, self.enableSliders)
        # now we can subscribe
        rospy.Subscriber('joint_states', JointState, self.stateCb)

        # timer for output
        self.timer = wx.Timer(self, self.TIMER_ID)
        self.timer.Start(50)
        wx.EVT_CLOSE(self, self.onClose)
        wx.EVT_TIMER(self, self.TIMER_ID, self.onTimer)

        # bind the panel to the paint event
        wx.EVT_PAINT(self, self.onPaint)
        self.dirty = 1
        self.onPaint()

        self.SetSizerAndFit(sizer)
        self.Show(True)

    def onClose(self, event):
        self.timer.Stop()
        self.Destroy()

    def enableSliders(self, event):
        servo = event.GetId()
        if event.IsChecked(): 
            self.servos[servo].position.Enable()
        else:
            self.servos[servo].position.Disable()
            self.relaxers[servo]()

    def stateCb(self, msg):        
        for servo in self.servos:
            if not servo.enabled.IsChecked():
                try:
                    idx = msg.name.index(servo.name)
                    servo.setPosition(msg.position[idx])
                except: 
                    pass

    def onPaint(self, event=None):
        # this is the wx drawing surface/canvas
        dc = wx.PaintDC(self.movebase)
        dc.Clear()
        # draw crosshairs
        dc.SetPen(wx.Pen("black",1))
        dc.DrawLine(width/2, 0, width/2, width)
        dc.DrawLine(0, width/2, width, width/2)
        dc.SetPen(wx.Pen("red",2))
        dc.SetBrush(wx.Brush('red', wx.SOLID))
        dc.SetPen(wx.Pen("black",2))
        dc.DrawCircle((width/2) + self.X*(width/2), (width/2) - self.Y*(width/2), 5)  

    def onMove(self, event=None):
        if event.LeftIsDown():        
            pt = event.GetPosition()
            if pt[0] > 0 and pt[0] < width and pt[1] > 0 and pt[1] < width:
                self.forward = ((width/2)-pt[1])/2
                self.turn = (pt[0]-(width/2))/2 
                self.X = (pt[0]-(width/2.0))/(width/2.0)
                self.Y = ((width/2.0)-pt[1])/(width/2.0)        
        else:
            self.forward = 0; self.Y = 0
            self.turn = 0; self.X = 0
        self.onPaint()          
        

    def onTimer(self, event=None):
        # send joint update

	#store info the servo pairs
	shoulder_lift = 0
	elbow_flex = 0

	#set synched servo values
	for s in self.servos:
		if s.synched != -1:
			s.setPosition(self.servos[s.synched].getPosition()*-1)

        for s,p in zip(self.servos,self.publishers):
            if s.enabled.IsChecked():
                d = Float64()
                d.data = s.getPosition()

                p.publish(d)
		
        # send base updates
        t = Twist()
        t.linear.x = self.forward/150.0; t.linear.y = 0; t.linear.z = 0
        if self.forward > 0:
            t.angular.x = 0; t.angular.y = 0; t.angular.z = -self.turn/50.0
        else:
            t.angular.x = 0; t.angular.y = 0; t.angular.z = self.turn/50.0
        self.cmd_vel.publish(t)

if __name__ == '__main__':
    # initialize GUI
    rospy.init_node('controllerGUI')
    app = wx.PySimpleApp()
    frame = controllerGUI(None, True)
    app.MainLoop()

