import os
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render
from django.conf import settings
from .models import DroneData, PilotData
from .birdnest import *
from django.core.paginator import Paginator

def main(request):
    # monitor = drone_monitor()
    # drones_in_NDZ = monitor.monitor_main()
    drones_in_NDZ = DroneData.objects.all().order_by('-id')
    # print(drones_in_NDZ.first().id)
    try:
        last_item_id = drones_in_NDZ.first().id
    except:
        last_item_id = None

    return render(request, 'birdnest/index.html', {'drones_in_NDZ': drones_in_NDZ, 'last_item_id': last_item_id})
    # return render(request, 'birdnest/index.html', {'drones_in_NDZ': drones_in_NDZ})
    # return HttpResponse(os.path.join(settings.BASE_DIR, 'birdnestapp/templates'))

def update_data(request):
    json_response = []
    # print(request.GET.get('last_item_id'))
    last_item_id = int(request.GET.get('last_item_id'))
    drones_in_NDZ = DroneData.objects.filter(id__gt=last_item_id).order_by('-id')
    try:
        last_item_id = {'last_item_id': drones_in_NDZ.first().id}
    except:
        last_item_id = {'last_item_id': request.GET.get('last_item_id')}
    # paginator = Paginator(drones_in_NDZ, 20) # Siirtää muuttujan asetukseen
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    for drones in drones_in_NDZ:
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
    return JsonResponse({'drones_in_NDZ': json_response, 'last_item_id': last_item_id})



def droneInfo(request, idx):
    try:
        drone = DroneData.objects.get(id=idx)
    except:
        print(f'Drone with id: ${idx} not found')
        drone = {}
    finally:
        context = {'drone': drone}
    return render(request, 'birdnest/drone_info.html', context)



