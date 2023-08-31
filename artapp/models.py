from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('a', 'Admin'),
        ('r', 'Retailer'),
        ('c', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Picture(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to="pictures")

    def __str__(self):
        return self.title


class Cart(models.Model):
    FORMAT_CHOICES = (
        ('audio', 'Audio'),
        ('physical', 'Physical'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: " + self.user.username + " Picture: " + str(self.picture)


class DeliveryInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return "delivery info for " + self.user.username


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    delivery_info = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
