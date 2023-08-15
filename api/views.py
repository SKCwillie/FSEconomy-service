from django.http import JsonResponse
from .serializers import *
from .scripts import *


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


def get_assignments_by_airport(request, icao):
    user_key = request.headers['userkey']
    query_set = get_assignments(user_key, icao.upper())
    return JsonResponse(query_set, safe=False)
