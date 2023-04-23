from django.db import models

# Create your models here.


class Destination:
    id: int
    name: str
    img: str
    desc: str
    price: int
    # def __init__():
    #     pass
    # def __init__(self, id, name, desc, price, img):
    #     self.id = id
    #     self.name = name
    #     self.desc = desc
    #     self.price = price
    #     self.img = img


class Wishlist (models.Model):
    username = models.TextField()
    apartmentID = models.IntegerField()

class Apartment(models.Model):
    ApartmentID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Address = models.TextField()
    Image = models.ImageField(upload_to='apartment_images/')
    Beds = models.IntegerField()
    Bath = models.IntegerField()
    Rent = models.IntegerField()
    Area = models.IntegerField()
    Furnished = models.BooleanField()
    Parking = models.BooleanField()
    Pool = models.BooleanField()
    Gatedcommunity = models.BooleanField()
    Patio = models.BooleanField()
    Garden = models.BooleanField()
    HardwoodFloors = models.BooleanField()
    Gym = models.BooleanField()
    DisabilityAccess = models.BooleanField()
    Kidfriendly = models.BooleanField()
    Washerdryer = models.BooleanField()
    Dishwasher = models.BooleanField()
    Radius = models.IntegerField()

