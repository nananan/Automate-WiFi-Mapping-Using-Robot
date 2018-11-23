#!/usr/bin/env python

import rospy
from scapy.all import *

import time, datetime
from nav_msgs.msg import Odometry

from collections import OrderedDict
#user = 'eliana'
import imp
db_man = imp.load_source('DB_Manager', '../cinnamon/src/db.py')
enum_man = imp.load_source('Enum_Type', '../cinnamon/src/Enum_Type.py')
#from db import DB_Manager
#from Enum_Type import Enum_Type


class Sniffer:
	def __init__(self):
		self.x = 1
		self.y = 1
		#rospy.init_node('sniffer', anonymous=False)
		#rospy.loginfo("Started ")
		self.DB_Man = db_man.DB_Manager.getInstance()
		self.odom=None
		self.channel = {
			2412 : 1,
			2417 : 2,
			2422 : 3,
			2427 : 4,
			2432 : 5,
			2437 : 6,
			2442 : 7,
			2447 : 8,
			2452 : 9,
			2457 : 10,
			2462 : 11,
			2467 : 12,
			2472 : 13,

			5180 : 36
		}
		self.pose_subscriber = rospy.Subscriber('odom', Odometry, self.pose_callback)
	
	def pose_callback(self, odom):
		#print(pose)
		self.odom = odom
		#.pose.position
		#orientation = pose.pose.orientation

		# record = OrderedDict([("position_x",pose.x),("position_y",pose.y),("position_z",pose.z),
		# 		("orientation_x",orientation.x), ("orientation_y",orientation.y), ("orientation_z",orientation.z), 
		# 		("orientation_w",orientation.w)])
		# self.db_manager.insert_Waypoint(record)

	def sniffAP(self, p):
		timestamp = datetime.datetime.now().isoformat()
		record_waypoint = None
		if ((p.haslayer(Dot11Beacon))):
			p.show() 
			ssid = p[Dot11Elt].info
			bssid = p[RadioTap].addr3	
			#channel = 'n/a'
			# if len(p[Dot11Elt:3].info) == 1:
			# print(p[Dot11Elt:3].ID)
			#print(int(p.Channel))
			#if p[Dot11Elt:3].ID == 3:
				# print("EEEEEEEEEEEEEEEEHI")
				# channel	= int( ord(p[Dot11Elt:3].info))
			channel = self.channel[p.Channel] if p.haslayer(Dot11Elt) else 'n/a'
			capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
					{Dot11ProbeResp:%Dot11ProbeResp.cap%}")

			type_ = enum_man.Enum_Type.type_packet[p[RadioTap].type]
			subtype = enum_man.Enum_Type.subtypes_management[p[RadioTap].subtype]

			#signal_decoded = ord(p.notdecoded[-4:-3])
			#info = p.sprintf("802.11 %Dot11.type% %Dot11.subtype% %RadioTap.dBm_AntSignal% %Dot11.pw-mgt% %Dot11.addr2% > %Dot11.addr1%")
			packet_signal = None
			packet_signal = p.dBm_AntSignal#-(256 - signal_decoded)
			#print(packet_signal)
			if re.search("privacy", capability): enc = 'Y'
			else: enc  = 'N'

			#p.show()

			record = OrderedDict([
				('access_point_name', ssid),
				('access_point_address', bssid),
				('channel', channel),
				('type', type_),
				('subtype', subtype),
				('strength', packet_signal),
				('timestamp', timestamp)
			])
			if self.odom is not None:
				record_waypoint = OrderedDict([
					("position_x", self.odom.pose.pose.position.x),
					("position_y", self.odom.pose.pose.position.y),
					("position_z", self.odom.pose.pose.position.z),
					("orientation_x", self.odom.pose.pose.orientation.x),
					("orientation_y", self.odom.pose.pose.orientation.y),
					("orientation_z", self.odom.pose.pose.orientation.z),
					("orientation_w", self.odom.pose.pose.orientation.w),
					("AP", bssid),
					("strength", packet_signal)
				])
			#pose_list = list(record_waypoint.items())[:6]
			#record_string = "".join(key[0]+"= "+str(key[1])+"," for key in pose_list)[:-1]
			
			if not self.DB_Man.exists_AP(bssid):
				self.DB_Man.insert_Ap(record)
				#if self.odom is not None:
				self.DB_Man.insert_Waypoint_AP(record_waypoint)
				print("--> INSERT Waypoints set ",record_waypoint," where AP=? ",bssid)
			else:
				#print("SIGNAL: ", signal_decoded)
				if packet_signal is not None:
					self.DB_Man.update_signal_AP(packet_signal, bssid)
					if self.odom is not None and record_waypoint is not None:
						#if not self.DB_Man.exists_Waypoint_AP(bssid, packet_signal):
						self.x = self.x+1
						self.DB_Man.insert_Waypoint_AP(record_waypoint)
					#pose_list = list(record_waypoint.items())[:7]
						#self.DB_Man.update_Waypoint_AP(pose_list, bssid)
						#print("UPDATE Waypoints set ",pose_list," where AP=? ",bssid)
				if channel != 'n/a':
					self.DB_Man.update_channel_AP(channel, bssid)
					#TODO Magari se si verificano entrambe, fare solo un metodo
		#print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])

		#if p.haslayer(Dot11):
			#All packets
			# addr1 = p[Dot11].addr1
			# addr2 = p[Dot11].addr2
			# addr3 = p[Dot11].addr3
		#DA QUI COMMENTATO
		# try:
		# 	#channel	= int( ord(p[Dot11Elt:3].info)) if p.haslayer(Dot11Elt) else 'n/a'
		# 	channel	= self.channel[p.Channel] if p.haslayer(Dot11Elt) else 'n/a'
		# except:	
		# 	channel = 'n/a'
		# capability = p.sprintf("{Dot11ProbeResp:%Dot11ProbeResp.cap%}") if p.haslayer(Dot11ProbeResp) else 'n/a'
		# #print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])
		# type_ = enum_man.Enum_Type.type_packet[p[Dot11FCS].type]
		# #print(p[Dot11].subtype)
		# subtype = enum_man.Enum_Type.subtypes_management[p[Dot11FCS].subtype]
		# #signal_decoded = None
		# #signal_decoded = ord(p.notdecoded[-4:-3]) if hasattr(p, 'notdecoded') else 'n/a'
		# #info = p.sprintf("802.11 %Dot11.type% %Dot11.subtype% %RadioTap.dBm_AntSignal% %Dot11.pw-mgt% %Dot11.addr2% > %Dot11.addr1%")
		# packet_signal = p.dBm_AntSignal# -(256 - signal_decoded) if signal_decoded != None else 'n/a'

		# if hasattr(p, 'FCfield') and p.FCfield is not None:
		# 	DS = p.FCfield & 0x3
		# 	to_DS = DS & 0x1 != 0
		# 	from_DS = DS & 0x2 != 0

		# if to_DS and not from_DS:
		# 	BSSID = p[Dot11FCS].addr1
		# 	source = p[Dot11FCS].addr2
		# 	destination = p[Dot11FCS].addr3
		# elif not to_DS and from_DS:
		# 	BSSID = p[Dot11FCS].addr2
		# 	destination = p[Dot11FCS].addr1
		# 	source = p[Dot11FCS].addr3
		# elif not to_DS and not from_DS:
		# 	destination = p[Dot11FCS].addr1
		# 	source = p[Dot11FCS].addr2
		# 	BSSID = p[Dot11FCS].addr3

		# if BSSID == None: BSSID = 'n/a'
		# if source == None: source = 'n/a'
		# if destination == None: destination = 'n/a'

		# if re.search("privacy", capability): enc = 'Y'
		# else: enc  = 'N'

		# record = OrderedDict([
		# 	('BSSID', BSSID),
		# 	('source', source),
		# 	('destination', destination),
		# 	('channel', channel),
		# 	('type', type_),
		# 	('subtype', subtype),
		# 	('strength', packet_signal),
		# 	('encrypted', enc),
		# 	('to_DS', to_DS),
		# 	('from_DS', from_DS),
		# 	('timestamp', timestamp)
		# ])

		# self.DB_Man.insert_Packet(record);

		# if p.haslayer(EAP):	#AUTHENTICATION is in a Beacon!!!!
		# 	# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		# 	# print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])
		# 	# print(p.addr1, " ", p.addr2, " ", p.addr3)
		# 	# print(to_DS, " ", from_DS)
		# 	# p.show()
		# 	# #if p.haslayer(EAP_PEAP):
		# 	# print("PEAP: ",p[EAP].type, " ", p[EAP].code)
		# 	type_ = enum_man.Enum_Type.eap_types[p[EAP].type]
		# 	code = enum_man.Enum_Type.eap_codes[p[EAP].code]
		# 	record = OrderedDict([
		# 		('BSSID', BSSID),
		# 		('source', source),
		# 		('destination', destination),
		# 		('channel', channel),
		# 		('type', type_),
		# 		('code', code),
		# 		('strength', packet_signal),
		# 		('encrypted', enc),
		# 		('to_DS', to_DS),
		# 		('from_DS', from_DS),
		# 		('timestamp', timestamp)
		# 	])
		# 	#print(record)
		# 	self.DB_Man.insert_EAP(record)


# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# ('Data', ' ', 'Beacon')
# ('fc:19:10:45:ef:01', ' ', 'd8:84:66:43:2a:48', ' ', 'd8:84:66:43:2a:48')
# (False, ' ', True)
