from django.db import models

class Call(models.Model):
    phoneNumber = models.CharField(max_length=12)
    call_date = models.CharField(max_length=20)
    num_delay = models.IntegerField()
    num_entered = models.IntegerField()

# Create your models here.
