import uuid
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # one-to-one link
    location = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_pics/', default='profile_pics/user-default.png', blank=True,null=True)
    social_linkedin = models.URLField(max_length=200, blank=True, null=True)
    social_instagram = models.URLField(max_length=200, blank=True, null=True)
    social_twitter = models.URLField(max_length=200, blank=True, null=True)
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



    def __str__(self):
     return self.user.username if self.user else self.username or "Unnamed Profile"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
    
class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)


