import random
import time

from .model import Drone, Pilot, DeviceInformation, Capture, Report, Report_wrap
from icecream import ic

def list_of_drones_and_pilots() -> tuple:
    all_drones = []
    all_pilots = []
    for i in range(30):
        drone = Drone()
        all_drones.append(drone)
        all_pilots.append(Pilot(drones=[drone]))
    return all_drones, all_pilots



def drones_in_radar_range(all_drones) -> object:
    drones = []
    num_of_drones_in_radar_range = random.randint(1, 10)
    for i in range(num_of_drones_in_radar_range):
        r = random.randint(0, 29)
        drone = all_drones[r]
        drone.positionX = random.randint(-500000, 500000)
        drone.positionY = random.randint(-500000, 500000)
        drone.altitude = random.randint(-500000, 500000)
        drones.append(drone)

    return drones



def get_report(detected_drones) -> object:
    updateIntervalMs = 2000
    report = Report(
        deviceInformation=DeviceInformation(updateIntervalMs=updateIntervalMs),
        capture=(Capture(drone=detected_drones))
    )

    return Report_wrap(report=report)


def report_obj_to_dict(report) -> dict:
    """Convert object to dictionary
    and rename fields deviceId and snapshotTimestamp
    to @deviceId and @snapshotTimestamp
    """
    report_dict = report.model_dump()
    report_dict['report']['deviceInformation']['@deviceId'] = report_dict['report'].pop('deviceId')
    report_dict['report']['capture']['@snapshotTimestamp'] = report_dict['report'].pop('snapshotTimestamp')

    return report_dict


def generate_report_of_drones_in_radar_range(all_drones):
    detected_drones = drones_in_radar_range(all_drones)
    report = get_report(detected_drones)
    report_dict = report_obj_to_dict(report)

    return report_dict



if __name__=='__main__':
    all_drones, all_pilots = list_of_drones_and_pilots()
    while True:
        ic(generate_report_of_drones_in_radar_range(all_drones))
        time.sleep(2)
