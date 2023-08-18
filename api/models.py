from django.db import models


class Aircraft(models.Model):
    MakeModel = models.CharField(max_length=200)
    Crew = models.IntegerField()
    Seats = models.IntegerField()
    CruiseSpeed = models.IntegerField()
    GPH = models.IntegerField()
    FuelType = models.IntegerField()
    MTOW = models.IntegerField()
    EmptyWeight = models.IntegerField()
    Price = models.FloatField()
    Ext1 = models.IntegerField()
    LTip = models.IntegerField()
    LAux = models.IntegerField()
    LMain = models.IntegerField()
    Center1 = models.IntegerField()
    Center2 = models.IntegerField()
    Center3 = models.IntegerField()
    RMain = models.IntegerField()
    RAux = models.IntegerField()
    RTip = models.IntegerField()
    RExt2 = models.IntegerField()
    Engines = models.IntegerField()
    EnginePrice = models.FloatField()
    ModelId = models.IntegerField(primary_key=True)
    MaxCargo = models.IntegerField()


class Airport(models.Model):
    icao = models.CharField(max_length=4, primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    type = models.CharField(max_length=200)
    size = models.IntegerField()
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)


class Assignment(models.Model):
    index = models.IntegerField(primary_key=True)
    FromIcao = models.CharField(max_length=4)
    ToIcao = models.CharField(max_length=4)
    Amount = models.IntegerField()
    UnitType = models.CharField(max_length=25)
    Type = models.CharField(max_length=25)
    Pay = models.IntegerField()
    Distance = models.IntegerField()
    ReturnAmount = models.IntegerField(null=True)


class Job(models.Model):
    index = models.IntegerField(primary_key=True)
    FromIcao = models.CharField(max_length=4)
    ToIcao = models.CharField(max_length=4)
    Amount = models.IntegerField()
    UnitType = models.CharField(max_length=25)
    Type = models.CharField(max_length=25)
    Pay = models.IntegerField()
    Distance = models.IntegerField()
    ReturnAmount = models.IntegerField(null=True)
    ReturnType = models.CharField(max_length=50, null=True)