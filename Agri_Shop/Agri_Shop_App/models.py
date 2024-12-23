from django.db import models
from django.contrib.auth.models import User

class registration(models.Model):
    fname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    cpass=models.CharField(max_length=20)

class HighQualitySeed(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/high_quality_seeds/')
    rating = models.TextField(max_length=6)

class OrganicFertilizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/organic_fertilizers/')
    rating = models.TextField(max_length=6)


class SafePesticide(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/safe_pesticides/')
    rating = models.TextField(max_length=6)

class FarmEquipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/farm_equipment/')
    rating = models.TextField(max_length=6)

class AnimalFeed(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/animal_feed/')
    rating = models.TextField(max_length=6)

class AgriElectronicsTool(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/agri_electronics_tools/')
    rating = models.TextField(max_length=6)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product_type = models.CharField(max_length=50) 
    product_id = models.PositiveIntegerField() 
    quantity = models.PositiveIntegerField(default=1)  
    added_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Cart({self.user.username}, {self.product_type}, {self.product_id}, Quantity: {self.quantity})"
    
class Contact_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.IntegerField(null=True)

class Subscribe(models.Model):
    email = models.EmailField(null=False ,unique=True)
    