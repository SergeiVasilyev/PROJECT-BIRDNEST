from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render
from django.conf import settings
from .models import DroneData, PilotData
from .birdnest import drone_monitor, xml_parsre

def main(request):
    drones_in_NDZ_db = DroneData.objects.all().order_by('-id')

    try:
        last_item_id = drones_in_NDZ_db.first().id
    except:
        last_item_id = None

    return render(request, 'birdnest/index.html', {'drones_in_NDZ_db': drones_in_NDZ_db, 'last_item_id': last_item_id})


def drones_outside_NDZ():
    monitor = drone_monitor()
    allDrones = xml_parsre()
    drones = allDrones.drones()

    drone_dict = []
    for drone in drones['drone_list']:
        if not monitor.is_in_protect_area(float(drone['positionX']), float(drone['positionY'])):
            get_drones = {}
            get_drones = drone
            drone_dict.append(get_drones)
    return drone_dict

def drones_inside_NDZ():
    monitor = drone_monitor()
    allDrones = xml_parsre()
    drones = allDrones.drones()

    drone_dict = []
    for drone in drones['drone_list']:
        if monitor.is_in_protect_area(float(drone['positionX']), float(drone['positionY'])):
            get_drones = {}
            get_drones = drone
            drone_dict.append(get_drones)
    return drone_dict


def update_data(request):
    json_response = []

    try:
        outside_NDZ = drones_outside_NDZ()
        inside_NDZ = drones_inside_NDZ()
    except:
        print("Can't parse data")
        outside_NDZ = []
        inside_NDZ = []

    last_item_id = int(request.GET.get('last_item_id')) if request.GET.get('last_item_id') != None else 0
    drones_in_NDZ = DroneData.objects.filter(id__gt=last_item_id).order_by('-id')
    try:
        last_item_id_obj = {'last_item_id': drones_in_NDZ.first().id}
    except:
        last_item_id_obj = {'last_item_id': last_item_id} # Fixed variable

    if drones_in_NDZ:
        for drones in drones_in_NDZ: # Fixed Check if drones_in_NDZ is None
            item = {
                'id': drones.id,
                'serialNumber': drones.serialNumber,
                'model': drones.model,
                'manufacturer': drones.manufacturer,
                'positionX': drones.positionX,
                'positionY': drones.positionY,
                'pilotId': drones.pilot.pilotId,
                'firstName': drones.pilot.firstName,
                'lastName': drones.pilot.lastName,
                'phoneNumber': drones.pilot.phoneNumber,
                'email': drones.pilot.email,
            }
            json_response.append(item)

    return JsonResponse({'drones_in_NDZ_db': json_response, 'last_item_id': last_item_id_obj, 'outside_NDZ': outside_NDZ, 'inside_NDZ': inside_NDZ})



def droneInfo(request, idx):
    try:
        drone = DroneData.objects.get(id=idx)
    except:
        print(f'Drone with id: ${idx} not found')
        drone = {}
    finally:
        context = {'drone': drone}
    return render(request, 'birdnest/drone_info.html', context)



