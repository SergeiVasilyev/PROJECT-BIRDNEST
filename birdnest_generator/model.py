from pydantic import BaseModel, Field, condecimal, ConfigDict
from datetime import datetime
import uuid
from icecream import ic
import random
import xmltodict
import time
from .ip_generator import get_random_ipv4, get_random_ipv6, get_random_mac


NAME = ['John', 'Kate', 'Mila', 'Jan', 'Anna', 'Peter', 'Alex', 'Dan']
LAST_NAME = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Martinez", "Garcia", "Jones"]
MANUFACTORER = ['DJI', 'AeroVironment', 'Parrot', 'PowerVision', 'Freefly']

class Drone(BaseModel):
    model_config = ConfigDict(extra='allow')
    serialNumber: str = Field(default_factory=lambda: 'SN-' + str(uuid.uuid4().hex)[:10])
    model: str = Field(default_factory=lambda: f'model-{str(uuid.uuid4().hex)[:3]}')
    manufacturer: str = Field(default_factory=lambda: MANUFACTORER[random.randint(0, 4)])
    mac: str = Field(default_factory=get_random_mac)
    ipv4: str = Field(default_factory=get_random_ipv4)
    ipv6: str = Field(default_factory=get_random_ipv6)
    firmware: str = '4.0.1'


class Pilot(BaseModel):
    pilotId: str = Field(default_factory=lambda: 'P-' + str(uuid.uuid4().hex)[:10])
    firstName: str = Field(default_factory=lambda: NAME[random.randint(0, 7)])
    lastName: str = Field(default_factory=lambda: LAST_NAME[random.randint(0, 7)])
    phoneNumber: str = Field(default_factory=lambda: f"+{''.join(map(lambda x: str(random.randint(0, 9)), range(1, 12)))}")
    createdDt: datetime = Field(default_factory=lambda: datetime.now())
    email: str = Field(default_factory=lambda: f'{str(uuid.uuid4())[:6]}@gmail.com')
    drones: list[Drone]
    

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


