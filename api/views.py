from django.http import JsonResponse
from .models import Aircraft, Airport
from .serializers import AircraftSerializer, AirportSerializer


def aircraft_list(request):
    query_set = Aircraft.objects.all().order_by('ModelId')
    serializer = AircraftSerializer(query_set, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_aircraft(request, model_id):
    query_set = Aircraft.objects.filter(ModelId=model_id)
    serializer = AircraftSerializer(query_set, many=True)
    return JsonResponse(serializer.data[0], safe=False)


def airport_list(request):
    query_set = Airport.objects.all()
    serializer = AirportSerializer(query_set, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_airport(request, icao):
    query_set = Airport.objects.filter(icao=icao.upper())
    serializer = AirportSerializer(query_set, many=True)
    return JsonResponse(serializer.data[0], safe=False)
