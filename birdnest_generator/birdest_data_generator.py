import random
import uuid
import time
import xmltodict

from .model import Drone, Pilot, DeviceInformation, Capture, Report, Report_wrap
from icecream import ic
from datetime import datetime


# TODO: First, you need to build a database of drones and pilots, and then use it to add positions to them

def generate_data():
    drones_num = random.randint(1, 10)

    all_drones = []
    for i in range(drones_num):
        # serialNumber = 'SN-1234567890'
        serialNumber = 'SN-' + str(uuid.uuid4().hex)[:10]
        positionY = random.randint(-500000, 500000)
        positionX = random.randint(-500000, 500000)
        altitude=random.randint(1, 500000)
        all_drones.append(Drone(serialNumber=serialNumber, 
                                model=f'model-{str(uuid.uuid4().hex)[:3]}',
                                positionX=positionX,
                                positionY=positionY,
                                altitude=altitude
                                ))

    pilots = []
    for n in all_drones:
        pilots.append(Pilot(drones=[n]))
        
    updateIntervalMs = 2000
    report = Report(
        deviceInformation=DeviceInformation(updateIntervalMs=updateIntervalMs),
        capture=(Capture(drone=all_drones))
    )
    report = Report_wrap(report=report)

    report_dict = report.model_dump()
    report_dict['report']['deviceInformation']['@deviceId'] = report_dict['report'].pop('deviceId')
    report_dict['report']['capture']['@snapshotTimestamp'] = report_dict['report'].pop('snapshotTimestamp')

    # print(xmltodict.unparse(report_dict, pretty=True))
    # print(pilots.model_dump_json())

    return [report_dict, pilots]
    # return (xmltodict.unparse(report_dict, pretty=True))
    # return (report_dict['report']['capture']['drone'].__len__())


# loop = True
# while loop == True:
#     t0 = time.time()

#     ic(generate_data())

#     t1 = time.time()
#     code_speed = t1-t0
#     ic(code_speed)

#     loop = True
#     time.sleep(2)