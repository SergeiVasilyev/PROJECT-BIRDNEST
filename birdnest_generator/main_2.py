import asyncio
import xmltodict

from .birdest_data_generator_2 import list_of_drones_and_pilots, generate_report_of_drones_in_radar_range
from icecream import ic
from fastapi import FastAPI, Response


app = FastAPI()

# https://github.com/tiangolo/fastapi/issues/2713
class BackgroundRunner:
    def __init__(self):
        self.data = {}
        self.pilots = []

    async def run_main(self):
        all_drones, self.pilots = list_of_drones_and_pilots()
        while True:
            self.data = xmltodict.unparse(generate_report_of_drones_in_radar_range(all_drones), pretty=True)
            await asyncio.sleep(2)
        

runner = BackgroundRunner()

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(runner.run_main())


@app.get("/")
def read_root():
    return Response(content=runner.data, media_type="application/xml")

@app.get("/pilots/{item_id}")
def read_pilot(item_id: str):
    pilots = runner.pilots
    for n in pilots:
        for x in n.drones:
            if item_id in x.serialNumber:
                return n.dict(exclude={'drones'})
