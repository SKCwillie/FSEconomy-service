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


if __name__ == '__main__':
    pass
