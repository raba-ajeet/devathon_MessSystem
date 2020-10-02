from django.db import models

# Create your models here.

# class (models.Model):


# class (models.Model):

class MessDetails(models.Model):
    timing=models.IntegerField(default=1,null=True)
    date_booked=models.DateField(null=True)
    registration_no=models.IntegerField(null=True)
    def __str__(self):
        return self.registration_no


