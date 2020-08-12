from django.db import models

# Create your models here.
class data(models.Model):
    Displacement = models.IntegerField()
    Horsepower = models.IntegerField()
    Weight_in_lbs = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class hasil(models.Model):
    data = models.ForeignKey(data,on_delete=models.CASCADE)
    hasil = models.IntegerField()