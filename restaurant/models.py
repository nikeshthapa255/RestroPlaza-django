from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Owner(models.Model):
    restaurantName = models.CharField(max_length=100)
    vision = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="restaurantImage")

    def __str__(self):
        return 'Owner of - {} resturant.\nVision -{}'.format(self.restaurantName, self.vision)

    def __repr__(self):
        return self.restaurantName

    class Meta:
        ordering = ["-join_date"]

class Dishes(models.Model):
    dishName =  models.CharField(max_length=100)
    owner = models.ForeignKey(Owner, related_name="dish", on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now=True)
    dishImage = models.ImageField(upload_to="dishImage")
    description = models.TextField()

    def __str__(self):
        return 'Dish - {} \n by Restaurant - {}'.format(self.dishName, self.owner.restaurantName)

    def __repr__(self):
        return self.dishName

    class Meta:
        ordering = ["-join_date"]




