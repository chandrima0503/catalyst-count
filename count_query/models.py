"""Models file when all the table structures are stored"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Upload(models.Model):
    """Model to upload csv file"""
    file = models.FileField(upload_to='files')

class Count(models.Model):
    """Model to count the number of rows asked by the query"""
    keyword=models.CharField(max_length=20, null=True, blank=True)
    industry=models.CharField(max_length=100, null=True, blank=True)
    year_founded=models.CharField(max_length=29, null=True, blank=True)
    city=models.CharField(max_length=100, null=True, blank=True)
    state=models.CharField(max_length=100, null=True, blank=True)
    country=models.CharField(max_length=10, null=True, blank=True)
    employees_from=models.CharField(max_length=500, null=True, blank=True)
    employees_to=models.CharField(max_length=500, null=True, blank=True)
    
class CompanyManager(models.Manager):
    """Model to provide an object to Company model"""
    pass

class Company(models.Model):
    """Model to store the csv data in database"""
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.IntegerField(null=True)
    industry = models.CharField(max_length=255)
    size_min = models.IntegerField(null=True)  
    size_max = models.IntegerField(null=True)
    city = models.CharField(max_length=255,default='')
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    linkedin_url = models.URLField()
    current_employee_estimate = models.IntegerField()  # Modified to handle integer values
    total_employee_estimate = models.IntegerField()  # Modified to handle integer values

    objects = CompanyManager()

    def __str__(self):
        return self.name

class UserActivityManager(models.Manager):
    """Model to create object for userActivity"""
    pass

class UserActivity(models.Model):
    """Model to store user activity"""
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(default=timezone.now)

    objects = UserActivityManager()
