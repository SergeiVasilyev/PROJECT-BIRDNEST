#!/usr/bin/env python
import math
import requests
import xml.etree.ElementTree as ET
import pandas
import time
from django.conf import settings
import sqlite3
import json
from datetime import datetime, timedelta
import os



class pilot_info:
    def __init__(self, serialNumber):
        pilot = self.parse(serialNumber)

        self.pilotId = pilot['pilotId']
        self.firstName = pilot['firstName']
        self.lastName = pilot['lastName']
        self.phoneNumber = pilot['phoneNumber']
        self.createdDt = pilot['createdDt']
        self.email = pilot['email']

    def parse(self, serialNumber):
        try:
            headers = {'Accept': 'application/json'}
            x = requests.get(f'http://assignments.reaktor.com/birdnest/pilots/{serialNumber}', headers=headers)
            responseJSON = x.json()
            # f = open('birdnestapp/test_pilot.json') # Read from file
            # responseJSON = json.load(f)
        except:
            responseJSON = None
        return responseJSON


class xml_parsre:
    def __init__(self):
        x = requests.get('http://assignments.reaktor.com/birdnest/drones')
        try:
            root = ET.fromstring(x.content) # Read from string
        except:
            root = None
        # root = ET.parse('birdnestapp/test.xml') # Read from file
        self.root = root
        self.drones_list = []
        self.drones_subdic = {}
        self.device_report = {}

    def drones(self):
        # Get Device information
        self.device_report = self.root.find('deviceInformation').attrib
        for deviceInfo in self.root.find('deviceInformation'):
            self.device_report[deviceInfo.tag] = deviceInfo.text
        self.device_report['snapshotTimestamp'] = self.root.find('capture').get('snapshotTimestamp')

        # Get all found drones
        capture = self.root.findall('capture')
        for drone in capture[0].findall('drone'):
            for drn_items in drone:
                self.drones_subdic[drn_items.tag] = drn_items.text

            self.drones_list.append(self.drones_subdic)
            self.drones_subdic = {}

        self.device_report['drone_list'] = self.drones_list
        # print(self.device_report)
        return self.device_report


class drone_monitor:
    def __init__(self):
        self.radius_protect_area = 100000 # Set a protect area
        self.center_x_protect_area = 250000 # Set X point of protect area
        self.center_y_protect_area = 250000 # Set Y point of protect area
        try:
            get_xml = xml_parsre()
            self.drones_report = get_xml.drones()
        except:
            self.drones_report = None
        self.drone_dict = {}
        self.device_dict = {}

    def monitor_main(self):
        self.drone_dict = {}
        if self.drones_report != None:
            self.device_dict['deviceId'] = self.drones_report['deviceId']
            self.device_dict['listenRange'] = self.drones_report['listenRange']
            self.device_dict['deviceStarted'] = self.drones_report['deviceStarted']
            self.device_dict['uptimeSeconds'] = self.drones_report['uptimeSeconds']
            self.device_dict['updateIntervalMs'] = self.drones_report['updateIntervalMs']
            self.device_dict['snapshotTimestamp'] = self.drones_report['snapshotTimestamp']

            for drone in self.drones_report['drone_list']:
                if self.is_in_protect_area(float(drone['positionX']), float(drone['positionY'])):
                    get_drones = {}
                    try:
                        pilot = pilot_info(drone['serialNumber']) # Get pilot info as object from httprequest
                        get_drones = drone # Copy drone to dict
                        get_drones['pilot'] = pilot.__dict__ # add pilot dict in drone dict
                        get_drones['device'] = self.device_dict
                        self.drone_dict[drone['serialNumber']] = get_drones # combine all drones informations
                    except:
                        print('Failed to get XML or JSON response')

            # print('self.drone_dict', self.drone_dict)
        return self.drone_dict

    def is_in_protect_area(self, drn_pos_x, drn_pos_y):
        res = math.sqrt((drn_pos_x - self.center_x_protect_area) ** 2 + (drn_pos_y - self.center_y_protect_area) ** 2)
        if res <= self.radius_protect_area:
            return res
        else:
            return None



