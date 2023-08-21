from rest_framework import serializers
from .models import Aircraft, Airport, Assignment, Job


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['MakeModel', 'Crew', 'Seats', 'CruiseSpeed', 'GPH', 'FuelType', 'MTOW', 'EmptyWeight', 'Price',
                  'Ext1', 'LTip', 'LAux', 'LMain', 'Center1', 'Center2', 'Center3', 'RMain', 'RAux', 'RTip', 'RExt2',
                  'Engines', 'EnginePrice', 'ModelId', 'MaxCargo']

    def to_representation(self, instance):
        Fuel = dict()
        Fuel['GPH'] = instance.GPH
        Fuel['Type'] = instance.FuelType
        Fuel['Ext1'] = instance.Ext1
        Fuel['LTip'] = instance.LTip
        Fuel['LAux'] = instance.LAux
        Fuel['LMain'] = instance.LMain
        Fuel['Center1'] = instance.Center1
        Fuel['Center2'] = instance.Center2
        Fuel['Center3'] = instance.Center3
        Fuel['RMain'] = instance.RMain
        Fuel['RAux'] = instance.RAux
        Fuel['RTip'] = instance.RTip
        Fuel['RExt2'] = instance.RExt2
        Fuel[
            'Total'] = instance.Ext1 + instance.LTip + instance.LAux + instance.LMain + instance.Center1 + instance.Center2 + instance.Center3 + instance.RMain + instance.RAux + instance.RTip + instance.RExt2
        Weight = dict()
        Weight['Max'] = instance.MTOW
        Weight['Empty'] = instance.EmptyWeight

        representation = {
            'id': instance.ModelId,
            'makeModel': instance.MakeModel,
            'Seats': instance.Seats,
            'CruiseSpeed': instance.CruiseSpeed,
            'Price': instance.Price,
            'Engines': instance.Engines,
            'EnginePrice': instance.EnginePrice,
            'Fuel': Fuel,
            'Weight': Weight
        }

        return representation


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['icao', 'lat', 'lon', 'type', 'size', 'name', 'city', 'state', 'country']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['index', 'FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay', 'Distance']

    def to_representation(self, instance):
        representation = {
            'FromIcao': instance.FromIcao,
            'ToIcao': instance.ToIcao,
            'Distance': instance.Distance,
            'Pay': instance.Pay,
            'Amount': instance.Amount,
            'UnitType': instance.UnitType,
            'Type': instance.Type
        }
        return representation


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['index', 'FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay', 'Distance', 'ReturnPax']

    def to_representation(self, instance):
        representation = {
            'ToIcao': instance.ToIcao,
            'Distance': instance.Distance,
            'Pay': instance.Pay,
            'Amount': instance.Amount,
            'UnitType': instance.UnitType,
            'Type': instance.Type,
            'ReturnPax': instance.ReturnPax
        }
        return representation
