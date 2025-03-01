from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('P', 'Pending'),
    ]

    ROLE_CHOICES = [
        ('C', 'Customer'),
        ('S', 'Seller'),
        ('A', 'Admin'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=False, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P') 
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='C') 
    image_avatar = models.ImageField(upload_to='image_avatars/', blank=True, null=True)

    groups = models.ManyToManyField('auth.Group', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username