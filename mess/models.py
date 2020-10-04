from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class MessUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(null=True,max_length=100)
    registration_no=models.IntegerField(null=False)
    def __str__(self):
        return str(self.username)

class MessStaff(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(null=True,max_length=100)
    unique_code = models.IntegerField(null=False)
    def __str__(self):
        return str(self.username)


class Item(models.Model):
    price=models.IntegerField()
    item_name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.item_name)

class Booking(models.Model):
    TIMINGS=(
        ('breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner')
    )
    timings=models.CharField(max_length=100,null=False,choices=TIMINGS)
    date_booked=models.DateField(null=False)
    customer=models.ForeignKey(MessUser,on_delete=models.CASCADE)
    item_booked=models.ManyToManyField(Item)
    messmember=models.ForeignKey(MessStaff,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)


