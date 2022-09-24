from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class vitals_data(models.Model):
    temperature = models.FloatField(default=0.0)
    temperature_flag = models.IntegerField(default=2)

    systolic_bp = models.FloatField(default=0.0)

    diastolic_bp = models.FloatField(default=0.0)

    pulse_rate = models.FloatField(default=0.0)
    bp_flag = models.IntegerField(default=2)

    oxygen_saturation = models.FloatField(default=0.0)
    oxygen_saturation_flag = models.IntegerField(default=2)

    exercise_prediction=models.FloatField(default=0.0)
    exercise_flag= models.IntegerField(default=2)

    health_prediction = models.CharField(max_length=20,default="Normal")
    health_flag = models.IntegerField(default=2)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)