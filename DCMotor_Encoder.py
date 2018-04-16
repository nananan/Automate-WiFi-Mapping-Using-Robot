import sys
import time 
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

rightWheels = 0 
leftWheels = 1

try:
    motorControl = DCMotor()
    enc = Encoder()
    
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

    
def ObjectAttached(self):
    try:
        attached = self
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        motorControl.setTargetVelocity(0)
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
def ObjectDetached(self):
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        motorControl.setTargetVelocity(0)
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

def VelocityUpdateHandler(e, velocity):
    print("Velocity: %f" % velocity)

def PositionChangeHandler(self, positionChange, timeChange, indexTriggered):
    #print("Position: %f\n" % motorControl.getMotorCount())
    print("Position Changed: %7d  %7.3lf  %d\n" % (positionChange, timeChange, indexTriggered))
    

try:
    motorControl.setOnAttachHandler(ObjectAttached)
    motorControl.setOnDetachHandler(ObjectDetached)
    motorControl.setOnErrorHandler(ErrorEvent)

    motorControl.setOnVelocityUpdateHandler(VelocityUpdateHandler)
    
    enc.setOnAttachHandler(ObjectAttached)
    enc.setOnDetachHandler(ObjectDetached)
    enc.setOnErrorHandler(ErrorEvent)

    enc.setOnPositionChangeHandler(PositionChangeHandler)

    print("Waiting for the Phidget DCMotor Object to be attached...")
    motorControl.openWaitForAttachment(5000)
    enc.openWaitForAttachment(5000)
except PhidgetException as e:
    motorControl.setTargetVelocity(0)
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)


if(not enc.getEnabled()):
    enc.setEnabled(1)

print("INITIAL POSITION: %d\n" % enc.getPosition());

print("Setting Target Velocity to 1 for 5 seconds...\n")
motorControl.setTargetVelocity(0.1)
time.sleep(6)

print("FINAL POSITION: %d\n" % enc.getPosition());

print("Setting Target Velocity to 0 for 5 seconds...\n")
motorControl.setTargetVelocity(0)
time.sleep(1)

try:
    motorControl.close()
    enc.close()
except PhidgetException as e:
    motorControl.setTargetVelocity(0)
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1) 
print("Closed DCMotor device")
exit(0)
                     
