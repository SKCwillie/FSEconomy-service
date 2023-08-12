from rest_framework import serializers
from .models import Aircraft


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['MakeModel', 'Crew', 'Seats', 'CruiseSpeed', 'GPH', 'FuelType', 'MTOW', 'EmptyWeight', 'Price',
                  'Ext1', 'LTip', 'LAux', 'LMain', 'Center1', 'Center2', 'Center3', 'RMain', 'RAux', 'RTip', 'RExt2',
                  'Engines', 'EnginePrice', 'ModelId', 'MaxCargo']
