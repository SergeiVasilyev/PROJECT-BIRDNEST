import os
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render
from django.conf import settings

from .birdnest import *

def main(request):
    monitor = drone_monitor()
    drones_in_NDZ = monitor.monitor_main()



    return render(request, 'birdnest/index.html', {'drones_in_NDZ': drones_in_NDZ})
    # return HttpResponse(os.path.join(settings.BASE_DIR, 'birdnestapp/templates'))


