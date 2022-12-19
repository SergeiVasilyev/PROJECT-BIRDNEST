import math
import requests
import xml.etree.ElementTree as ET

x = requests.get('http://assignments.reaktor.com/birdnest/drones')
# print(x.content)

# tree = ET.parse('test.xml') # Read from file
tree = ET.fromstring(x.content) # Read from string
# tree = ET.parse('test.xml')
# tree = ET.parse('test.xml')
for child in tree.iter('*'):
    print(child.tag, child.attrib, child.text)
    




position = [250000, 250000]
# position = [400000, 400000]


def main():
    monitor = drone_monitor()
    monitor.monitor_main(*position)

class drone_monitor:
    def __init__(self):
        self.radius_protect_area = 100000
        self.center_x_protect_area = 250000
        self.center_y_protect_area = 250000   

    def monitor_main(self, drn_pos_x, drn_pos_y):
        drone_point = self.is_in_protect_area(drn_pos_x, drn_pos_y)
        if drone_point is not None:
            print('This drone in no drone zone', drone_point)

    def get_drones(self):
        req = requests.get('http://assignments.reaktor.com/birdnest/drones')
        return req
    
    def parse_xml(self):
        drones = self.get_drones()

    # def make_list(self):
    #     print('sdsd')

    def is_in_protect_area(self, drn_pos_x, drn_pos_y):
        res = math.sqrt((drn_pos_x - self.center_x_protect_area) ** 2 + (drn_pos_y - self.center_y_protect_area) ** 2)
        if res <= self.radius_protect_area:
            return res
        else:
            return None









if __name__ == "__main__":
    main()


