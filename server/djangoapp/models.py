import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid
# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    Name = models.CharField(max_length=25)
    Description = models.CharField(max_length=25)

    def __str__(self):
        return "Name: "+  self.Name + "\n Descripcion: "+ self.Description



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    Make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    DealerId = models.IntegerField(default=0)
    CAR_MODELS = [
        ('NOT_DEFINED','not_defined'),
        ('SUV', 'Suv'),
        ('WAGON', 'Wagon'),
        ('SEDAN', 'Sedan')
    ]
    Type = models.CharField(max_length=11, choices=CAR_MODELS, default='NOT_DEFINED')
    Year = models.DateField(default=now)
    Color = models.CharField(max_length=10)
    def __str__(self):
        return "Make: " + self.Make.Name +'\n'+ \
                "Dealer Id: " + str(self.DealerId) +\
                "Year: "+ str(self.Year.year)+\
                "Type: "+ self.Type



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
