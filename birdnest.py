import enum
import math
import requests
import xml.etree.ElementTree as ET

# position = [250000, 250000]
# position = [400000, 400000]

# x = requests.get('http://assignments.reaktor.com/birdnest/drones')
# print(x.content)

# tree = ET.fromstring(x.content) # Read from string
# for child in tree.iter('*'):
#     print(child.tag, child.attrib, child.text)

# for drone in tree.findall('drone'):
#     print(drone.find('serialNumber').text)

# capture = tree.findall('capture')
# for el in capture:
#     droneEls = el.findall('drone')
#     print(droneEls)
#     for drn in droneEls:
#         print(drn.find('serialNumber').text)


class xml_parsre:
    def __init__(self):
        x = requests.get('http://assignments.reaktor.com/birdnest/drones')
        root = ET.fromstring(x.content) # Read from string
        self.root = root
        self.drones_list = []
        self.drones_subdic = {}
        self.device_report = {}

    def drones(self):
        # print(self.root.find('deviceInformation').attrib)
        # print(self.root.find('capture').attrib)
        # print(self.root.find('capture').get('snapshotTimestamp'))
        # print(self.root.find('deviceInformation').find('listenRange').text)
        # self.device_dic2[self.root.find('deviceInformation').attrib.fromkeys]
        # print(self.root.find('deviceInformation').attrib)
        # print(self.root.find('deviceInformation').keys()[0])
        # print(self.root.find('deviceInformation').get('deviceId))
        self.device_report = self.root.find('deviceInformation').attrib
        for deviceInfo in self.root.find('deviceInformation'):
            self.device_report[deviceInfo.tag] = deviceInfo.text
        self.device_report['snapshotTimestamp'] = self.root.find('capture').get('snapshotTimestamp')
        # print(self.device_report)

        capture = self.root.findall('capture')
        # print(capture[0].findall('drone'))
        for drone in capture[0].findall('drone'):
            for drn_items in drone:
                self.drones_subdic[drn_items.tag] = drn_items.text
                # print(drn_items.tag, drn_items.text)
            self.drones_list.append(self.drones_subdic)
        self.device_report['drone_list'] = self.drones_list
            
        capture = self.root.findall('capture')
        for el in capture:
            droneEls = el.findall('drone')
            for drn in droneEls:
                for key, drn_subel in enumerate(drn):
                    # print(key, drn_subel.tag, drn_subel.text)
                    self.drones_subdic[drn_subel.tag] = drn_subel.text
                self.drones_list.append(self.drones_subdic)
                # print(ET.dump(drn))
                # print(drn.find('serialNumber').text)
                # print(drn.find('positionY').text)
        # print(self.drones_list)
        self.device_report['drone_list'] = self.drones_list
        print(self.device_report)
        return self.device_report


def main():
    monitor = drone_monitor()
    get_xml = xml_parsre()
    # get_xml.drones()
    # monitor.monitor_main(*position)
    # monitor.monitor_main()

class drone_monitor:
    def __init__(self):
        self.radius_protect_area = 100000
        self.center_x_protect_area = 250000
        self.center_y_protect_area = 250000
        get_xml = xml_parsre()
        self.drones_report = get_xml.drones()

    def monitor_main(self):
        print('List of drones violating the no-fly zone')
        # print(self.drones_report['drone_list'])

        for drone in self.drones().findall('drone'):
            serialNumber = drone.find('serialNumber').text
            drn_pos_x = drone.find('positionX').text
            drn_pos_y = drone.find('positionY').text

            print(serialNumber, drn_pos_x, drn_pos_y)

            drone_point = self.is_in_protect_area(drn_pos_x, drn_pos_y)
            if drone_point is not None:
                print('This drone in no drone zone', drone_point)

    def get_drones(self):
        req = requests.get('http://assignments.reaktor.com/birdnest/drones')
        root = ET.fromstring(req.content)
        return root
    
    def drones(self):
        drones = self.get_drones()
        return drones

    def make_list(self):
        print('List of drones violating the no-fly zone')



    def is_in_protect_area(self, drn_pos_x, drn_pos_y):
        res = math.sqrt((drn_pos_x - self.center_x_protect_area) ** 2 + (drn_pos_y - self.center_y_protect_area) ** 2)
        if res <= self.radius_protect_area:
            return res
        else:
            return None









if __name__ == "__main__":
    main()


