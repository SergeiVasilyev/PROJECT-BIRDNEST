import enum
import math
import requests
import xml.etree.ElementTree as ET

# headers = {'Accept': 'application/json'}
# x = requests.get('http://assignments.reaktor.com/birdnest/pilots/SN-exdp-6bzDn', headers=headers)
# print(x.json()['pilotId'])

class pilot_info:
    def __init__(self, serialNumber):
        # self.serialNumber = serialNumber
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
        root = ET.parse('test_2.xml')
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
                # print(drn_items.tag, drn_items.text)

            self.drones_list.append(self.drones_subdic)
            self.drones_subdic = {}
            # print(self.drones_list)

        self.device_report['drone_list'] = self.drones_list
        return self.device_report


def main():
    f1 = pilot_info('SN-exdp-6bzDn')
    monitor = drone_monitor()
    # get_xml = xml_parsre()
    # get_xml.drones()
    # monitor.monitor_main(*position)
    monitor.monitor_main()

class drone_monitor:
    def __init__(self):
        self.radius_protect_area = 100000
        self.center_x_protect_area = 250000
        self.center_y_protect_area = 250000
        get_xml = xml_parsre()
        self.drones_report = get_xml.drones()
        self.drone_list = []

    def monitor_main(self):
        for drone in self.drones_report['drone_list']:
            # print(drone['positionX'], drone['positionY'])
            if self.is_in_protect_area(float(drone['positionX']), float(drone['positionY'])):
                # print(drone['serialNumber'])
                pilot = pilot_info(drone['serialNumber'])
                # print(pilot.__dict__)
                self.drone_list.append(drone)

                drone_dict = drone
                drone_dict['pilot'] = pilot.__dict__
        # print(self.drone_list)
        print(drone_dict)
        return self.drone_list

    def get_drones(self):
        req = requests.get('http://assignments.reaktor.com/birdnest/drones')
        root = ET.fromstring(req.content)
        return root
    
    def drones(self):
        drones = self.get_drones()
        return drones

    def is_in_protect_area(self, drn_pos_x, drn_pos_y):
        res = math.sqrt((drn_pos_x - self.center_x_protect_area) ** 2 + (drn_pos_y - self.center_y_protect_area) ** 2)
        if res <= self.radius_protect_area:
            return res
        else:
            return None









if __name__ == "__main__":
    main()


