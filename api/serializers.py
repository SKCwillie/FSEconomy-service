from rest_framework import serializers
from .models import Aircraft, AircraftRental, Airport, Job, AircraftJob, AvailableAircraft
from .scripts import get_financials


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


class AvailableAircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableAircraft
        fields = ['id', 'makeModel']


class AircraftRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftRental
        fields = ['SerialNumber', 'MakeModel', 'Location', 'LocaitonName', 'Home', 'SalePrice', 'Equipment',
                  'RentalDry', 'RentalWet', 'Bonus', 'RentalTime', 'PctFuel', 'NeedsRepair', 'EngineTime',
                  'TimeLast100hr']

    def to_representation(self, instance):
        representation = {
            'MakeModel': instance.MakeModel,
            'SerialNumber': instance.SerialNumber,
            'Equipment': instance.Equipment,
            'Home': instance.Home,
            'NeedsRepair': instance.NeedsRepair,
            'PctFuel': instance.PctFuel,
            'Cost': {
                'RentalDry': instance.RentalDry,
                'RentalWet': instance.RentalWet,
                'Bonus': instance.Bonus
            },
            'EngineTime': instance.EngineTime,
            'TimeLast100h': instance.TimeLast100hr
        }
        return representation


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['icao', 'lat', 'lon', 'type', 'size', 'name', 'city', 'state', 'country']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay', 'Distance', 'ReturnPax']

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


class AircraftJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftJob
        fields = ['FromIcao', 'ToIcao', 'Amount', 'UnitType', 'Type', 'Pay', 'Distance', 'ReturnPax', 'SerialNumber',
                  'MakeModel', 'Registration', 'Location', 'LocaitonName', 'Home', 'SalePrice', 'Equipment',
                  'RentalDry', 'RentalWet',
                  'Bonus', 'RentalTime', 'PctFuel', 'NeedsRepair', 'EngineTime', 'TimeLast100hr']

    def to_representation(self, instance):
        instance = get_financials(instance)
        representation = {
            'Job': {
                'FromIcao': instance.FromIcao,
                'ToIcao': instance.ToIcao,
                'Amount': int(instance.Amount),
                'Distance': int(instance.Distance),
                'UnitType': instance.UnitType,
                'ReturnPax': int(instance.ReturnPax),
                'Pay': int(instance.Pay),
            },
            'Rental': {
                'Registration': instance.Registration,
                'Equipment': instance.Equipment,
                'RentalDry': int(instance.RentalDry),
                'RentalWet': int(instance.RentalWet),
                'Bonus': int(instance.Bonus),
                'NeedsRepair': bool(instance.NeedsRepair)
            },
            'Financial': {
                'NetPay': instance.NetPay,
                'PaxTo': instance.PaxTo,
                'PaxFrom': instance.PaxFrom,
                'BestRental': instance.BestRental,
                'RentalCost': instance.RentalCost,
                'BookingFeeTo': instance.BookingFeeTo,
                'BookingFeeFrom': instance.BookingFeeFrom,
                'Earnings': instance.Earnings,
                'EarningsPerHr': instance.EarningsPerHr
            }
        }
        return representation
