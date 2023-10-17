from typing import Optional, List
from pydantic import BaseModel, Field, condecimal, ConfigDict
from decimal import Decimal
from datetime import datetime
import uuid
from icecream import ic
import random
import xmltodict
import time


NAME = ['John', 'Kate', 'Mila', 'Jan', 'Anna', 'Peter', 'Alex', 'Dan']
LAST_NAME = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Martinez", "Garcia", "Jones"]
MANUFACTORER = ['DJI', 'AeroVironment', 'Parrot', 'PowerVision', 'Freefly']

class Drone(BaseModel):
    model_config = ConfigDict(extra='allow')
    serialNumber: str = Field(default_factory=lambda: 'SN-' + str(uuid.uuid4().hex)[:10])
    model: str = Field(default_factory=lambda: f'model-{str(uuid.uuid4().hex)[:3]}')
    manufacturer: str = Field(default_factory=lambda: MANUFACTORER[random.randint(0, 4)])
    mac: str = '9c:d2:ac:13:77:71'
    ipv4: str = '66.11.30.157'
    ipv6: str = '3b9f:6b6d:a9eb:03f5:8af8:efd3:e683:8a6e'
    firmware: str = '4.0.1'


class Pilot(BaseModel):
    pilotId: str = Field(default_factory=lambda: 'P-' + str(uuid.uuid4().hex)[:10])
    firstName: str = Field(default_factory=lambda: NAME[random.randint(0, 7)])
    lastName: str = Field(default_factory=lambda: LAST_NAME[random.randint(0, 7)])
    phoneNumber: str = Field(default_factory=lambda: f"+{''.join(map(lambda x: str(random.randint(0, 9)), range(1, 12)))}")
    createdDt: datetime = Field(default_factory=lambda: datetime.now())
    email: str = Field(default_factory=lambda: f'{str(uuid.uuid4())[:6]}@gmail.com')
    drones: list[Drone]


class Pilot_wrap(BaseModel):
    pilots: list[Pilot]
    

class DeviceInformation(BaseModel):
    listenRange: int = 500000
    deviceStarted: datetime = Field(default_factory=lambda: datetime.now())
    uptimeSeconds: int = 5000
    updateIntervalMs: int = 2000

class Capture(BaseModel):
    drone: list[Drone]

class Report(BaseModel):
    deviceInformation: DeviceInformation
    deviceId: str = "GUARDB1RD"
    capture: Capture
    snapshotTimestamp: datetime = Field(default_factory=lambda: datetime.now())

# Required to generate XML using xmltodict
class Report_wrap(BaseModel): 
    report: Report




if __name__=='__main__':
    # Generate drones and pilots
    all_drones = []
    for i in range(20):
        all_drones.append(Drone())

    pilots = []
    for i in range(10):
        pilots.append(Pilot(drones=all_drones[i*2:i*2+2]))

    ic(pilots)

    # Generate report
    loop = True
    while loop == True:
        t0 = time.time()

        drones = all_drones.copy()
        for i, drone in enumerate(drones):
            drones[i].positionY = random.randint(-700000, 700000)
            drones[i].positionX = random.randint(-700000, 700000)
            drones[i].altitude=random.randint(-700000, 700000)

        for i, drone in enumerate(drones):
            if drone.positionX not in range(-500000, 500000) or drone.positionY not in range(-500000, 500000):
                drones.pop(i)

        updateIntervalMs = 2000
        report = Report(
            deviceInformation=DeviceInformation(listenRange=500000, deviceStarted='2022-12-23T19:59:46.911Z', updateIntervalMs=2000),
            capture=(Capture(drone=drones))
        )
        # Make Report wrap becouse xmltodict required one root element
        report = Report_wrap(report=report)

        # Make dict
        report_dict = report.model_dump()

        # Change name deviceId to @deviceId to send it as tag parameter
        report_dict['report']['deviceInformation']['@deviceId'] = report_dict['report'].pop('deviceId')
        report_dict['report']['capture']['@snapshotTimestamp'] = report_dict['report'].pop('snapshotTimestamp')

        print(xmltodict.unparse(report_dict, pretty=True))

        t1 = time.time()
        code_speed = t1-t0
        ic(code_speed)

        loop = False
        time.sleep(2)