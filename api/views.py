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
    print(type(query_set))
    print(query_set)
    serializer = AirportSerializer(query_set, many=True)
    return JsonResponse(serializer.data[0], safe=False)


def get_assignments_by_airport(request, icao):
    user_key = request.headers['userkey']
    get_assignments(user_key, icao)
    query_set = Assignment.objects.all()
    serializer = AssignmentSerializer(query_set, many=True)
    cur.execute('DELETE FROM api_assignment')
    return JsonResponse(serializer.data, safe=False)
