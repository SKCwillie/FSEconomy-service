from django.http import JsonResponse
from .models import Aircraft
from .serializers import AircraftSerializer


def aircraft_list(request):
    aircraft = Aircraft.objects.all()
    serializer = AircraftSerializer(aircraft, many=True)
    return JsonResponse(serializer.data, safe=False)