def main():
    sqliteConnection = create_connection('../birdnest/db.sqlite3')
    try:
        cursor = sqliteConnection.cursor()
    except sqlite3.Error as e:
        print(e)
    
    combine_list = []
    monitor = drone_monitor()
    drones_in_NDZ = monitor.monitor_main()

    for key, drone in drones_in_NDZ.items(): 
        list_of_drones_NDZ = {} # Create list for pandas
        list_of_drones_NDZ['Drone SN'] = drone['serialNumber']
        list_of_drones_NDZ['Drone model'] = drone['model']
        list_of_drones_NDZ['Drone positionX'] = drone['positionX']
        list_of_drones_NDZ['Drone positionY'] = drone['positionY']
        list_of_drones_NDZ['pilot Id'] = drone['pilot']['pilotId']
        list_of_drones_NDZ['first name'] = drone['pilot']['firstName']
        list_of_drones_NDZ['last name'] = drone['pilot']['lastName']

        combine_list.append(list_of_drones_NDZ) 

        # Append data to SQLite
        with sqliteConnection:
            res = sqliteConnection.execute("SELECT * FROM birdnestapp_dronescannerinfo WHERE deviceId=?", (drone['device']['deviceId'], ))
            get_one_device = res.fetchone()
            time_now = datetime.now()

            if get_one_device == None:
                device_task = (drone['device']['deviceId'], drone['device']['listenRange'], drone['device']['deviceStarted'], drone['device']['uptimeSeconds'], drone['device']['updateIntervalMs'], time_now)
                sql_device = '''INSERT INTO birdnestapp_dronescannerinfo (deviceId, listenRange, deviceStarted, uptimeSeconds, updateIntervalMs, time_added) VALUES (?, ?, ?, ?, ?, ?)'''
                cursor.execute(sql_device, device_task)
                device_id = cursor.lastrowid
            else:
                device_id = get_one_device[0]

            res = sqliteConnection.execute("SELECT * FROM birdnestapp_pilotdata WHERE pilotId=?", (drone['pilot']['pilotId'], ))
            get_one = res.fetchone()

            if get_one == None:
                pilot_task = (drone['pilot']['pilotId'], drone['pilot']['firstName'], drone['pilot']['lastName'], drone['pilot']['phoneNumber'], drone['pilot']['createdDt'], drone['pilot']['email'], time_now)
                sql_pilot = '''INSERT INTO birdnestapp_pilotdata (pilotId, firstName, lastName, phoneNumber, createdDt, email, time_added) VALUES (?, ?, ?, ?, ?, ?, ?)'''
                cursor.execute(sql_pilot, pilot_task)
                pilot_id = cursor.lastrowid
            else:
                pilot_id = get_one[0]

            drone_task = (drone['serialNumber'], drone['model'], drone['manufacturer'], drone['mac'], drone['ipv4'], drone['ipv6'], drone['firmware'], drone['positionY'], drone['positionX'], drone['altitude'], pilot_id, time_now, drone['device']['snapshotTimestamp'], device_id)
            sql_drone = '''INSERT INTO birdnestapp_dronedata (serialNumber, model, manufacturer, mac, ipv4, ipv6, firmware, positionY, positionX, altitude, pilot_id, time_added, snapshotTimestamp, device_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(sql_drone, drone_task)
            sqliteConnection.commit()

    if sqliteConnection:
        sqliteConnection.close()
        # print("The SQLite connection is closed")

    # print(combine_list)
    if combine_list:
        print(pandas.DataFrame(combine_list))
        

def create_connection(db_file):
    db_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'db.sqlite3'))
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def delete_rows(timeDelta):
    # Delete rows created more than <timeDelta> minutes ago
    print('TIME TO DELETE OLD ROWS')
    sqliteConnection = create_connection('../birdnest/db.sqlite3')
    sqliteConnection.execute("PRAGMA foreign_keys = ON")
    cursor = sqliteConnection.cursor()
    try:
        with sqliteConnection:
            sql_drone = 'DELETE FROM birdnestapp_dronedata WHERE time_added<?'
            cursor.execute(sql_drone, (timeDelta,))

            sql_pilot = 'DELETE FROM birdnestapp_pilotdata WHERE time_added<?'
            cursor.execute(sql_pilot, (timeDelta,))

            sqliteConnection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


if __name__ == "__main__":
    now = datetime.now()
    td = timedelta(minutes = 10) # Create timedelta 10 minutes
    # td = timedelta(seconds = 30) # Create timedelta 20 seconds for tests
    now_plus_10 = now + td
    while True:
        now = datetime.now()
        main()
        if now >= now_plus_10:
            delete_rows(now - td)
            now_plus_10 = now + td
        time.sleep(1.8) # restart script every 2 secods



