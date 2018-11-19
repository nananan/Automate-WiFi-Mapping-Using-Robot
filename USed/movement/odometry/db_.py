#!/usr/bin/python

#import MySQLdb 
import pyodbc
from collections import OrderedDict

# Open database connection
#db = MySQLdb.connect("localhost","root","root","TESTDB" )
class DB_Manager:
	
	db = pyodbc.connect("DRIVER={myodbc_mysql}; SERVER=localhost; PORT=3306;DATABASE=cinnamon; UID=root; PASSWORD=root;")

	def insert_Ap(self, record):
		cursor = self.db.cursor()

		# for row in cursor.execute("select access_point_name from APs"):
		# 	print(row.access_point_name)

		try:
			cursor.execute("insert into APs values (?,?,?,?,?,?,?)", record.values())
			self.db.commit()
		except:
			self.db.rollback()


	def update_signal_AP(self, strength, access_point_address):
		cursor = self.db.cursor()
		try:
			cursor.execute("update APs set strength=? where access_point_address=?", strength, access_point_address)
			self.db.commit()
		except:
			print("ROOOOOOLBACK")
			self.db.rollback()

	def exists_AP(self, mac_address):
		cursor = self.db.cursor()
		#sql = "select exists (select 1 from APs where access_point_address = ?)"
		sql = "select * from APs where access_point_address = ?"
		count = cursor.execute(sql, mac_address).rowcount
		#print("MAC: ", mac_address, " ", count)
		if count > 0:
			return True
		return False

	def select_Waypoints(self):
		cursor = self.db.cursor()
		sql = "select * from Waypoints where AP is NULL"
		waypoints_list = cursor.execute(sql)
		return waypoints_list
	
	def select_Waypoints_AP(self, mac_address):
		cursor = self.db.cursor()
		sql = "select * from Waypoints where AP = ?"
		waypoints_list = cursor.execute(sql, mac_address)
		return waypoints_list

	def insert_Waypoint(self, record):
		cursor = self.db.cursor()
		try:			
			record_string = "("+"".join(key+"," for key in record)[:-1]+")"
			values_string = "("+"".join("?," for key in record)[:-1]+")"
			values = [record[key] for key in record]
			cursor.execute("insert into Waypoints "+record_string+" values "+values_string, values)
			self.db.commit()
		except Exception as e:
			print(e)
			self.db.rollback()

	def insert_Packet(self, record):
		cursor = self.db.cursor()
		try:
			cursor.execute("insert into Packets values (?,?,?,?,?,?,?,?,?,?,?)", record.values())
			self.db.commit()
		except:
			self.db.rollback()

	def insert_EAP(self, record):
		cursor = self7.db.cursor()
		try:
			cursor.execute("insert into EAP values (?,?,?,?,?,?,?,?,?,?,?)", record.values())
			self.db.commit()
		except:
			self.db.rollback()


if __name__ == "__main__":
	DB_Man = DB_Manager();
	#DB_Man.create_table();

	 
    #record = OrderedDict([
    #    ('access_point_name', "aaaaa"),
    #    ('access_point_address', "1234")
    #])

	#DB_Man.insert_Ap(record)
	
	record = OrderedDict([("position_x",12.3),("position_y",13.676767),("position_w",1283.4),("AP","TUTTO IN UNA LINEA CUCCIOLA PUPINA DOLCE")])
	print("INSERT")
	print(record.values())
	DB_Man.insert_Waypoint(record)

	for item in DB_Man.select_Waypoints_AP("TUTTO IN UNA LINEA CUCCIOLA PU"):
		print(item.AP)

	# disconnect from server
	DB_Man.db.close()
