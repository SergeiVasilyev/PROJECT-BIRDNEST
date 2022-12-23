import math
import os
import requests
import xml.etree.ElementTree as ET
import pandas

from django.conf import settings


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
        headers = {'Accept': 'application/json'}
        x = requests.get(f'http://assignments.reaktor.com/birdnest/pilots/{serialNumber}', headers=headers)
        responseJSON = x.json()
        return responseJSON


class xml_parsre:
    def __init__(self):
        # x = requests.get('http://assignments.reaktor.com/birdnest/drones')
        # root = ET.fromstring(x.content) # Read from string
        # root = ET.parse(os.path.join(settings.BASE_DIR, 'birdnestapp/test_2.xml'))
        root = ET.parse('birdnestapp/test_2.xml')
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
        return self.device_report


class drone_monitor:
    def __init__(self):
        self.radius_protect_area = 100000
        self.center_x_protect_area = 250000
        self.center_y_protect_area = 250000
        get_xml = xml_parsre()
        self.drones_report = get_xml.drones()
        self.drone_dict = {}

    def monitor_main(self):
        for drone in self.drones_report['drone_list']:
            if self.is_in_protect_area(float(drone['positionX']), float(drone['positionY'])):
                get_drones = {}
                pilot = pilot_info(drone['serialNumber']) # Get pilot info as object from httprequest
                get_drones = drone # Copy drone to dict
                get_drones['pilot'] = pilot.__dict__ # add pilot dict in drone dict
                self.drone_dict[drone['serialNumber']] = get_drones # combine all drones informations

        return self.drone_dict

    def drones(self):
        req = requests.get('http://assignments.reaktor.com/birdnest/drones')
        root = ET.fromstring(req.content)
        drones = root
        return drones

    def is_in_protect_area(self, drn_pos_x, drn_pos_y):
        res = math.sqrt((drn_pos_x - self.center_x_protect_area) ** 2 + (drn_pos_y - self.center_y_protect_area) ** 2)
        if res <= self.radius_protect_area:
            return res
        else:
            return None





def main():
    combine_list = []
    monitor = drone_monitor()
    drones_in_NDZ = monitor.monitor_main()
    # print(drones_in_NDZ)
    for key, drone in drones_in_NDZ.items():
        list_of_drones_NDZ = {}
        # print(key, drone)
        # print(drone['serialNumber'])
        # print(drone['pilot']['pilotId'])
        list_of_drones_NDZ['Drone SN'] = drone['serialNumber']
        list_of_drones_NDZ['Drone model'] = drone['model']
        list_of_drones_NDZ['Drone mac'] = drone['mac']
        list_of_drones_NDZ['Drone positionX'] = drone['positionX']
        list_of_drones_NDZ['Drone positionY'] = drone['positionY']
        list_of_drones_NDZ['pilot Id'] = drone['pilot']['pilotId']
        list_of_drones_NDZ['pilot first name'] = drone['pilot']['firstName']
        list_of_drones_NDZ['pilot last name'] = drone['pilot']['lastName']
        # list_of_drones_NDZ['pilot phone number'] = drone['pilot']['phoneNumber']
        # list_of_drones_NDZ['pilot createdDt'] = drone['pilot']['createdDt']
        list_of_drones_NDZ['pilot email'] = drone['pilot']['email']

        combine_list.append(list_of_drones_NDZ)

    print(combine_list)    
    if combine_list:
        print(pandas.DataFrame(combine_list))



if __name__ == "__main__":
    main()


