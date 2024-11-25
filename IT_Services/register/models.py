from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='services/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


  
class Subscription(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.service}"
    
    
    
class login(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=250,blank=True,null=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.pk and self.password:  # Only hash password if it's a new record
    #         self.password = self.password
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    