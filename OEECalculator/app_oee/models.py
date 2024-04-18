from django.db import models

class Machine(models.Model):
    machine_name = models.CharField(max_length=100)
    machine_serial_no = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

class ProductionLog(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cycle_no = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    material_name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    duration = models.FloatField()
