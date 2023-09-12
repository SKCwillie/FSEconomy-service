from django.http import JsonResponse
from .serializers import *
from .scripts import *


def aircraft_list(request):
    query_set = Aircraft.objects.all().order_by('ModelId')
    serializer = AircraftSerializer(query_set, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_aircraft(request, model_id):
    try:
        int(model_id)
    except ValueError:
        model_id = aliases[model_id.lower().replace(' ', '')][1]
    print(model_id)
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


def get_jobs(request, icao):
    job_query = Job.objects.filter(FromIcao=icao.upper(), ReturnPax__gt=0)
    job_serializer = JobSerializer(job_query, many=True)
    rental_query = AircraftRental.objects.filter(Location=icao.upper())
    rental_serializer = AircraftRentalSerializer(rental_query, many=True)
    return_json = {icao.upper(): job_serializer.data, 'Rentals': rental_serializer.data}
    return JsonResponse(return_json, safe=False)


def get_jobs_by_aircraft(request, aircraft):
    aircraft = aliases[aircraft.lower().replace(' ', '')][0]
    seats = get_max_pax(aircraft)
    query_set = AircraftJob.objects.filter(MakeModel=aircraft, UnitType='passengers', Amount__gt=seats, ReturnPax__gt=seats, Amount__lt=50)
    serializer = AircraftJobSerializer(query_set, many=True)
    return JsonResponse({aircraft: serializer.data}, safe=False)
